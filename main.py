from pygame import mixer
import speech_recognition as sr
import time
import pyaudio
words = ["Kamilu", "stróżek", "Kamil", "kamień", "stróżyk", "Stróżyk", "Suszek"]

class Audio:
    def voice_speech(self):
        mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
        mixer.music.load("alert.wav")
        print("Ansewer_sound=true")
        mixer.music.play(0, 0.0)
        time.sleep(1)
        mixer.music.stop()
def capture():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK,input_device_index=2)
    data = stream.read(CHUNK)
    frames = []
    frames.append(data)

def listen_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Powiedz coś: ')
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio,language="pl-PL")
            print('You said: {}'.format(text))
            for word in words:
                if word in text:
                    print("EXEC WORD:{}".format(word))
                    play.voice_speech()
                    break
        except sr.UnknownValueError:
            print('--------')
        except sr.RequestError as e:
            print("Error request!!!")
        except Exception:
            print("Except error")
play = Audio()
capture()
while True:
    listen_speech()





