import { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { chatAPI } from '../api/client';
import type { Message } from '../types';

export default function ChatPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: session, isLoading: sessionLoading } = useQuery({
    queryKey: ['chat-session', sessionId],
    queryFn: async () => {
      const response = await chatAPI.getSession(sessionId!);
      return response.data;
    },
    enabled: !!sessionId,
  });

  const {
    data: messages,
    isLoading: messagesLoading,
    refetch: refetchMessages,
  } = useQuery({
    queryKey: ['chat-messages', sessionId],
    queryFn: async () => {
      const response = await chatAPI.getMessages(sessionId!);
      return response.data;
    },
    enabled: !!sessionId,
    refetchInterval: 5000, // Poll every 5 seconds
  });

  const sendMessageMutation = useMutation({
    mutationFn: async (content: string) => {
      const response = await chatAPI.sendMessage(sessionId!, content);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-messages', sessionId] });
      refetchMessages();
      setInputValue('');
    },
  });

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      sendMessageMutation.mutate(inputValue);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (sessionLoading) return <div className="loading">Loading chat session...</div>;
  if (!session) return <div className="error">Chat session not found</div>;

  return (
    <div>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <button
            className="button button-secondary"
            onClick={() => navigate(`/objectives/${session.objective_id}`)}
          >
            ← Back to Objective
          </button>
        </div>
        <h2>{session.name || 'Chat Session'}</h2>
      </div>

      <div className="card chat-container">
        <div className="chat-messages">
          {messagesLoading ? (
            <div className="loading">Loading messages...</div>
          ) : messages && messages.length > 0 ? (
            messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))
          ) : (
            <div style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
              No messages yet. Start a conversation!
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="chat-input-container">
          <input
            type="text"
            className="chat-input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about the extracted knowledge..."
            disabled={sendMessageMutation.isPending}
          />
          <button
            type="submit"
            className="button button-primary"
            disabled={sendMessageMutation.isPending || !inputValue.trim()}
          >
            {sendMessageMutation.isPending ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`message ${isUser ? 'message-user' : 'message-agent'}`}
      style={{ alignSelf: isUser ? 'flex-end' : 'flex-start' }}
    >
      <div style={{ marginBottom: '5px' }}>
        <strong style={{ fontSize: '12px', opacity: 0.8 }}>
          {isUser ? 'You' : 'Agent'}
        </strong>
        {message.agent_type && (
          <span style={{ fontSize: '11px', opacity: 0.7, marginLeft: '5px' }}>
            ({message.agent_type})
          </span>
        )}
      </div>
      <div>{message.content}</div>
      {message.sources && message.sources.length > 0 && (
        <div style={{ marginTop: '10px', fontSize: '12px', opacity: 0.8 }}>
          <div style={{ fontWeight: '600', marginBottom: '5px' }}>Sources:</div>
          {message.sources.map((source, index) => (
            <div key={index} style={{ marginBottom: '5px' }}>
              • {source.source_name}
              {source.relevance_score && ` (confidence: ${(source.relevance_score * 100).toFixed(0)}%)`}
            </div>
          ))}
        </div>
      )}
      <div style={{ fontSize: '11px', opacity: 0.6, marginTop: '8px' }}>
        {new Date(message.created_at).toLocaleTimeString()}
      </div>
    </div>
  );
}
