/**
 * API client for KETA backend
 */

import axios from 'axios';
import type { Objective, Source, ChatSession, Message } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

const client = axios.create({
  baseURL: `${API_URL}${API_PREFIX}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Objectives API
export const objectivesAPI = {
  list: () => client.get<Objective[]>('/objectives'),
  get: (id: string) => client.get<Objective>(`/objectives/${id}`),
  create: (data: Partial<Objective>) => client.post<Objective>('/objectives', data),
  update: (id: string, data: Partial<Objective>) =>
    client.put<Objective>(`/objectives/${id}`, data),
  delete: (id: string) => client.delete(`/objectives/${id}`),
  getStats: (id: string) => client.get(`/objectives/${id}/stats`),
};

// Sources API
export const sourcesAPI = {
  list: (objectiveId: string) =>
    client.get<Source[]>(`/objectives/${objectiveId}/sources`),
  get: (id: string) => client.get<Source>(`/sources/${id}`),
  create: (objectiveId: string, data: Partial<Source>) =>
    client.post<Source>(`/objectives/${objectiveId}/sources`, data),
  delete: (id: string) => client.delete(`/sources/${id}`),
  triggerExtraction: (id: string) =>
    client.post(`/sources/${id}/extract`),
  getExtractionStatus: (id: string) =>
    client.get(`/sources/${id}/extraction-status`),
};

// Chat API
export const chatAPI = {
  listSessions: (objectiveId: string) =>
    client.get<ChatSession[]>('/chat/sessions', { params: { objective_id: objectiveId } }),
  getSession: (id: string) => client.get<ChatSession>(`/chat/sessions/${id}`),
  createSession: (data: Partial<ChatSession>) =>
    client.post<ChatSession>('/chat/sessions', data),
  deleteSession: (id: string) => client.delete(`/chat/sessions/${id}`),
  getMessages: (sessionId: string) =>
    client.get<Message[]>(`/chat/sessions/${sessionId}/messages`),
  sendMessage: (sessionId: string, content: string) =>
    client.post<Message>(`/chat/sessions/${sessionId}/messages`, { content }),
};

// Health API
export const healthAPI = {
  check: () => client.get('/health'),
};

export default client;
