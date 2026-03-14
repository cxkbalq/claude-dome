<template>
  <div class="chat-container">
    <div class="messages-area" ref="messagesArea">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', `message-${message.role}`]"
      >
        <MessageRenderer :message="message" />
      </div>
      <div v-if="isStreaming" class="streaming-indicator">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
    <div class="input-area">
      <textarea
        v-model="inputMessage"
        @keydown.enter.prevent="handleSend"
        placeholder="Type a message to send to Claude..."
        :disabled="isStreaming"
        rows="3"
      ></textarea>
      <button
        @click="handleSend"
        :disabled="!inputMessage.trim() || isStreaming"
        class="btn-send"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import MessageRenderer from './MessageRenderer.vue';

const props = defineProps({
  sessionId: {
    type: String,
    required: true,
  },
  messages: {
    type: Array,
    required: true,
  },
  isStreaming: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['send-message']);

const inputMessage = ref('');
const messagesArea = ref(null);

function handleSend() {
  if (!inputMessage.value.trim() || props.isStreaming) return;

  emit('send-message', inputMessage.value.trim());
  inputMessage.value = '';
}

// Auto-scroll to bottom when new messages arrive
watch(
  () => props.messages.length,
  async () => {
    await nextTick();
    if (messagesArea.value) {
      messagesArea.value.scrollTop = messagesArea.value.scrollHeight;
    }
  }
);
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fff;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 8px;
}

.message-user {
  background-color: #e3f2fd;
  margin-left: 20%;
}

.message-assistant {
  background-color: #f5f5f5;
  margin-right: 20%;
}

.message-tool {
  background-color: #fff3e0;
  margin-right: 20%;
  border-left: 3px solid #ff9800;
}

.streaming-indicator {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  justify-content: center;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #007bff;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  background-color: #fafafa;
}

.input-area textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.9rem;
  resize: none;
}

.input-area textarea:focus {
  outline: none;
  border-color: #007bff;
}

.input-area textarea:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

.btn-send {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-send:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-send:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
