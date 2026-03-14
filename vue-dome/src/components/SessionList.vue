<template>
  <div class="session-list">
    <div class="session-list-header">
      <h2>Sessions</h2>
      <button @click="$emit('create-session')" class="btn-primary">
        + New Session
      </button>
    </div>
    <div class="session-items">
      <div
        v-for="session in sessions"
        :key="session.id"
        :class="['session-item', { active: session.id === currentSessionId }]"
        @click="$emit('select-session', session.id)"
      >
        <div class="session-info">
          <div class="session-model">{{ session.config.model }}</div>
          <div class="session-time">{{ formatTime(session.updated_at) }}</div>
        </div>
        <button
          @click.stop="$emit('delete-session', session.id)"
          class="btn-delete"
          title="Delete session"
        >
          🗑️
        </button>
      </div>
      <div v-if="sessions.length === 0" class="no-sessions">
        No sessions yet. Create one to start!
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  sessions: {
    type: Array,
    required: true,
  },
  currentSessionId: {
    type: String,
    default: null,
  },
});

defineEmits(['create-session', 'select-session', 'delete-session']);

function formatTime(isoString) {
  const date = new Date(isoString);
  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return 'Just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  return `${days}d ago`;
}
</script>

<style scoped>
.session-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.session-list-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.session-list-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  color: #333;
}

.btn-primary {
  width: 100%;
  padding: 0.6rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.session-items {
  flex: 1;
  overflow-y: auto;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.session-item:hover {
  background-color: #f8f8f8;
}

.session-item.active {
  background-color: #e3f2fd;
  border-left: 3px solid #007bff;
}

.session-info {
  flex: 1;
}

.session-model {
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.session-time {
  font-size: 0.75rem;
  color: #999;
}

.btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.btn-delete:hover {
  opacity: 1;
}

.no-sessions {
  padding: 2rem 1rem;
  text-align: center;
  color: #999;
  font-size: 0.9rem;
}
</style>
