import os
import asyncio
import json
import websockets
from vosk import Model, KaldiRecognizer, SpkModel,SetLogLevel
import numpy as np
import wave
# Load Vosk model
model_path = "vosk-model-cn-0.22"
if not os.path.exists(model_path):
    raise FileNotFoundError("Please download the Vosk model and place it in the 'vosk_model/model' directory.")
SetLogLevel(-1)
model = Model(model_path)
# 加载说话人识别模型
spk_model = SpkModel("vosk-model-spk-0.4")  # 替换为说话人识别模型路径
recognizer = KaldiRecognizer(model, 16000)
recognizer.SetSpkModel(spk_model)


speaker_list = []
id = 1
threshold = 0.49
# 计算两个向量的余弦距离，距离越小说明两个向量越相似
def cosine_dist(x, y):
    nx = np.array(x)
    ny = np.array(y)
    return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

def check_speaker(vector):
    global id
    for index, item in enumerate(speaker_list):
        dist = cosine_dist(vector, item)
        print(dist)
        if dist < threshold:
            id = index + 1
            return
    speaker_list.append(vector)
    id = len(speaker_list)



# WebSocket server handler
async def recognize(websocket, path):
    print(f"Client connected: {websocket.remote_address}")
    text_all = ""
    global speaker_list, id
    # Open a WAV file to save the audio
    # with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    #     wf.setnchannels(CHANNELS)
    #     wf.setsampwidth(SAMPLE_WIDTH)
    #     wf.setframerate(FRAME_RATE)
    while True:
        try:
            audio_data = await websocket.recv()
            # Save the audio data to the WAV file
            # wf.writeframes(audio_data)
            if recognizer.AcceptWaveform(audio_data):
                final_result = json.loads(recognizer.Result())
                if final_result['text'] != "":
                    final_result['text'] = final_result['text'].replace(' ', '')
                    text_all += final_result['text']
                    check_speaker(final_result['spk'])
                    final_result['spk'] = id
                    await websocket.send(json.dumps(final_result))
            else:
                partial_result = json.loads(recognizer.PartialResult())
                if partial_result['partial'] != "":
                    partial_result['partial'] = partial_result['partial'].replace(' ', '')
                    await websocket.send(json.dumps(partial_result))
        except websockets.ConnectionClosedOK:
            print(f"Client disconnected: {websocket.remote_address}")
            with open("output.txt", "a", encoding="utf-8") as f:
                f.write(text_all + "\n")
            recognizer.Reset()
            speaker_list = []
            id = 1
            break

# Start the WebSocket server
async def main():
    server = await websockets.serve(recognize, "localhost", 5000)
    print("WebSocket server started on http://localhost:5000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
