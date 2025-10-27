/**
 * TypeScript type definitions for KETA UI
 */

export interface Objective {
  id: string;
  name: string;
  description?: string;
  domain?: string;
  status: 'DRAFT' | 'ACTIVE' | 'COMPLETED' | 'ARCHIVED';
  created_at: string;
  updated_at: string;
  metadata: Record<string, any>;
}

export interface Source {
  id: string;
  objective_id: string;
  name: string;
  description?: string;
  content_type: string;
  content: string;
  extraction_status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  extraction_progress: Record<string, any>;
  extraction_error?: string;
  uploaded_at: string;
  processed_at?: string;
  metadata: Record<string, any>;
}

export interface ChatSession {
  id: string;
  objective_id: string;
  name?: string;
  status: 'ACTIVE' | 'ARCHIVED';
  scope_source_ids: string[];
  created_at: string;
  last_message_at?: string;
  metadata: Record<string, any>;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'agent' | 'system';
  agent_type?: 'extraction' | 'conversation';
  content: string;
  metadata: Record<string, any>;
  sources: SourceCitation[];
  created_at: string;
  deleted_at?: string;
}

export interface SourceCitation {
  source_id: string;
  source_name: string;
  snippet: string;
  relevance_score?: number;
}

export interface Entity {
  id: string;
  name: string;
  type: string;
  source_ids: string[];
  confidence: number;
  extraction_method: string;
  created_at: string;
  updated_at: string;
}

export interface Relationship {
  entity1_id: string;
  entity1_name: string;
  entity2_id: string;
  entity2_name: string;
  relationship_type: string;
  description: string;
  confidence: number;
  source_ids: string[];
}
