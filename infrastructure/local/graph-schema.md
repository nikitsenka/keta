# KETA Graph Schema - Apache AGE

This document describes the graph schema for the KETA knowledge graph stored in Apache AGE.

## Graph Name
`keta_graph`

## Node Labels

### Entity
Represents named entities extracted from text documents.

**Properties:**
- `id` (String/UUID): Unique identifier
- `name` (String): Entity name
- `type` (String): Entity type - one of: PERSON, ORGANIZATION, LOCATION, DATE, PRODUCT, CONCEPT, EVENT
- `source_ids` (Array[UUID]): References to sources table
- `confidence` (Float): Extraction confidence (0.0 to 1.0)
- `extraction_method` (String): Method used for extraction
- `created_at` (Timestamp): Creation timestamp
- `updated_at` (Timestamp): Last update timestamp

**Example:**
```cypher
CREATE (:Entity {
    id: '123e4567-e89b-12d3-a456-426614174000',
    name: 'John Doe',
    type: 'PERSON',
    source_ids: ['abc...'],
    confidence: 0.95,
    extraction_method: 'llm_structured',
    created_at: '2025-10-27T10:00:00Z',
    updated_at: '2025-10-27T10:00:00Z'
})
```

### Document
Graph representation of source documents.

**Properties:**
- `id` (UUID): References sources.id
- `title` (String): Document title
- `chunk_index` (Integer): Chunk number for split documents
- `text_snippet` (String): First 500 characters
- `created_at` (Timestamp): Creation timestamp

**Example:**
```cypher
CREATE (:Document {
    id: '789...',
    title: 'Company Overview',
    chunk_index: 0,
    text_snippet: 'Our company was founded...',
    created_at: '2025-10-27T10:00:00Z'
})
```

## Edge Types

### RELATED_TO
Generic relationship between two entities.

**Properties:**
- `relationship_type` (String): Specific relationship (e.g., works_at, located_in, related_to)
- `description` (String): Natural language description
- `confidence` (Float): Relationship confidence (0.0 to 1.0)
- `source_ids` (Array[UUID]): References to sources

**Example:**
```cypher
MATCH (e1:Entity {name: 'John Doe'}), (e2:Entity {name: 'Acme Corp'})
CREATE (e1)-[:RELATED_TO {
    relationship_type: 'works_at',
    description: 'John Doe is employed by Acme Corp',
    confidence: 0.90,
    source_ids: ['abc...']
}]->(e2)
```

### MENTIONED_IN
Links entity to the document where it was mentioned.

**Properties:**
- `mention_count` (Integer): Number of mentions in document
- `positions` (Array[Integer]): Character positions of mentions
- `context_snippets` (Array[String]): Text context around mentions

**Example:**
```cypher
MATCH (e:Entity {name: 'John Doe'}), (d:Document {id: '789...'})
CREATE (e)-[:MENTIONED_IN {
    mention_count: 3,
    positions: [100, 450, 890],
    context_snippets: ['...John Doe joined...', '...CEO John Doe...', '...Doe stated...']
}]->(d)
```

### EXTRACTED_FROM
Provenance tracking from entity to source.

**Properties:**
- `extraction_date` (Timestamp): When entity was extracted
- `confidence` (Float): Extraction confidence
- `extraction_method` (String): Method used

**Example:**
```cypher
MATCH (e:Entity {name: 'John Doe'}), (d:Document {id: '789...'})
CREATE (e)-[:EXTRACTED_FROM {
    extraction_date: '2025-10-27T10:00:00Z',
    confidence: 0.95,
    extraction_method: 'llm_structured'
}]->(d)
```

## Common Queries

### Find all entities of a specific type
```cypher
SELECT * FROM cypher('keta_graph', $$
    MATCH (e:Entity {type: 'PERSON'})
    RETURN e
$$) AS (entity agtype);
```

### Find relationships between two entities
```cypher
SELECT * FROM cypher('keta_graph', $$
    MATCH (e1:Entity {name: 'John Doe'})-[r:RELATED_TO]->(e2:Entity)
    RETURN e1, r, e2
$$) AS (entity1 agtype, relationship agtype, entity2 agtype);
```

### Find all entities from a specific source
```cypher
SELECT * FROM cypher('keta_graph', $$
    MATCH (e:Entity)-[:EXTRACTED_FROM]->(d:Document {id: 'source_id_here'})
    RETURN e
$$) AS (entity agtype);
```

### Find entities and their connections (depth 2)
```cypher
SELECT * FROM cypher('keta_graph', $$
    MATCH path = (e:Entity {name: 'John Doe'})-[*1..2]-(connected)
    RETURN path
$$) AS (path agtype);
```

## Indexing Strategy

AGE automatically indexes vertex and edge labels. For better performance on specific properties:

1. Entity names are frequently queried - consider indexing
2. Entity types for filtering - consider indexing
3. Document IDs for provenance - consider indexing

Note: AGE indexing syntax may vary; consult Apache AGE documentation for current best practices.
