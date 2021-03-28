from pygame import mixer
import speech_recognition as sr
import time
import pyaudio
words = ["Kamilu", "stróżek", "Kamil", "kamień", "stróżyk", "Stróżyk", "Suszek"]

class Audio:
    def voice_speech(self):
        mixer.init()
        mixer.music.load("alert.wav")
        print("Ansewer_sound=true")
        mixer.music.play(0, 0.0)
        time.sleep(1)
        mixer.music.stop()



def listen_speech():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print('Recognizing: ')
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
while True:
    listen_speech()





