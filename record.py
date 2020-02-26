import os
import pyaudio
import time
import wave
import speech_recognition as sr

from threading import Thread


class Record:
    def recording(self):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 2
        rate = 40000
        record_seconds = 5

        file_num = 0
        while os.path.exists(f"audio-{file_num}"):
            file_num += 1
        self.wave_output_filename = f"audio-{file_num}"

        pa = pyaudio.PyAudio()

        print("* RECORDING")

        stream = pa.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )

        frames = []

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        pa.terminate()

        print("* FINISHED")
        print("Saved to: ", self.wave_output_filename)

        wf = wave.open(self.wave_output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def countdowwn(self, t):
        while t:
            mins, secs = divmod(t, 5)
            timeformat = "{:02d}:{:02d}".format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1

    def speech_to_text(self):
        question = input("Do you want convert this to text? y/ N: ")

        if question == "y":
            r = sr.Recognizer()
            speech_to_text_filename = sr.AudioFile("audio-0.wav")
            with speech_to_text_filename as source:
                audio = r.record(source)

            file_num = 0
            while os.path.exists("text-%s.txt" % file_num):
                file_num += 1
            speech_to_text_filename = ("text-%s.txt" % file_num)

            try:
                with open(speech_to_text_filename, "w") as f:
                    f.write(r.recognize_google(audio))

                print("Text save to: ", speech_to_text_filename)
            except:
                print("No input recognised")


if __name__ == "__main__":
    t1 = Record()
    Thread(target=t1.recording).start()
    Thread(target=t1.countdowwn(5)).start()
    time.sleep(1)
    t1.speech_to_text()
