import os
import pyaudio
import time
import wave  # audio file format - .wav file
import speech_recognition as sr

from threading import Thread


class Record:
    def recording(self):
        chunk = 1024  # How many bytes
        format = pyaudio.paInt16  # 16 bit
        channels = 2
        rate = 40000  # Hz - the amount of samples per second
        record_seconds = 5

        file_num = 0
        while os.path.exists("audio-%s.wav" % file_num):
            file_num += 1
        self.wave_output_filename = ("audio-%s.wav" % file_num)

        pa = pyaudio.PyAudio()

        stream = pa.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )

        print("* RECORDING")

        frames = []

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print("* FINISHED")
        print("Saved to: ", self.wave_output_filename)

        stream.stop_stream()
        stream.close()
        pa.terminate()

        wf = wave.open(self.wave_output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def countdowwn(self, t):
        while t:
            mins, secs = divmod(t, 5)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1

    def speech_to_text(self):
        question = input(str("Do you want convert this to text? y/ N: "))

        if question == "y":
            r = sr.Recognizer()
            speech_to_text_filename = sr.AudioFile(self.wave_output_filename)
            with speech_to_text_filename as source:
                audio = r.record(source)

            file_num = 0
            while os.path.exists("text-%s.txt" % file_num):
                file_num += 1
            speech_to_text_filename = ("audio-%s.txt" % file_num)

            try:
                f = open(speech_to_text_filename, "w+")
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
