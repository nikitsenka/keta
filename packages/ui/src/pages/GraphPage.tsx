import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { graphAPI } from '../api/client';
import { GraphVisualization } from '../components/GraphVisualization';
import type { GraphVisualizationData, Entity } from '../types';

const ENTITY_TYPES = ['PERSON', 'ORGANIZATION', 'LOCATION', 'DATE', 'PRODUCT', 'CONCEPT', 'EVENT'];

export default function GraphPage() {
  const { objectiveId } = useParams<{ objectiveId: string }>();
  const navigate = useNavigate();
  const [searchName, setSearchName] = useState('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [graphData, setGraphData] = useState<GraphVisualizationData>({ nodes: [], edges: [] });
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);

  const { data: entities, isLoading: entitiesLoading, error: entitiesError } = useQuery({
    queryKey: ['entities', objectiveId, searchName, selectedType],
    queryFn: async () => {
      if (!objectiveId) return [];
      const response = await graphAPI.searchEntities(objectiveId, {
        name: searchName || undefined,
        entity_type: selectedType || undefined,
        limit: 100,
      });
      return response.data;
    },
    enabled: !!objectiveId,
  });

  const { data: stats } = useQuery({
    queryKey: ['graph-stats', objectiveId],
    queryFn: async () => {
      if (!objectiveId) return null;
      const response = await graphAPI.getStatistics(objectiveId);
      return response.data;
    },
    enabled: !!objectiveId,
  });

  const { data: neighborhoodData } = useQuery({
    queryKey: ['entity-neighborhood', selectedEntityId],
    queryFn: async () => {
      if (!selectedEntityId) return null;
      const response = await graphAPI.getEntityNeighborhood(selectedEntityId, 2);
      return response.data;
    },
    enabled: !!selectedEntityId,
  });

  useEffect(() => {
    if (entities && entities.length > 0 && !selectedEntityId) {
      const initialData: GraphVisualizationData = {
        nodes: entities.map((entity: Entity) => ({
          id: entity.id,
          label: entity.name,
          type: entity.type,
          properties: {
            confidence: entity.confidence,
            source_ids: entity.source_ids,
          },
        })),
        edges: [],
      };
      setGraphData(initialData);
    }
  }, [entities, selectedEntityId]);

  useEffect(() => {
    if (neighborhoodData) {
      setGraphData(neighborhoodData);
    }
  }, [neighborhoodData]);

  const handleNodeClick = (nodeId: string) => {
    setSelectedEntityId(nodeId);
  };

  const handleSearch = () => {
    setSelectedEntityId(null);
  };

  if (entitiesLoading) return <div className="loading">Loading knowledge graph...</div>;
  if (entitiesError) return <div className="error">Error loading knowledge graph</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Knowledge Graph</h2>
        <button className="button" onClick={() => navigate(`/objectives/${objectiveId}`)}>
          Back to Objective
        </button>
      </div>

      {stats && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>Graph Statistics</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginTop: '15px' }}>
            <div>
              <strong>Total Entities:</strong> {stats.total_entities}
            </div>
            <div>
              <strong>Total Relationships:</strong> {stats.total_relationships}
            </div>
          </div>
          <div style={{ marginTop: '15px' }}>
            <strong>Entity Types:</strong>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
              {Object.entries(stats.entity_type_counts).map(([type, count]) => (
                <span key={type} className="badge badge-info">
                  {type}: {count}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="card" style={{ marginBottom: '20px' }}>
        <h3>Search & Filter</h3>
        <div style={{ display: 'flex', gap: '10px', marginTop: '15px', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="Search by entity name..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            style={{ flex: '1', minWidth: '200px', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          />
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            style={{ padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          >
            <option value="">All Types</option>
            {ENTITY_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
          <button className="button button-primary" onClick={handleSearch}>
            Search
          </button>
          {selectedEntityId && (
            <button
              className="button"
              onClick={() => {
                setSelectedEntityId(null);
                handleSearch();
              }}
            >
              Reset View
            </button>
          )}
        </div>
        {selectedEntityId && (
          <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
            <strong>Viewing neighborhood of selected entity</strong> - Click another node to explore or reset view
          </div>
        )}
      </div>

      <div className="card">
        {graphData.nodes.length > 0 ? (
          <GraphVisualization
            data={graphData}
            onNodeClick={handleNodeClick}
            width={1000}
            height={600}
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <p>No entities found. Upload and extract sources to populate the knowledge graph.</p>
          </div>
        )}
      </div>

      {entities && entities.length > 0 && (
        <div className="card" style={{ marginTop: '20px' }}>
          <h3>Entities ({entities.length})</h3>
          <div style={{ maxHeight: '300px', overflowY: 'auto', marginTop: '15px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                  <th style={{ padding: '8px' }}>Name</th>
                  <th style={{ padding: '8px' }}>Type</th>
                  <th style={{ padding: '8px' }}>Confidence</th>
                  <th style={{ padding: '8px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {entities.map((entity: Entity) => (
                  <tr key={entity.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '8px' }}>{entity.name}</td>
                    <td style={{ padding: '8px' }}>
                      <span className="badge badge-info">{entity.type}</span>
                    </td>
                    <td style={{ padding: '8px' }}>{(entity.confidence * 100).toFixed(0)}%</td>
                    <td style={{ padding: '8px' }}>
                      <button
                        className="button"
                        onClick={() => setSelectedEntityId(entity.id)}
                        style={{ padding: '4px 8px', fontSize: '12px' }}
                      >
                        Explore
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
