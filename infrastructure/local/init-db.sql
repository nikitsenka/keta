-- Initialize PostgreSQL database for KETA
-- This script runs first during container initialization

-- Ensure PostgreSQL extensions are available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schema for application tables
CREATE SCHEMA IF NOT EXISTS keta;

-- Set search path
SET search_path TO keta, public;

\echo 'PostgreSQL database initialized successfully'
