import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller  # Make sure this module is available
import app
from threading import Thread

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  

    reply("I am Jiva, how may I assist you?")

# Set Microphone parameters
def setup_microphone():
    with sr.Microphone() as source:
        r.energy_threshold = 500  # Adjust as per your environment
        r.dynamic_energy_threshold = False
        print("Microphone is ready to capture audio...")

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("Listening for command...")
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
            print("Recognized: ", voice_data)
        except sr.RequestError:
            reply('Sorry, my service is down. Please check your internet connection.')
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        return voice_data.lower()

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print("Processing: ", voice_data)
    # Handle both "jiva" and "jeeva" in command by removing both if present
    voice_data = voice_data.replace('jiva', '').replace('jeeva', '').strip()

    app.eel.addUserMsg(voice_data)

    if is_awake == False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Jiva!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        query = voice_data.split('search')[1].strip()
        reply(f'Searching for {query}')
        url = f'https://google.com/search?q={query}'
        try:
            webbrowser.get().open(url)
            reply('This is what I found, Sir.')
        except:
            reply('Please check your internet connection.')

    elif 'location' in voice_data:
        reply('Which place are you looking for?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = f'https://google.nl/maps/place/{temp_audio}/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found, Sir.')
        except:
            reply('Please check your internet connection.')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Goodbye, Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()

    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data or 'jeeva launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode == 1:
            reply('Gesture recognition is already active.')
        else:
            try:
                gc = Gesture_Controller.GestureController()  # Create an instance of GestureController
                t = Thread(target=gc.start)  # Start gesture recognition in a separate thread
                t.start()
                Gesture_Controller.GestureController.gc_mode = 1  # Set gc_mode to active
                reply('Gesture recognition launched successfully.')
            except Exception as e:
                print(f"Error launching gesture recognition: {e}")
                reply('Failed to launch gesture recognition.')

    elif 'stop gesture recognition' in voice_data or 'jeeva stop gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode == 1:
            Gesture_Controller.GestureController.gc_mode = 0  # Deactivate gesture recognition
            reply('Gesture recognition stopped.')
        else:
            reply('Gesture recognition is already inactive.')

    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied.')

    elif 'paste' in voice_data or 'page' in voice_data or 'pest' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted.')

    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            filestr += f"{counter}: {f}\n"
        file_exp_status = True
        reply('These are the files in your root directory:')
        app.ChatBot.addAppMsg(filestr)

    elif file_exp_status:
        counter = 0
        if 'open' in voice_data:
            file_index = int(voice_data.split(' ')[-1]) - 1
            if isfile(join(path, files[file_index])):
                os.startfile(path + files[file_index])
                file_exp_status = False
            else:
                try:
                    path = path + files[file_index] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += f"{counter}: {f}\n"
                    reply('Opened successfully.')
                    app.ChatBot.addAppMsg(filestr)
                except:
                    reply('You do not have permission to access this folder.')

        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory.')
            else:
                path = path.rsplit('//', 2)[0] + '//'
                files = listdir(path)
                for f in files:
                    counter += 1
                    filestr += f"{counter}: {f}\n"
                reply('OK.')
                app.ChatBot.addAppMsg(filestr)

    else:
        reply('I am not programmed to perform this action.')

# ------------------Driver Code--------------------

t1 = Thread(target=app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()

# Main loop for capturing and responding to voice commands
while True:
    voice_data = record_audio()

    if voice_data:
        # Process commands containing "jiva" or "jeeva"
        if 'jiva' in voice_data or 'jeeva' in voice_data:
            try:
                respond(voice_data)
            except SystemExit:
                reply("Exit successful.")
                break
            except Exception as e:
                print(f"Exception occurred: {e}")
                reply("An error occurred while processing the command.")