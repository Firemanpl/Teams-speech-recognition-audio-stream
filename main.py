from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import speech_recognition as sr
import pygame
import json
import random
import time
from datetime import datetime


class Audio:
    def detect_END_music(self):
        global lock
        pygame.init()
        for event in pygame.event.get():
            if event.type == SONG_END:
                print("the song ended!")
                mic_btn = driver.find_element_by_id("microphone-button")
                mic_btn.send_keys(Keys.CONTROL+Keys.SHIFT+"M")
                print('DEBUG: Mic Turned off')
                lock = False



    def turnOn_mic(self):
        global lock
        mic_btn = driver.find_element_by_id("microphone-button")
        mic_btn.send_keys(Keys.CONTROL+Keys.SHIFT+"M")
        print('DEBUG: Mic Turned on')
        lock = True

    def voice_speech(self):
        global SONG_END
        SONG_END = pygame.USEREVENT + 1
        random_track = config['your_voice']
        pygame.init()
        pygame.mixer.music.load(random.choice(random_track))
        # pygame.mixer.music.set_volume(0.8)
        print("Ansewer_sound=true")
        pygame.mixer.music.play(0, 0.0)
        pygame.mixer.music.set_endevent(SONG_END)

    def listen_speech(self):
        words = config['trigger_words']
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Recognizing: ')
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=3)
            # audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language=config['language'])
                print('You said: {}'.format(text))
                for word in words:
                    if word in text:
                        print("EXEC WORD:{}".format(word))
                        # turn on mic
                        Audio.turnOn_mic()
                        # Voice recognize
                        Audio.voice_speech()
                        while lock is True:
                            # detect turned mic off
                            Audio.detect_END_music()
                        break
            except sr.UnknownValueError:
                print('--------')
            except sr.RequestError as e:
                print("Error request!!!")
            except Exception:
                print("Except error")


class Teams:
    def get_meeting_members(self):
        meeting_elems = driver.find_elements_by_css_selector(".one-call")
        for meeting_elem in meeting_elems:
            try:
                meeting_elem.click()
                break
            except:
                continue


    def join_meeting(self):
        team_name = config['teamname']
        print(team_name)
        team_css_selector = "div[data-tid='team-{}-li']".format(team_name)
        teams_page = wait_until_found(team_css_selector, 60 * 5)
        if teams_page is not None:
            print('DEBUG: Clicked Team Name')
            teams_page.click()
        # click join button
        join_btn = wait_until_found(f"span[ng-if='!ctrl.roundButton']", 30)
        while join_btn is None:
            join_btn = driver.find_element_by_css_selector(f"span[ng-if='!ctrl.roundButton']")
            print('DEBUG: Join button not found')
            time.sleep(3)

        join_btn.click()
        print('DEBUG: Join Button Clicked')
        time.sleep(1)
        # turn camera off
        video_btn = driver.find_element_by_css_selector("toggle-button[data-tid='toggle-video']>div>button")
        video_is_on = video_btn.get_attribute("aria-pressed")
        if video_is_on == "true":
            print('DEBUG: Video Turned Off')
            video_btn.click()

        # turn mic off
        audio_btn = driver.find_element_by_css_selector("toggle-button[data-tid='toggle-mute']>div>button")
        audio_is_on = audio_btn.get_attribute("aria-pressed")
        if audio_is_on == "true":
            print('DEBUG: Audio Turned Off')
            audio_btn.click()

        # final join button
        join_now_btn = wait_until_found("button[data-tid='prejoin-join-button']", 30)
        if join_now_btn is None:
            print('DEBUG: Join now button not found')
            return
        join_now_btn.click()
    def leave(self):
        if current_members < config['current_members_is_less_than']:
            print('DEBUG: Exiting Meeting...')
            hangup_btn = driver.find_element_by_css_selector("button[id='hangup-button']")
            hangup_btn.click()
            print('DEBUG: Exited')
            exit()

    def login(self):
        if config['email'] != "" and config['password'] != "":
            print('Email and Password found in config.json!')

            login_email = wait_until_found("input[type='email']", 30)
            if login_email is not None:
                login_email.send_keys(config['email'])
                time.sleep(1)

            # find the element again to avoid StaleElementReferenceException
            login_email = wait_until_found("input[type='email']", 5)
            if login_email is not None:
                login_email.send_keys(Keys.ENTER)

            login_pwd = wait_until_found("input[type='password']", 5)
            if login_pwd is not None:
                login_pwd.send_keys(config['password'])
                time.sleep(1)

            # find the element again to avoid StaleElementReferenceException
            login_pwd = wait_until_found("input[type='password']", 5)
            if login_pwd is not None:
                login_pwd.send_keys(Keys.ENTER)

            # stay signed in
            keep_logged_in = wait_until_found("input[id='idBtn_Back']", 5)
            if keep_logged_in is not None:
                keep_logged_in.click()

            # use web app instead
            use_web_instead = wait_until_found("a.use-app-lnk", 5)
            if use_web_instead is not None:
                use_web_instead.click()


def load_config():
    global config
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)


def wait_until_found(sel, timeout):
    try:
        element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, sel))
        WebDriverWait(driver, timeout).until(element_present)
        return driver.find_element_by_css_selector(sel)
    except exceptions.TimeoutException:
        print("Timeout waiting for element.")
        return None


def main():
    global config, driver, current_members
    load_config()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    driver.get("https://teams.microsoft.com")
    Teams.login()

    # make sure to have list mode configuration in ms teams
    jointime = config['meetingtime']
    current_time = 0
    while current_time != jointime:
        now = datetime.now()
        current_time = now.strftime(f"%H:%M")
        print("Actual time:", current_time, "Time join:", jointime)
        time.sleep(10)
    Teams.join_meeting()
    while True:
        Audio.listen_speech()
        current_members = Teams.get_meeting_members()
        print("Current members:", current_members)
        if current_members is not None:
            Teams.leave()


if __name__ == "__main__":
    Audio = Audio()
    Teams = Teams()
    main()
