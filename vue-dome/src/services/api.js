/**
 * API Service for backend communication
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

/**
 * API Service Class
 */
class ApiService {
  /**
   * Create a new session
   * @param {Object} config - Session configuration
   * @returns {Promise<Object>} Session object
   */
  async createSession(config) {
    const response = await apiClient.post('/sessions', config);
    return response.data;
  }

  /**
   * Get all sessions
   * @param {number} limit - Maximum number of sessions
   * @param {number} offset - Offset for pagination
   * @returns {Promise<Array>} List of sessions
   */
  async getSessions(limit = 100, offset = 0) {
    const response = await apiClient.get('/sessions', {
      params: { limit, offset },
    });
    return response.data;
  }

  /**
   * Get session details
   * @param {string} sessionId - Session ID
   * @returns {Promise<Object>} Session details with messages
   */
  async getSession(sessionId) {
    const response = await apiClient.get(`/sessions/${sessionId}`);
    return response.data;
  }

  /**
   * Delete a session
   * @param {string} sessionId - Session ID
   * @returns {Promise<Object>} Deletion confirmation
   */
  async deleteSession(sessionId) {
    const response = await apiClient.delete(`/sessions/${sessionId}`);
    return response.data;
  }

  /**
   * Send a message to a session
   * @param {string} sessionId - Session ID
   * @param {string} message - Message text
   * @returns {Promise<Object>} Message confirmation
   */
  async sendMessage(sessionId, message) {
    const response = await apiClient.post(`/sessions/${sessionId}/messages`, {
      message,
    });
    return response.data;
  }

  /**
   * Get stream URL for a session
   * @param {string} sessionId - Session ID
   * @returns {string} Stream URL
   */
  getStreamUrl(sessionId) {
    return `${API_BASE_URL}/sessions/${sessionId}/stream`;
  }

  /**
   * Health check
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    const response = await apiClient.get('/health');
    return response.data;
  }
}

export default new ApiService();
