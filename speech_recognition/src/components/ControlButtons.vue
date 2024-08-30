<template>
  <div class="control-buttons" justify="center">
    <button @click="startRecording" icon="el-icon-microphone">开始录音</button>
    <button @click="stopRecording">停止录音</button>
  </div>
</template>

<script>
export default {
  methods: {
    startRecording() {
      this.$emit("start");
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
