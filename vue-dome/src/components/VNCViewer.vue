<template>
  <div class="vnc-viewer">
    <iframe src="http://localhost:6080/" frameborder="0"></iframe>
  </div>
</template>

<script setup>
// No script needed for this simple implementation
</script>

<style scoped>
.vnc-viewer {
  width: 100%;
  height: 100%;
}

.vnc-viewer iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>
