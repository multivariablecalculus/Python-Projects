import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import subprocess
import math
import numpy
import tensorflow  #da goat maybe?

# recog engine
recognizer = sr.Recognizer()
jarvis_voice = pyttsx3.init()

# Voice reg keys
voices = {
    "male": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0",
    "female": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0",
    "robotic": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
}

# probably will customize this
def pick_voice(option):
    try:
        jarvis_voice.setProperty('voice', voices[option])
    except KeyError:
        print(f"Voice '{option}' not found.")

#Output
def say(text, mode=None):
    prefix = f"Jarvis: {text.strip()}"
    
    #Display fail safe
    try:
        print(prefix.ljust(80))
    except UnicodeEncodeError:
        print(prefix.encode('ascii', 'ignore').decode('ascii'))

    #Save output
    with open("jarvis_log.txt", "a", encoding='utf-8') as log_file:
        log_file.write(f"{prefix}\n")

    if mode:
        pick_voice(mode)
    
    jarvis_voice.say(text)
    jarvis_voice.runAndWait()

# listening
def hear():
    with sr.Microphone() as mic:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(mic)
        audio = recognizer.listen(mic)

    try:
        print("\nProcessing...")
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        print("\nDidn't catch that, sorry.")
    except sr.RequestError as err:
        print(f"\nSpeech recognition service failed: {err}")
    
    return ""

def greet_user():
    say("Hi! I'm Jarvis. What can I do for you today?")

def pr_cmd(cmd):
    if any(phrase in cmd for phrase in ["hello", "hi", "hey"]):
        say("Hey there! What can I help with?")
    elif "how are you" in cmd:
        say("Doing great, thanks for asking.")
    elif "your name" in cmd:
        say("I'm Jarvis—your slightly quirky assistant.")
    elif "thanks" in cmd:
        say("No problem at all.")
    elif "change voice" in cmd:
        say("Sure—male, female, or robotic?")
        voice_choice = hear()
        if voice_choice in voices:
            say("Got it. Changing voice now.", voice_choice)
        else:
            say("Oops, I don't know that voice option.")
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%H:%M")
        say(f"The time is {now}.")
    elif "search" in cmd:
        say("What should I search for?")
        term = hear()
        if term:
            try:
                summary = wikipedia.summary(term, sentences=2) #pls dont ask for sus stuff, u can tho
                say(f"Here's what I found: {summary}")
            except wikipedia.exceptions.DisambiguationError:
                say("Too many results—could you be more specific?")
            except wikipedia.exceptions.PageError:
                say("I couldn’t find anything relevant.")
    elif "open website" in cmd:
        say("Which site?")
        site = hear()
        if site:
            webbrowser.open(f"https://{site}.com")
            say(f"Opening {site}")
    elif "open application" in cmd:
        say("Which app?")
        app = hear()
        if "chrome" in app:
            subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe"])
            say("Launching Chrome.")
        elif "notepad" in app:
            subprocess.Popen(["notepad.exe"])
            say("Here's Notepad.")
        elif "visual studio" in app:
            subprocess.Popen(["C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/IDE/devenv.exe"])
            say("Opening Visual Studio.")
        else:
            say(f"I couldn't find the app: {app}")
    elif "exit" in cmd or "bye" in cmd:
        say("Catch you later!")
        exit()
    elif "calculate" in cmd or "solve" in cmd:
        say("Sure. What's the equation?")
        expr = hear()
        try:
            result = eval(expr)
            say(f"The result is {result}")
        except:
            say("Something went wrong with the calculation.")
    elif "square root" in cmd:
        say("Which number?")
        try:
            num = float(hear())
            say(f"The square root of {num} is {math.sqrt(num)}")
        except:
            say("Didn't quite get the number.")
    elif "cube root" in cmd:
        say("Which number?")
        try:
            num = float(hear())
            say(f"Cube root of {num} is {num ** (1/3)}")
        except:
            say("Say that number again?")
    elif "square of" in cmd:
        say("Which number?")
        try:
            num = float(hear())
            say(f"{num} squared is {num**2}")
        except:
            say("Didn't catch that.")
    elif "cube of" in cmd:
        say("Number?")
        try:
            num = float(hear())
            say(f"{num} cubed is {num**3}")
        except:
            say("Hmm, that input was unclear.")
    elif "factorial" in cmd:
        say("Give me an integer.")
        try:
            num = int(hear())
            say(f"{num}! is {math.factorial(num)}")
        except:
            say("Make sure to give me a whole number.")
    elif "divide" in cmd:
        say("Give me two numbers.")
        try:
            a = float(hear())
            b = float(hear())
            if b == 0:
                say("Can't divide by zero.")
            else:
                say(f"{a} divided by {b} is {a/b}")
        except:
            say("Hmm, that was tricky to understand.")
    else:
        say("I don’t have a response for that yet.")

# disgusting
if __name__ == "__main__":
    greet_user()
    while True:
        cmd = hear().strip()
        if cmd:
            pr_cmd(cmd)
