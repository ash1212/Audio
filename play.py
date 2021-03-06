import pyaudio
import wave
import time


file_name = input("Enter the file name: ")

wf = wave.open(file_name, 'rb')

pa = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return data, pyaudio.paContinue


stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(),
                 rate=wf.getframerate(),
                 output=True,
                 stream_callback=callback)

print("Playing ", file_name)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

print("Finished")

pa.terminate()
