# Knowledge Graph Schema - KETA

## Overview

KETA uses Apache AGE (A Graph Extension for PostgreSQL) to store extracted knowledge as a graph of entities and their
relationships. This document describes the graph schema, node types, relationship types, and properties.

---

## Graph Structure

```
┌─────────────────────────────────────────────────────────────┐
│                   Knowledge Graph (AGE)                      │
│                                                              │
│   Entity ──[RELATED_TO]──> Entity                           │
│     │                                                        │
│     ├──[MENTIONED_IN]──> Document                           │
│     └──[EXTRACTED_FROM]──> Document                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

# Run in docker
## Search all entities of type PERSON
```bash
docker exec keta-postgres psql -U postgres -d keta_db -c "LOAD 'age'; SET search_path = ag_catalog, keta, public; SELECT * FROM cypher('keta_graph', \$\$ MATCH (e:Entity {type: 'PERSON'}) RETURN e.name, e.type \$\$) as (name agtype, type agtype);"docker exec keta-postgres psql -U postgres -d keta_db -c "
LOAD 'age';
SET search_path = ag_catalog, keta, public;
SELECT * FROM cypher('keta_graph', \$\$
  MATCH (e:Entity {type: 'ORGANIZATION'})
  RETURN e.name, e.type, e.id
\$\$) as (name agtype, type agtype, id agtype);
"
```
## Search by ID
```bash
 docker exec keta-postgres psql -U postgres -d keta_db -c "LOAD 'age'; SET search_path = ag_catalog, keta, public; SELECT * FROM cypher('keta_graph', 
\$\$
  MATCH (e:Entity {id: '4421a463-460d-448b-92fe-74a33e8e9ad6'})
  RETURN e.name, e.type, e.confidence
\$\$) as (name agtype, type agtype, confidence agtype);
"
```
## Search all relationships of type works_at

```bash 
 docker exec keta-postgres psql -U postgres -d keta_db -c "LOAD 'age'; SET search_path = ag_catalog, keta, public; SELECT * FROM cypher('keta_graph', 
\$\$
  MATCH (e1:Entity)-[r:RELATED_TO]->(e2:Entity)
  RETURN e1.name, e2.name, r.description, r.confidence, r.relationship_type, r.source_ids
\$\$) as (employee agtype, organization agtype, description agtype, confidence agtype, relationship_type agtype, source_ids agtype);"
```

## Summary

The KETA knowledge graph uses a simple but powerful schema:

- **2 Node Types**: Entity, Document
- **3 Relationship Types**: RELATED_TO, MENTIONED_IN, EXTRACTED_FROM
- **7 Entity Types**: PERSON, ORGANIZATION, LOCATION, DATE, PRODUCT, CONCEPT, EVENT
- **Flexible Relationships**: Custom relationship_type property for semantic richness
- **Full Provenance**: Track sources and confidence for all extracted knowledge
- **Query Power**: Leverage Cypher for complex graph traversals and pattern matching

This schema balances simplicity with expressiveness, making it easy to extract, store, and query knowledge from
documents.

