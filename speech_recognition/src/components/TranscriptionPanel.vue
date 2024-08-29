<template>
  <div class="transcription-panel">
    <div
      v-for="(transcription, index) in transcriptions"
      :key="index"
      :class="transcription.speaker"
    >
      <strong>{{ transcription.speaker }}:</strong> {{ transcription.text }}
    </div>
  </div>
</template>

<script>
export default {
  props: ["transcriptions"], // Array of transcriptions passed from parent
};
</script>

<style scoped>
.transcription-panel {
  border: 1px solid #ccc;
  padding: 10px;
  height: 300px;
  overflow-y: auto;
}
.speaker1 {
  color: blue;
}
.speaker2 {
  color: green;
}
</style>
