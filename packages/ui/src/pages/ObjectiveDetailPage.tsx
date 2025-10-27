import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { objectivesAPI, sourcesAPI, chatAPI } from '../api/client';
import type { Source } from '../types';

export default function ObjectiveDetailPage() {
  const { objectiveId } = useParams<{ objectiveId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [showUploadForm, setShowUploadForm] = useState(false);

  const { data: objective, isLoading: objectiveLoading } = useQuery({
    queryKey: ['objective', objectiveId],
    queryFn: async () => {
      const response = await objectivesAPI.get(objectiveId!);
      return response.data;
    },
    enabled: !!objectiveId,
  });

  const { data: sources, isLoading: sourcesLoading } = useQuery({
    queryKey: ['sources', objectiveId],
    queryFn: async () => {
      const response = await sourcesAPI.list(objectiveId!);
      return response.data;
    },
    enabled: !!objectiveId,
  });

  const { data: sessions } = useQuery({
    queryKey: ['chat-sessions', objectiveId],
    queryFn: async () => {
      const response = await chatAPI.listSessions(objectiveId!);
      return response.data;
    },
    enabled: !!objectiveId,
  });

  const uploadMutation = useMutation({
    mutationFn: (data: Partial<Source>) => sourcesAPI.create(objectiveId!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources', objectiveId] });
      setShowUploadForm(false);
    },
  });

  const extractMutation = useMutation({
    mutationFn: (sourceId: string) => sourcesAPI.triggerExtraction(sourceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources', objectiveId] });
    },
  });

  const createSessionMutation = useMutation({
    mutationFn: () =>
      chatAPI.createSession({
        objective_id: objectiveId!,
        name: `Chat Session ${new Date().toLocaleString()}`,
      }),
    onSuccess: (response) => {
      navigate(`/chat/${response.data.id}`);
    },
  });

  if (objectiveLoading) return <div className="loading">Loading objective...</div>;
  if (!objective) return <div className="error">Objective not found</div>;

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <button className="button button-secondary" onClick={() => navigate('/')}>
          ← Back to Objectives
        </button>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
          <div>
            <h2>{objective.name}</h2>
            {objective.description && (
              <p style={{ color: '#666', marginTop: '8px' }}>{objective.description}</p>
            )}
          </div>
          <span className={`badge badge-success`}>{objective.status}</span>
        </div>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h3>Sources</h3>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              className="button button-primary"
              onClick={() => setShowUploadForm(!showUploadForm)}
            >
              {showUploadForm ? 'Cancel' : 'Upload Document'}
            </button>
            <button
              className="button button-primary"
              onClick={() => createSessionMutation.mutate()}
              disabled={!sources || sources.length === 0}
            >
              Start Chat
            </button>
          </div>
        </div>

        {showUploadForm && (
          <UploadDocumentForm
            onSubmit={(data) => uploadMutation.mutate(data)}
            isLoading={uploadMutation.isPending}
          />
        )}

        {sourcesLoading ? (
          <div className="loading">Loading sources...</div>
        ) : sources && sources.length > 0 ? (
          <div style={{ marginTop: '20px' }}>
            {sources.map((source) => (
              <SourceCard
                key={source.id}
                source={source}
                onExtract={() => extractMutation.mutate(source.id)}
              />
            ))}
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            No sources yet. Upload a document to get started!
          </div>
        )}
      </div>

      {sessions && sessions.length > 0 && (
        <div className="card">
          <h3>Recent Chat Sessions</h3>
          <div style={{ marginTop: '15px' }}>
            {sessions.map((session) => (
              <div
                key={session.id}
                style={{
                  padding: '15px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  marginBottom: '10px',
                  cursor: 'pointer',
                }}
                onClick={() => navigate(`/chat/${session.id}`)}
              >
                <div style={{ fontWeight: '600' }}>{session.name || 'Untitled Session'}</div>
                <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                  Created: {new Date(session.created_at).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function UploadDocumentForm({
  onSubmit,
  isLoading,
}: {
  onSubmit: (data: Partial<Source>) => void;
  isLoading: boolean;
}) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    content: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '20px', marginBottom: '20px' }}>
      <h4>Upload Text Document</h4>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="label">Document Name *</label>
          <input
            type="text"
            className="input"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label className="label">Description</label>
          <textarea
            className="textarea"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            style={{ minHeight: '60px' }}
          />
        </div>
        <div className="form-group">
          <label className="label">Content *</label>
          <textarea
            className="textarea"
            value={formData.content}
            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            required
            style={{ minHeight: '200px' }}
            placeholder="Paste your text content here..."
          />
        </div>
        <button type="submit" className="button button-primary" disabled={isLoading}>
          {isLoading ? 'Uploading...' : 'Upload Document'}
        </button>
      </form>
    </div>
  );
}

function SourceCard({ source, onExtract }: { source: Source; onExtract: () => void }) {
  const statusColor = {
    PENDING: 'info',
    PROCESSING: 'warning',
    COMPLETED: 'success',
    FAILED: 'danger',
  }[source.extraction_status] || 'info';

  return (
    <div style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '15px', marginBottom: '10px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <div>
          <h4>{source.name}</h4>
          {source.description && (
            <p style={{ color: '#666', fontSize: '14px', marginTop: '5px' }}>{source.description}</p>
          )}
          <div style={{ marginTop: '10px' }}>
            <span className={`badge badge-${statusColor}`}>{source.extraction_status}</span>
            {source.extraction_progress?.entities_extracted !== undefined && (
              <span style={{ marginLeft: '10px', fontSize: '14px', color: '#666' }}>
                {source.extraction_progress.entities_extracted} entities,{' '}
                {source.extraction_progress.relationships_extracted} relationships
              </span>
            )}
          </div>
        </div>
        {source.extraction_status === 'PENDING' && (
          <button className="button button-primary" onClick={onExtract}>
            Extract
          </button>
        )}
      </div>
      {source.extraction_error && (
        <div className="error" style={{ marginTop: '10px' }}>
          {source.extraction_error}
        </div>
      )}
    </div>
  );
}
