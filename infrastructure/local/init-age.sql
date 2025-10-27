-- Initialize Apache AGE for KETA
-- This script runs after init-db.sql

-- Load AGE extension
CREATE EXTENSION IF NOT EXISTS age;

-- Load ag_catalog into search path
SET search_path = ag_catalog, "$user", public;

-- Create graph for KETA knowledge
SELECT create_graph('keta_graph');

\echo 'Apache AGE initialized successfully'
\echo 'Graph "keta_graph" created'
