/**
 * SSE (Server-Sent Events) Client
 */

class SSEClient {
  constructor() {
    this.eventSource = null;
  }

  /**
   * Connect to SSE stream
   * @param {string} url - Stream URL
   * @param {Object} callbacks - Event callbacks
   * @param {Function} callbacks.onContent - Content event callback
   * @param {Function} callbacks.onToolResult - Tool result event callback
   * @param {Function} callbacks.onError - Error event callback
   * @param {Function} callbacks.onComplete - Complete event callback
   */
  connect(url, callbacks = {}) {
    this.disconnect(); // Close existing connection

    this.eventSource = new EventSource(url);

    this.eventSource.onopen = () => {
      console.log('SSE connection opened');
    };

    this.eventSource.onmessage = (event) => {
      console.log('SSE message received:', event.data);
      try {
        const data = JSON.parse(event.data);
        console.log('SSE event type:', data.event);

        switch (data.event) {
          case 'content':
            console.log('Calling onContent callback with:', data.data);
            callbacks.onContent?.(data.data);
            break;
          case 'tool_result':
            callbacks.onToolResult?.(data.data);
            break;
          case 'complete':
            console.log('SSE complete, disconnecting');
            callbacks.onComplete?.();
            this.disconnect();
            break;
          case 'error':
            callbacks.onError?.(data.data);
            this.disconnect();
            break;
          default:
            console.warn('Unknown SSE event:', data.event);
        }
      } catch (error) {
        console.error('Error parsing SSE message:', error);
        callbacks.onError?.(error);
      }
    };

    this.eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      callbacks.onError?.(error);
      this.disconnect();
    };
  }

  /**
   * Disconnect from SSE stream
   */
  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }

  /**
   * Check if connected
   * @returns {boolean} Connection status
   */
  isConnected() {
    return this.eventSource !== null && this.eventSource.readyState === EventSource.OPEN;
  }
}

export default SSEClient;
