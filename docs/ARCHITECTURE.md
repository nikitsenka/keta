# KETA Architecture - POC

## System Architecture Overview

### High-Level Components

```
┌─────────────┐
│   React UI  │  User interface for managing objectives, uploading documents, chatting
└──────┬──────┘
       │ HTTP/REST
┌──────┴──────┐
│  FastAPI    │  REST API endpoints
└──────┬──────┘
       │
┌──────┴──────┐
│  LangGraph  │  Agent orchestrator - routes to Extraction or Conversation agent
│ Orchestrator│
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──┴──┐ ┌──┴──┐
│Extr.│ │Conv.│  Two specialized agents
│Agent│ │Agent│
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
   ┌───┴────────┐
   │   Tools    │  Entity extraction, graph queries, relationship traversal
   └───┬────────┘
       │
   ┌───┴──────────┐
   │              │
┌──┴───────┐  ┌──┴─────┐
│PostgreSQL│  │  AGE   │  Hybrid storage: metadata + graph
│ Tables   │  │ Graph  │
└──────────┘  └────────┘
```

---

## Agent Orchestration Flow

### Message Processing Flow

```
User Message
    │
    ▼
Load Context (session, history, objective)
    │
    ▼
Agent Orchestrator (LangGraph)
    │
    ├─ Classify Intent
    │  ├─ Keywords: "extract", "process" → Extraction Agent
    │  └─ Keywords: "what", "who", "how" → Conversation Agent
    │
    ▼
Execute Agent
    │
    ├─ Extraction Agent
    │  ├─ Extract entities (LLM)
    │  ├─ Extract relationships (LLM)
    │  └─ Insert to graph
    │
    └─ Conversation Agent
       ├─ Parse question
       ├─ Query graph (Cypher)
       ├─ Get entities/relationships
       └─ Generate answer (LLM)
    │
    ▼
Return Response + Sources
    │
    ▼
Persist to chat_messages
    │
    ▼
Send to User
```

---

## Data Model Relationships

### PostgreSQL Tables

```
objectives (1) ───< (many) sources
    │                     │
    │                     └─ content_type: "text"
    │                     └─ extraction_status: PENDING/PROCESSING/COMPLETED/FAILED
    │
    └───< (many) chat_sessions
             │
             └───< (many) chat_messages
                      │
                      └─ role: user/agent/system
                      └─ agent_type: extraction/conversation
                      └─ sources: JSONB array
```

### Apache AGE Graph

```
Entity nodes
    │
    ├─ Properties: id, name, type, confidence, source_ids
    │
    ├─ RELATED_TO ──> Entity (with relationship_type)
    ├─ MENTIONED_IN ──> Document (with mention_count, positions)
    └─ EXTRACTED_FROM ──> Document (with extraction_date)

Document nodes
    │
    └─ Properties: id (references sources.id), title, chunk_index
```

---

## Knowledge Graph Schema

### Node Types

**Entity**
- Extracted named entities
- Types: PERSON, ORGANIZATION, LOCATION, DATE, PRODUCT, CONCEPT, EVENT
- Tracks: source_ids, confidence, extraction timestamp

**Document**
- Represents chunks of source documents
- Links to entities mentioned within
- Stores text snippet for context

### Relationship Types

**RELATED_TO** (Entity → Entity)
- Generic relationship between entities
- Properties: relationship_type, description, confidence, source_ids

**MENTIONED_IN** (Entity → Document)
- Entity appears in document
- Properties: mention_count, positions (character offsets)

**EXTRACTED_FROM** (Entity → Document)
- Provenance tracking
- Properties: extraction_date, confidence

---

## Extraction Pipeline

### Entity and Relationship Extraction Flow

```
Text Document
    │
    ▼
Chunk if large (>10k tokens)
    │
    ▼
Extract Entities (LLM with structured output)
    │
    ├─ Prompt: "Identify named entities in this text"
    ├─ Output: List of {name, type, confidence}
    ├─ Types: PERSON, ORG, LOCATION, DATE, PRODUCT, CONCEPT, EVENT
    │
    ▼
Store Entities in Graph
    │
    ├─ Create Entity node
    ├─ Link to Document (MENTIONED_IN)
    ├─ Track source_id
    │
    ▼
Extract Relationships (LLM with structured output)
    │
    ├─ Input: Text + list of entities
    ├─ Prompt: "Identify relationships between these entities"
    ├─ Output: List of {entity1, entity2, type, description, confidence}
    │
    ▼
Store Relationships in Graph
    │
    ├─ Create RELATED_TO edge
    ├─ Set relationship_type property
    ├─ Track source_id and confidence
    │
    ▼
Update extraction_status = COMPLETED
    │
    ▼
Return Summary (entities count, relationships count)
```

---

## Conversation Agent Workflow

### Question Answering Flow

