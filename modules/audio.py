import pyaudio
import wave
import time
from pynput import keyboard

class Audio:
    def __init__(self, audio_path: str):
        self.paused = False
        # '.\\src\\carmen-bizet.wav'
        self.wf = wave.open(audio_path, 'rb')

        # instantiate PyAudio
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        stream_callback=self.callback)

        self.stream.start_stream()

        while self.stream.is_active() or paused==True:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
            time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()

        # close PyAudio
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        print(in_data, frame_count, time_info, status)
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def on_press(self, key) -> False:
        print (key)
        if key == keyboard.Key.space:
            if self.stream.is_stopped():     # time to play audio
                print ('play pressed')
                self.stream.start_stream()
                self.paused = False
                return False
            elif self.stream.is_active():   # time to pause audio
                print ('pause pressed')
                self.stream.stop_stream()
                self.paused = True
                return False
        return False