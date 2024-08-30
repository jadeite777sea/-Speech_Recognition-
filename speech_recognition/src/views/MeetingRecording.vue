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
          <p>发言人{{ speaker_id }}</p>
        </el-card>
        <el-card style="margin-top: 50px">
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
import axios from "axios";
import io from 'socket.io-client';
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
      meeting_name: "",
    };
  },
  methods: {
    async startRecording() {
      this.stopRecording();

      // 获取自动递增的会议名称
      try {
        const response = await axios.get(
          "http://localhost:5000/get_all_meetings"
        );
        const meetingNames = response.data.meetings;

        // 计算下一个会议名称
        const nextMeetingNumber = meetingNames.length + 1;
        this.meeting_name = `Meeting${nextMeetingNumber}`;

        // 向后端创建新会议
        await axios.post("http://localhost:5000/create_meeting", {
          meeting_name: this.meeting_name,
        });

        console.log("New meeting created:", this.meeting_name);
      } catch (error) {
        console.error("Error fetching or creating meeting:", error);
        return;
      }

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

        this.ws = io("http://localhost:5000");
        this.ws.on("connect", () => {
          console.log("WebSocket connection opened");
        });

        this.ws.on("partial_result", (data) => {
          const result = JSON.parse(data);
          this.partial_text = result.partial;
        });
        this.ws.on("final_result", (data) => {
          const result = JSON.parse(data);
          this.final_text = result.text;
          this.speaker_id = result.spk;
        });

        this.workletNode.port.onmessage = (event) => {
          if (this.ws.connected) {
            this.ws.emit('audio_data', event.data);
          }
        };

        source.connect(this.workletNode);
      } catch (error) {
        console.error(
          "Error accessing microphone or initializing AudioContext: ",
          error
        );
      }
    },

    async stopRecording() {
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
        this.ws.disconnect();
        console.log("WebSocket connection closed");
      }
      this.final_text = "";
      this.partial_text = "";
      this.speaker_id = null;
    },
  },
};
</script>

<style scoped>
.meeting-recording {
  padding: 20px;
}
</style>
