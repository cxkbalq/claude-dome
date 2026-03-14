<template>
  <div class="settings-overlay" @click.self="$emit('close')">
    <div class="settings-modal">
      <div class="settings-header">
        <h2>Settings</h2>
        <button @click="$emit('close')" class="btn-close">✕</button>
      </div>
      <div class="settings-body">
        <div class="form-group">
          <label>API Key</label>
          <input
            v-model="localConfig.api_key"
            type="password"
            placeholder="Enter your Claude API key"
          />
        </div>

        <div class="form-group">
          <label>Model</label>
          <select v-model="localConfig.model">
            <option value="claude-sonnet-4-5-20250929">Claude Sonnet 4.5</option>
            <option value="claude-opus-4-5-20251101">Claude Opus 4.5</option>
            <option value="claude-haiku-4-5-20251001">Claude Haiku 4.5</option>
          </select>
        </div>

        <div class="form-group">
          <label>Provider</label>
          <select v-model="localConfig.provider">
            <option value="anthropic">Anthropic</option>
            <option value="bedrock">AWS Bedrock</option>
            <option value="vertex">Google Vertex</option>
          </select>
        </div>

        <div class="form-group">
          <label>Max Output Tokens</label>
          <input
            v-model.number="localConfig.max_tokens"
            type="number"
            min="1024"
            max="128000"
          />
        </div>

        <div class="form-group">
          <label>Thinking Budget (optional)</label>
          <input
            v-model.number="localConfig.thinking_budget"
            type="number"
            min="0"
            placeholder="Leave empty to disable"
          />
        </div>

        <div class="form-group">
          <label>Tool Version</label>
          <select v-model="localConfig.tool_version">
            <option value="computer_use_20250124">2025-01-24</option>
            <option value="computer_use_20250429">2025-04-29</option>
            <option value="computer_use_20251124">2025-11-24</option>
          </select>
        </div>

        <div class="form-group">
          <label>Recent Images to Keep</label>
          <input
            v-model.number="localConfig.only_n_most_recent_images"
            type="number"
            min="0"
            max="10"
          />
        </div>

        <div class="form-group">
          <label>
            <input
              v-model="localConfig.token_efficient_tools_beta"
              type="checkbox"
            />
            Enable Token-Efficient Tools Beta
          </label>
        </div>

        <div class="form-group">
          <label>Custom System Prompt</label>
          <textarea
            v-model="localConfig.system_prompt"
            rows="4"
            placeholder="Additional instructions for Claude..."
          ></textarea>
        </div>
      </div>
      <div class="settings-footer">
        <button @click="$emit('close')" class="btn-secondary">Cancel</button>
        <button @click="handleSave" class="btn-primary">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['close', 'save']);

const localConfig = ref({ ...props.config });

watch(
  () => props.config,
  (newConfig) => {
    localConfig.value = { ...newConfig };
  },
  { deep: true }
);

function handleSave() {
  emit('save', localConfig.value);
}
</script>

<style scoped>
.settings-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.settings-modal {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.settings-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.btn-close:hover {
  color: #333;
}

.settings-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
  font-size: 0.9rem;
}

.form-group input[type='text'],
.form-group input[type='password'],
.form-group input[type='number'],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.9rem;
}

.form-group input[type='checkbox'] {
  margin-right: 0.5rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
}

.settings-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}
</style>
