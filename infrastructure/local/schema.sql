-- KETA Database Schema
-- PostgreSQL tables for relational data

SET search_path TO keta, public;

-- ============================================
-- OBJECTIVES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS objectives (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    domain TEXT,
    status TEXT NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'ACTIVE', 'COMPLETED', 'ARCHIVED')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_objectives_status ON objectives(status);
CREATE INDEX idx_objectives_created_at ON objectives(created_at DESC);
CREATE INDEX idx_objectives_domain ON objectives(domain) WHERE domain IS NOT NULL;

-- ============================================
-- SOURCES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    objective_id UUID NOT NULL REFERENCES objectives(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    content_type TEXT NOT NULL DEFAULT 'text' CHECK (content_type IN ('text')),
    content TEXT NOT NULL,
    extraction_status TEXT NOT NULL DEFAULT 'PENDING' CHECK (extraction_status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')),
    extraction_progress JSONB DEFAULT '{}'::jsonb,
    extraction_error TEXT,
    uploaded_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT sources_objective_name_unique UNIQUE (objective_id, name)
);

CREATE INDEX idx_sources_objective_id ON sources(objective_id);
CREATE INDEX idx_sources_extraction_status ON sources(extraction_status);
CREATE INDEX idx_sources_uploaded_at ON sources(uploaded_at DESC);

-- ============================================
-- CHAT SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    objective_id UUID NOT NULL REFERENCES objectives(id) ON DELETE CASCADE,
    name TEXT,
    status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'ARCHIVED')),
    scope_source_ids UUID[],
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_message_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_chat_sessions_objective_id ON chat_sessions(objective_id);
CREATE INDEX idx_chat_sessions_status ON chat_sessions(status);
CREATE INDEX idx_chat_sessions_last_message_at ON chat_sessions(last_message_at DESC);

-- ============================================
-- CHAT MESSAGES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'agent', 'system')),
    agent_type TEXT CHECK (agent_type IN ('extraction', 'conversation')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    sources JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at DESC);
CREATE INDEX idx_chat_messages_role ON chat_messages(role);
CREATE INDEX idx_chat_messages_deleted_at ON chat_messages(deleted_at) WHERE deleted_at IS NULL;

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_objectives_updated_at
    BEFORE UPDATE ON objectives
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- Objective statistics view
CREATE OR REPLACE VIEW objective_stats AS
SELECT
    o.id,
    o.name,
    o.status,
    COUNT(DISTINCT s.id) AS source_count,
    COUNT(DISTINCT s.id) FILTER (WHERE s.extraction_status = 'COMPLETED') AS completed_sources,
    COUNT(DISTINCT s.id) FILTER (WHERE s.extraction_status = 'FAILED') AS failed_sources,
    COUNT(DISTINCT cs.id) AS session_count,
    COUNT(DISTINCT cm.id) AS message_count,
    MAX(s.processed_at) AS last_processed_at,
    MAX(cs.last_message_at) AS last_chat_at
FROM objectives o
LEFT JOIN sources s ON o.id = s.objective_id
LEFT JOIN chat_sessions cs ON o.id = cs.objective_id
LEFT JOIN chat_messages cm ON cs.id = cm.session_id AND cm.deleted_at IS NULL
GROUP BY o.id, o.name, o.status;

\echo 'Database schema created successfully'
