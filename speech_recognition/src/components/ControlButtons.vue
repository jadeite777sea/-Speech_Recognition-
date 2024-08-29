<template>
  <div class="control-buttons">
    <button @click="startRecording">开始录音</button>
    <button @click="pauseRecording">暂停</button>
    <button @click="stopRecording">停止录音</button>
  </div>
</template>

<script>
export default {
  methods: {
    startRecording() {
      this.$emit("start");
    },
    pauseRecording() {
      this.$emit("pause");
    },
    stopRecording() {
      this.$emit("stop");
    },
  },
};
</script>

<style scoped>
.control-buttons {
  display: flex;
  gap: 10px;
}
</style>
