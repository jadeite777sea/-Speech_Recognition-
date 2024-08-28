<template>
  <div class="meeting">
    <div class="video-container">
      <div class="video-stream" v-for="(user, index) in users" :key="index">
        <div class="video-placeholder">{{ user.name }}</div>
      </div>
    </div>
    <div class="controls">
      <el-button type="primary" icon="el-icon-microphone" @click="toggleRecording">
        {{ recording ? 'Stop Recording' : 'Start Recording' }}
      </el-button>
      <el-button type="primary" icon="el-icon-video-camera">Stop Video</el-button>
      <el-button type="primary" icon="el-icon-share">Share Screen</el-button>
      <el-button type="primary" icon="el-icon-chat-line-round">Chat</el-button>
    </div>
    <div class="sidebar">
      <el-card class="chat-window">
        <div class="chat-header">Chat</div>
        <div class="chat-messages">
          <div v-for="(message, index) in messages" :key="index" class="chat-message">
            <strong>{{ message.user }}:</strong> {{ message.text }}
          </div>
        </div>
        <el-input v-model="newMessage" placeholder="Type a message" @keyup.enter="sendMessage"></el-input>
      </el-card>
      <el-card class="participants">
        <div class="participants-header">Participants</div>
        <ul>
          <li v-for="(user, index) in users" :key="index">{{ user.name }}</li>
        </ul>
      </el-card>
    </div>
  </div>
</template>

<script>
import Recorder from 'recorder-js'

export default {
  data () {
    return {
      users: [
        { name: 'User 1' },
        { name: 'User 2' },
        { name: 'User 3' }
      ],
      messages: [
        { user: 'User 1', text: 'Hello everyone!' },
        { user: 'User 2', text: 'Hi there!' }
      ],
      newMessage: '',
      recorder: null,
      audioContext: null,
      recording: false
    }
  },
  methods: {
    sendMessage () {
      if (this.newMessage.trim()) {
        this.messages.push({ user: 'You', text: this.newMessage })
        this.newMessage = ''
      }
    },
    async toggleRecording () {
      if (this.recording) {
        this.stopRecording()
      } else {
        await this.startRecording()
      }
    },
    async startRecording () {
      if (!this.recorder) {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)()
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        this.recorder = new Recorder(this.audioContext, {
          onAnalysed: (data) => console.log(data)
        })
        this.recorder.init(stream)
      }

      this.recorder.start().then(() => {
        this.recording = true
        console.log('Recording started')
      })
    },
    stopRecording () {
      if (this.recording && this.recorder) {
        this.recorder.stop().then(({ blob }) => {
          this.uploadAudio(blob)
        })
        this.recording = false
        console.log('Recording stopped')
      }
    },
    uploadAudio (blob) {
      const formData = new FormData()
      formData.append('audio', blob, 'recording.wav')

      fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          console.log('Upload success:', data)
        })
        .catch(error => {
          console.error('Upload error:', error)
        })
    }
  }
}
</script>

<style scoped>
.meeting {
  display: flex;
  height: 100vh;
}

.video-container {
  flex: 3;
  display: flex;
  flex-wrap: wrap;
  padding: 10px;
  background-color: #2c3e50;
}

.video-stream {
  flex: 1 1 30%;
  background-color: #34495e;
  margin: 10px;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.5rem;
  height: 200px;
}

.controls {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center;
  gap: 10px;
}

.sidebar {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 10px;
  background-color: #ecf0f1;
}

.chat-window,
.participants {
  margin-bottom: 20px;
}

.chat-header,
.participants-header {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.chat-messages {
  height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.chat-message {
  margin-bottom: 5px;
}
</style>
