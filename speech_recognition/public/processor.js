class MyProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.accumulatedData = [];
    this.sampleRate = 16000; // 采样率为 16000Hz
    this.chunkSize = this.sampleRate * 0.5; // 每 0.5 秒发送一次数据块
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (input && input.length > 1) {
      const inputDataL = input[0]; // 左声道数据
      const inputDataR = input[1]; // 右声道数据
      const pcmData = new Int16Array(inputDataL.length);

      for (let i = 0; i < inputDataL.length; i++) {
        const monoData = (inputDataL[i] + inputDataR[i]) / 2;
        pcmData[i] = Math.min(1, Math.max(-1, monoData)) * 0x7fff;
      }

      this.accumulatedData.push(...pcmData);

      // 当累积的数据达到设定的块大小时，发送到主线程
      if (this.accumulatedData.length >= this.chunkSize) {
        const chunk = new Int16Array(this.accumulatedData);
        this.port.postMessage(chunk.buffer); // 发送数据到主线程
        this.accumulatedData = []; // 清空已发送的数据
      }
    } else if (input && input.length > 0) {
      // 处理单声道输入的情况
      const inputData = input[0];
      const pcmData = new Int16Array(inputData.length);

      for (let i = 0; i < inputData.length; i++) {
        pcmData[i] = Math.min(1, Math.max(-1, inputData[i])) * 0x7fff;
      }

      this.accumulatedData.push(...pcmData);

      // 当累积的数据达到设定的块大小时，发送到主线程
      if (this.accumulatedData.length >= this.chunkSize) {
        const chunk = new Int16Array(this.accumulatedData);
        this.port.postMessage(chunk.buffer); // 发送数据到主线程
        this.accumulatedData = []; // 清空已发送的数据
      }
    }

    return true;
  }
}

registerProcessor("my-processor", MyProcessor);
