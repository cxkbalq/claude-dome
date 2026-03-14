<template>
  <div class="message-renderer">
    <div class="message-role">{{ roleLabel }}</div>
    <div class="message-content">
      <template v-if="Array.isArray(message.content)">
        <div
          v-for="(block, index) in message.content"
          :key="index"
          class="content-block"
        >
          <!-- Text content -->
          <div v-if="block.type === 'text'" class="text-content">
            {{ block.text }}
          </div>

          <!-- Thinking content -->
          <div v-else-if="block.type === 'thinking'" class="thinking-content">
            <div class="thinking-label">💭 Thinking</div>
            <div class="thinking-text">{{ block.thinking }}</div>
          </div>

          <!-- Tool use -->
          <div v-else-if="block.type === 'tool_use'" class="tool-use">
            <div class="tool-label">🔧 Tool: {{ block.name }}</div>
            <pre class="tool-input">{{ JSON.stringify(block.input, null, 2) }}</pre>
          </div>

          <!-- Tool result -->
          <div v-else-if="block.type === 'tool_result'" class="tool-result">
            <div v-if="block.output" class="tool-output">
              <pre>{{ block.output }}</pre>
            </div>
            <div v-if="block.error" class="tool-error">
              ❌ Error: {{ block.error }}
            </div>
            <div v-if="block.base64_image" class="tool-image">
              <img :src="`data:image/png;base64,${block.base64_image}`" alt="Screenshot" />
            </div>
          </div>
        </div>
      </template>

      <!-- Tool result (direct) -->
      <template v-else-if="message.role === 'tool'">
        <div v-if="message.content.output" class="tool-output">
          <pre>{{ message.content.output }}</pre>
        </div>
        <div v-if="message.content.error" class="tool-error">
          ❌ Error: {{ message.content.error }}
        </div>
        <div v-if="message.content.base64_image" class="tool-image">
          <img :src="`data:image/png;base64,${message.content.base64_image}`" alt="Screenshot" />
        </div>
      </template>

      <!-- Simple text -->
      <div v-else class="text-content">
        {{ message.content }}
      </div>
    </div>
    <div class="message-time">{{ formatTime(message.created_at) }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
});

const roleLabel = computed(() => {
  const labels = {
    user: 'You',
    assistant: 'Claude',
    tool: 'Tool Result',
  };
  return labels[props.message.role] || props.message.role;
});

function formatTime(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleTimeString();
}
</script>

<style scoped>
.message-renderer {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.message-role {
  font-weight: 600;
  font-size: 0.85rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.content-block {
  display: flex;
  flex-direction: column;
}

.text-content {
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.thinking-content {
  background-color: #f0f0f0;
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 3px solid #9c27b0;
}

.thinking-label {
  font-weight: 600;
  font-size: 0.85rem;
  color: #9c27b0;
  margin-bottom: 0.5rem;
}

.thinking-text {
  color: #666;
  font-style: italic;
  line-height: 1.5;
}

.tool-use {
  background-color: #e8f5e9;
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 3px solid #4caf50;
}

.tool-label {
  font-weight: 600;
  font-size: 0.85rem;
  color: #4caf50;
  margin-bottom: 0.5rem;
}

.tool-input {
  background-color: #fff;
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  overflow-x: auto;
  margin: 0;
}

.tool-result {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tool-output pre {
  background-color: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  overflow-x: auto;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.tool-error {
  color: #d32f2f;
  background-color: #ffebee;
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 3px solid #d32f2f;
}

.tool-image {
  margin-top: 0.5rem;
}

.tool-image img {
  max-width: 100%;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.message-time {
  font-size: 0.75rem;
  color: #999;
  text-align: right;
}
</style>
