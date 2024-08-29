<template>
  <div class="meeting-recording">
    <h1>会议记录</h1>
    <ControlButtons
      @start="startRecording"
      @pause="pauseRecording"
      @stop="stopRecording"
    />
    <TranscriptionPanel :transcriptions="transcriptions" />
  </div>
</template>

<script>
import ControlButtons from "../components/ControlButtons.vue";
import TranscriptionPanel from "../components/TranscriptionPanel.vue";

export default {
  components: { ControlButtons, TranscriptionPanel },
  data() {
    return {
      transcriptions: [], // 存储实时转录内容
    };
  },
  methods: {
    startRecording() {
      // 开始录音并接收转录内容的逻辑
      this.websocket = new WebSocket("ws://localhost:8080/recording");
      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.transcriptions.push(data);
      };
    },
    pauseRecording() {
      // 暂停录音的逻辑
      this.websocket.send(JSON.stringify({ action: "pause" }));
    },
    stopRecording() {
      // 停止录音的逻辑
      this.websocket.send(JSON.stringify({ action: "stop" }));
      this.websocket.close();
    },
  },
};
</script>

<style scoped>
.meeting-recording {
  padding: 20px;
}
</style>
