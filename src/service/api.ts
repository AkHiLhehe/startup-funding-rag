// src/services/api.ts
export interface ChatResponse {
  answer: string;
  sources: string[];
}

export const askAnalyst = async (query: string, language: string): Promise<ChatResponse> => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, language }),
  });
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};