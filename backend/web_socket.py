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
recognizer = KaldiRecognizer(model, 16000)
# WAV file parameters
# WAVE_OUTPUT_FILENAME = "output.wav"
# CHANNELS = 1
# SAMPLE_WIDTH = 2  # 16位 = 2字节
# FRAME_RATE = 16000  # 采样率为 16000Hz


# WebSocket server handler
async def recognize(websocket, path):
    print(f"Client connected: {websocket.remote_address}")
    text_all = ""
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
            break

# Start the WebSocket server
async def main():
    server = await websockets.serve(recognize, "localhost", 5000)
    print("WebSocket server started on http://localhost:5000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
