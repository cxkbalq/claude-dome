<template>
  <div class="computer-use-container">
    <!-- Header -->
    <div class="header">
      <h1>Claude Computer Use</h1>
      <div class="header-actions">
        <button @click="showSettings = !showSettings" class="btn-secondary">
          ⚙️ Settings
        </button>
        <button @click="showVNC = !showVNC" class="btn-secondary">
          🖥️ {{ showVNC ? 'Hide' : 'Show' }} VNC
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Sidebar -->
      <div class="sidebar">
        <SessionList
          :sessions="sessions"
          :currentSessionId="currentSessionId"
          @create-session="handleCreateSession"
          @select-session="handleSelectSession"
          @delete-session="handleDeleteSession"
        />
      </div>

      <!-- Chat Area -->
      <div class="chat-area">
        <Chat
          v-if="currentSessionId"
          :sessionId="currentSessionId"
          :messages="currentMessages"
          :isStreaming="isStreaming"
          @send-message="handleSendMessage"
        />
        <div v-else class="no-session">
          <p>Select a session or create a new one to start</p>
        </div>
      </div>

      <!-- VNC Viewer (conditional) -->
      <div v-if="showVNC" class="vnc-area">
        <VNCViewer />
      </div>
    </div>

    <!-- Settings Modal -->
    <Settings
      v-if="showSettings"
      :config="sessionConfig"
      @close="showSettings = false"
      @save="handleSaveConfig"
    />
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue';
import SessionList from './SessionList.vue';
import Chat from './Chat.vue';
import VNCViewer from './VNCViewer.vue';
import Settings from './Settings.vue';
import ApiService from '../services/api.js';
import SSEClient from '../services/sse.js';

// State
const sessions = ref([]);
const currentSessionId = ref(null);
const currentMessages = ref([]);
const isStreaming = ref(false);
const showSettings = ref(false);
const showVNC = ref(false);

// Session configuration
const sessionConfig = ref({
  model: 'claude-sonnet-4-5-20250929',
  provider: 'anthropic',
  api_key: localStorage.getItem('api_key') || '',
  system_prompt: localStorage.getItem('system_prompt') || '',
  max_tokens: 16384,
  thinking_budget: null,
  tool_version: 'computer_use_20250124',
  only_n_most_recent_images: 3,
  token_efficient_tools_beta: false,
});

// SSE Client
const sseClient = new SSEClient();

// Computed
const currentSession = computed(() => {
  return sessions.value.find(s => s.id === currentSessionId.value);
});

// Methods
async function loadSessions() {
  try {
    sessions.value = await ApiService.getSessions();
  } catch (error) {
    console.error('Failed to load sessions:', error);
  }
}

async function handleCreateSession() {
  try {
    const session = await ApiService.createSession(sessionConfig.value);
    sessions.value.unshift(session);
    currentSessionId.value = session.id;
    currentMessages.value = [];
  } catch (error) {
    console.error('Failed to create session:', error);
    alert('Failed to create session. Please check your API key.');
  }
}

async function handleSelectSession(sessionId) {
  try {
    currentSessionId.value = sessionId;
    const session = await ApiService.getSession(sessionId);
    currentMessages.value = session.messages || [];
  } catch (error) {
    console.error('Failed to load session:', error);
  }
}

async function handleDeleteSession(sessionId) {
  try {
    await ApiService.deleteSession(sessionId);
    sessions.value = sessions.value.filter(s => s.id !== sessionId);
    if (currentSessionId.value === sessionId) {
      currentSessionId.value = null;
      currentMessages.value = [];
    }
  } catch (error) {
    console.error('Failed to delete session:', error);
  }
}

async function handleSendMessage(message) {
  if (!currentSessionId.value || isStreaming.value) return;

  try {
    // Add user message to UI
    currentMessages.value.push({
      role: 'user',
      content: [{ type: 'text', text: message }],
      created_at: new Date().toISOString(),
    });

    // Send message to backend
    await ApiService.sendMessage(currentSessionId.value, message);

    // Start streaming response
    isStreaming.value = true;
    const streamUrl = ApiService.getStreamUrl(currentSessionId.value);

    // Temporary assistant message for streaming (use reactive)
    const assistantMessage = reactive({
      role: 'assistant',
      content: [],
      created_at: new Date().toISOString(),
      streaming: true,
    });
    currentMessages.value.push(assistantMessage);

    sseClient.connect(streamUrl, {
      onContent: (data) => {
        console.log('onContent received:', data);
        
        // Handle streaming text content
        if (data.type === 'text') {
          if (data.partial) {
            // For partial text chunks, append to the last text block or create new one
            const lastBlock = assistantMessage.content[assistantMessage.content.length - 1];
            if (lastBlock && lastBlock.type === 'text') {
              // Append to existing text block
              lastBlock.text += data.text;
            } else {
              // Create new text block
              assistantMessage.content.push({
                type: 'text',
                text: data.text
              });
            }
          } else if (data.text === '' && data.partial === false) {
            // Final marker for text completion - no action needed
            console.log('Text streaming complete');
          }
        } else {
          // Non-text content (thinking, tool_use, etc.) - add as new block
          assistantMessage.content.push(data);
        }
      },
      onToolResult: (data) => {
        console.log('onToolResult received:', data);
        // Add tool result to messages
        currentMessages.value.push({
          role: 'tool',
          content: data,
          created_at: new Date().toISOString(),
        });
      },
      onComplete: () => {
        console.log('onComplete received');
        isStreaming.value = false;
        assistantMessage.streaming = false;
        // Don't reload session - the message is already displayed
        // If needed, we can reload in the background without updating UI
      },
      onError: (error) => {
        console.error('Streaming error:', error);
        isStreaming.value = false;
        alert('Error during streaming. Please try again.');
      },
    });
  } catch (error) {
    isStreaming.value = false;
    console.error('Failed to send message:', error);
    alert('Failed to send message. Please try again.');
  }
}

function handleSaveConfig(config) {
  sessionConfig.value = { ...config };
  localStorage.setItem('api_key', config.api_key);
  localStorage.setItem('system_prompt', config.system_prompt);
  showSettings.value = false;
}

// Lifecycle
onMounted(() => {
  loadSessions();
});
</script>

<style scoped>
.computer-use-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 300px;
  background-color: #fff;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.vnc-area {
  width: 600px;
  background-color: #000;
  border-left: 1px solid #e0e0e0;
}

.no-session {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 1.2rem;
}
</style>
