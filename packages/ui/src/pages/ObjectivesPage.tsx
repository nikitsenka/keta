import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { objectivesAPI } from '../api/client';
import type { Objective } from '../types';

export default function ObjectivesPage() {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: objectives, isLoading, error } = useQuery({
    queryKey: ['objectives'],
    queryFn: async () => {
      const response = await objectivesAPI.list();
      return response.data;
    },
  });

  const createMutation = useMutation({
    mutationFn: (data: Partial<Objective>) => objectivesAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['objectives'] });
      setShowCreateForm(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => objectivesAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['objectives'] });
    },
  });

  if (isLoading) return <div className="loading">Loading objectives...</div>;
  if (error) return <div className="error">Error loading objectives</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Objectives</h2>
        <button
          className="button button-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : 'Create New Objective'}
        </button>
      </div>

      {showCreateForm && (
        <CreateObjectiveForm
          onSubmit={(data) => createMutation.mutate(data)}
          isLoading={createMutation.isPending}
        />
      )}

      <div className="grid grid-2">
        {objectives?.map((objective) => (
          <div key={objective.id} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <div>
                <h3
                  style={{ cursor: 'pointer', color: '#007bff' }}
                  onClick={() => navigate(`/objectives/${objective.id}`)}
                >
                  {objective.name}
                </h3>
                {objective.description && (
                  <p style={{ color: '#666', marginTop: '8px' }}>{objective.description}</p>
                )}
                {objective.domain && (
                  <span className="badge badge-info" style={{ marginTop: '8px' }}>
                    {objective.domain}
                  </span>
                )}
              </div>
              <span className={`badge badge-${getStatusColor(objective.status)}`}>
                {objective.status}
              </span>
            </div>
            <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
              <button
                className="button button-primary"
                onClick={() => navigate(`/objectives/${objective.id}`)}
              >
                View Details
              </button>
              <button
                className="button button-danger"
                onClick={() => {
                  if (confirm('Are you sure you want to delete this objective?')) {
                    deleteMutation.mutate(objective.id);
                  }
                }}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {objectives?.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ color: '#666' }}>No objectives yet. Create your first objective to get started!</p>
        </div>
      )}
    </div>
  );
}

function CreateObjectiveForm({
  onSubmit,
  isLoading,
}: {
  onSubmit: (data: Partial<Objective>) => void;
  isLoading: boolean;
}) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    domain: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="card">
      <h3>Create New Objective</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="label">Name *</label>
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
          />
        </div>
        <div className="form-group">
          <label className="label">Domain</label>
          <input
            type="text"
            className="input"
            value={formData.domain}
            onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
            placeholder="e.g., medical, legal, technical"
          />
        </div>
        <button type="submit" className="button button-primary" disabled={isLoading}>
          {isLoading ? 'Creating...' : 'Create Objective'}
        </button>
      </form>
    </div>
  );
}

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    DRAFT: 'info',
    ACTIVE: 'success',
    COMPLETED: 'success',
    ARCHIVED: 'warning',
  };
  return colors[status] || 'info';
}