```
User Question
    │
    ▼
Parse Question
    │
    ├─ Identify mentioned entities
    ├─ Determine query type (lookup, traversal, comparison)
    │
    ▼
Generate Graph Query
    │
    ├─ Entity lookup: MATCH (e:Entity {name: "..."})
    ├─ Relationship traversal: MATCH (e1)-[r]-(e2)
    ├─ Multi-hop: MATCH (e1)-[*1..3]-(e2)
    │
    ▼
Execute Cypher Query
    │
    ├─ Query graph database
    ├─ Get entities, relationships, context
    │
    ▼
Rank Results
    │
    ├─ By confidence score
    ├─ By relevance to question
    │
    ▼
Generate Answer (LLM)
    │
    ├─ Context: Question + graph results
    ├─ Prompt: "Answer based on this knowledge"
    ├─ Output: Natural language answer
    │
    ▼
Add Source Citations
    │
    ├─ Link to source documents
    ├─ Include entity IDs and confidence
    │
    ▼
Return Response
```

---

## Agent Routing Logic

### Intent Classification

```
Incoming Message
    │
    ▼
Keyword Analysis
    │
    ├─ "extract", "process", "analyze document"
    │  └──> Route to Extraction Agent
    │
    ├─ "what", "who", "where", "when", "how", "tell me"
    │  └──> Route to Conversation Agent
    │
    └─ Default
       └──> Route to Conversation Agent
```

### Two Agents Only

**Extraction Agent**
- Trigger: Document processing keywords
- Actions: Extract entities, extract relationships, store in graph
- Tools: extract_entities, extract_relationships, graph_insert

**Conversation Agent**
- Trigger: Question keywords or default
- Actions: Query graph, generate answer, cite sources
- Tools: entity_search, relationship_traversal, cypher_query

---

## Technology Stack Layers

### Application Layers

```
Presentation Layer
├─ React 19
├─ TypeScript 5.9
├─ D3.js 7.9 (graph visualization)
└─ Vite 7 (build tool)

API Layer
├─ FastAPI 0.119+
├─ Pydantic 2.12+ (validation)
└─ Uvicorn 0.37+ (ASGI server)

Agent Layer
├─ LangGraph 0.6+ (orchestration)
└─ LangChain 0.3+ (LLM abstraction)

Data Layer
├─ PostgreSQL 17 (relational tables)
├─ Apache AGE 1.1+ (graph database)
└─ asyncpg 0.30+ (async driver)

LLM Layer
└─ OpenAI API

Infrastructure
├─ Docker 28+
└─ Docker Compose 2.39+
```

---

### Future Enhancements

Can be improved later with:
- Dedicated NER models (spaCy, Flair)
- Entity linking and deduplication
- Fact extraction
- Concept hierarchies
- Multi-pass extraction
- Confidence calibration

---

## Data Flow Examples

### Example 1: Document Upload and Extraction

```
User uploads document → POST /api/v1/objectives/{id}/sources
    │
    ▼
Create source record (status: PENDING)
    │
    ▼
Trigger extraction → POST /api/v1/sources/{id}/extract
    │
    ▼
Update status: PROCESSING
    │
    ▼
Chunk document if large
    │
    ▼
For each chunk:
    ├─ Extract entities (LLM)
    ├─ Extract relationships (LLM)
    ├─ Insert to graph
    └─ Update progress
    │
    ▼
Update status: COMPLETED
    │
    ▼
Return summary
```

### Example 2: Chat Query

```
User asks: "Who works at Google?"
    │
    ▼
POST /api/v1/chat/sessions/{id}/messages
    │
    ▼
Load session, history, objective
    │
    ▼
Orchestrator classifies intent → "query"
    │
    ▼
Route to Conversation Agent
    │
    ▼
Agent generates Cypher:
MATCH (person:Entity {type: 'PERSON'})-[r:RELATED_TO {relationship_type: 'works_at'}]->(org:Entity {name: 'Google'})
RETURN person.name
    │
    ▼
Execute query → Results: ["Alice", "Bob"]
    │
    ▼
LLM generates answer: "Based on the knowledge graph, Alice and Bob work at Google."
    │
    ▼
Add sources (entity IDs, document IDs, confidence)
    │
    ▼
Save message to chat_messages
    │
    ▼
Return response to user
```

---

## Project Structure

### Monorepo Layout

```
keta/
├─ packages/
│  ├─ api/           # FastAPI backend
│  ├─ agents/        # LangGraph agents
│  ├─ graph/         # Database repositories
│  ├─ shared/        # Shared utilities
│  └─ ui/            # React frontend
│
├─ infrastructure/
│  └─ docker/        # Docker configurations
│
├─ docs/             # Documentation
│
├─ docker-compose.yml
├─ README.md
├─ IMPLEMENTATION_PLAN.md
└─ ARCHITECTURE.md
```
