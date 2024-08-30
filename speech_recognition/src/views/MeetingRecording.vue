<template>
  <div class="meeting-recording">
    <h1>会议记录</h1>
    <el-row justify="center" align="middle" style="margin-top: 20px">
      <el-col :span="8">
        <el-button
          type="primary"
          @click="startRecording"
          icon="el-icon-microphone"
        >
          Start Recording
        </el-button>
        <el-button
          type="danger"
          @click="stopRecording"
          icon="el-icon-microphone-off"
          style="margin-left: 10px"
        >
          Stop Recording
        </el-button>
      </el-col>
    </el-row>
    <el-row justify="center" align="middle" style="margin-top: 20px">
      <el-col :span="16">
        <el-card>
          <p>{{ partial_text }}</p>
        </el-card>
        <el-card style="margin-top: 50px">
          <p>{{ final_text }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      transcriptions: [], // 存储实时转录内容
      audioContext: null,
      workletNode: null,
      ws: null,
      partial_text: "",
      final_text: "",
      speaker_id: null,
    };
  },
  methods: {
    async startRecording() {
      this.stopRecording();
      // 开始录音并接收转录内容的逻辑
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        this.audioContext = new (window.AudioContext ||
          window.webkitAudioContext)({ sampleRate: 16000 });
        const source = this.audioContext.createMediaStreamSource(stream);
        await this.audioContext.audioWorklet.addModule("/processor.js");
        this.workletNode = new AudioWorkletNode(
          this.audioContext,
          "my-processor"
        );

        this.ws = new WebSocket("ws://localhost:5000");

        this.ws.onopen = () => {
          console.log("WebSocket connection opened");
        };

        this.ws.onmessage = (event) => {
          const result = JSON.parse(event.data);
          if ("partial" in result) {
            this.partial_text = result["partial"];
          }
          if ("text" in result) {
            this.partial_text = result["text"];
            this.final_text = result["text"];
            this.speaker_id = result["spk"];
          }
        };

        this.workletNode.port.onmessage = (event) => {
          if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(event.data);
          }
        };

        source.connect(this.workletNode);
        // this.workletNode.connect(this.audioContext.destination);
        // source.connect(this.audioContext.destination);
      } catch (error) {
        console.error(
          "Error accessing microphone or initializing AudioContext: ",
          error
        );
      }
    },

    stopRecording() {
      // 停止录音的逻辑
      if (this.workletNode) {
        this.workletNode.disconnect();
        this.workletNode = null;
      }

      if (this.audioContext) {
        this.audioContext.close();
        this.audioContext = null;
      }

      if (this.ws) {
        this.ws.close();
        console.log("WebSocket connection closed");
      }
      this.partial_text = "";
    },
  },
};
</script>

<style scoped>
.meeting-recording {
  padding: 20px;
}
</style>
