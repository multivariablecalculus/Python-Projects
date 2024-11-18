import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import subprocess
import math
import numpy
import tensorflow

# Initialize the speech recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Voice options using registry paths (modify these paths as per your system)
voice_options = {
    "male": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0",
    "female": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0",
    "robotic": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
}

# Function to set the voice based on voice ID
def set_voice(voice_id):
    try:
        engine.setProperty('voice', voice_options[voice_id])
    except KeyError:
        print(f"Voice ID '{voice_id}' not found in voice options.")

# Function to speak out text with optional voice selection
def speak(text, voice_id=None):
    # Format the text for console display (justified)
    formatted_text = f"Jarvis: {text.strip()}"
    try:
        print(formatted_text.ljust(80))  # Adjust the width (e.g., 80) as needed
    except UnicodeEncodeError:
        print(formatted_text.encode('ascii', 'ignore').decode('ascii'))

    # Write to a log file (UTF-8 encoding for wide character support)
    with open("jarvis_log.txt", "a", encoding='utf-8') as f:
        f.write(f"{formatted_text}\n")
    
    # Set voice if specified
    if voice_id:
        set_voice(voice_id)
    
    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Function to listen for commands and return the query
def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        print("\nRecognizing...")
        query = recognizer.recognize_google(audio).lower()  # Use Google Speech Recognition
        print(f"\nYou said: {query}")
        return query
    except sr.UnknownValueError:
        print("\nSorry, I didn't catch that. Please say that again.")
        return ""
    except sr.RequestError as e:
        print(f"\nSorry, I'm having trouble with accessing Google Speech Recognition: {e}")
        return ""

# Function for Jarvis to introduce himself
def introduce_jarvis():
    speak("Hello, I am Jarvis, your personal assistant. How can I assist you today?")

# Updated command handling to include more variations
def handle_command(query):
    if any(word in query for word in ["hello", "hi", "what's up", "sup"]):
        speak("\nHello! How can I assist you?")
    elif any(word in query for word in ["how are you", "how is life", "are you good", "you good"]):
        speak("\nI'm fine, thank you!")
    elif any(word in query for word in ["what's your name", "who are you", "what is your name"]):
        speak("\nI'm Jarvis, your personal assistant.")
    elif any(word in query for word in ["thank you", "thanks", "cheers"]):
        speak("\nYou're most welcome. I'm glad I could help.")
    elif "change voice" in query:
        speak("\nSure, which voice would you like me to use?")
        voice_query = listen().lower()
        if voice_query in voice_options:
            speak("\nChanging voice.", voice_query)
        else:
            speak("\nSorry, I didn't recognize that voice. Available options are male, female, or robotic.")
    elif any(word in query for word in ["time", "what's the time", "what is the time", "can you tell the time", "tell the time"]):
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"\nThe current time is {current_time}.")
    elif any(word in query for word in ["search", "search this", "search this for me", "look this up"]):
        speak("\nWhat do you want me to search for?")
        search_query = listen()
        if search_query:
            try:
                results = wikipedia.summary(search_query, sentences=2)
                speak(f"\nAccording to Wikipedia, {results}")
            except wikipedia.exceptions.DisambiguationError:
                speak(f"\nThere were multiple results for {search_query}. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak(f"\nSorry, I couldn't find any information on {search_query}.")
    elif "open website" in query:
        speak("\nWhich website do you want me to open?")
        website = listen()
        if website:
            url = f"https://www.{website.lower()}.com"
            webbrowser.open(url)
            speak(f"\nOpening {website} for you.")
    elif "open application" in query:
        speak("\nWhich application do you want me to open?")
        app_name = listen().lower()
        if "chrome" in app_name:
            subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe"])
            speak("\nOpening Google Chrome.")
        elif "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
            speak("\nOpening Notepad.")
        elif "visual studio" in app_name:
            subprocess.Popen(["C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/IDE/devenv.exe"])
            speak("\nOpening Visual Studio 2022.")
        elif "audacity" in app_name:
            subprocess.Popen(["C:/Program Files/Audacity/audacity.exe"])
            speak("\nOpening Audacity.")
        elif "adobe acrobat" in app_name:
            subprocess.Popen(["C:/Program Files/Adobe/Acrobat DC/Acrobat/Acrobat.exe"])
        elif "whatsapp" in app_name:
            subprocess.Popen("C:/Users/dipra/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Discord Inc")
        else:
            speak(f"\nSorry, I couldn't find {app_name} in my list of applications.")
    elif any(word in query for word in ["exit", "goodbye", "bye"]):
        speak("\nGoodbye!")
        exit()
    elif "calculate" in query or "solve" in query:
        speak("\nSure, what would you like me to calculate?")
        math_query = listen()
        if math_query:
            try:
                # Evaluate mathematical expressions
                result = eval(math_query)
                speak(f"\nThe result of {math_query} is {result}")
            except Exception as e:
                speak(f"\nSorry, I couldn't calculate that. Error: {str(e)}")
    elif "square root" in query:
        speak("\nSure, which number's square root would you like to calculate?")
        try:
            number = float(listen())
            if number >= 0:
                result = math.sqrt(number)
                speak(f"\nThe square root of {number} is {result}")
            else:
                speak("\nPlease provide a non-negative number for square root calculation.")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "cube root" in query:
        speak("\nSure, which number's cube root would you like to calculate?")
        try:
            number = float(listen())
            result = number ** (1 / 3)
            speak(f"\nThe cube root of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "cube of" in query:
        speak("\nSure, which number's cube would you like to calculate?")
        try:
            number = float(listen())
            result = number ** 3
            speak(f"\nThe cube of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "square of" in query:
        speak("\nSure, which number's square would you like to calculate?")
        try:
            number = float(listen())
            result = number ** 2
            speak(f"\nThe square of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "raise" in query or "to the power of" in query:
        speak("\nSure, please provide the base and the exponent.")
        try:
            base = float(listen())
            exponent = float(listen())
            result = base ** exponent
            speak(f"{base} raised to the power of {exponent} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say valid numbers for base and exponent.")
    elif "sum of" in query:
        speak("\nSure, please provide the numbers you want to sum up.")
        try:
            number1 = float(listen())
            number2 = float(listen())
            result = number1 + number2
            speak("\nThe sum of {} and {} is {}.".format(number1, number2, result))
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say valid numbers.")
    elif "subtract" in query or "difference" in query:
        speak("\nSure, please provide the numbers for subtraction.")
        try:
            number1 = float(listen())
            number2 = float(listen())
            result = number1 + number2
            speak("\nThe difference of {} and {} is {}.".format(number1, number2, result))
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say valid numbers.")
    elif "multiply" in query or "product of" in query:
        speak("\nSure, please provide the numbers for multiplication.")
        try:
            number1 = float(listen())
            number2 = float(listen())
            result = number1 + number2
            speak("\nThe product of {} and {} is {}.".format(number1, number2, result))
        except ValueError:
            speak("Sorry, I didn't catch that. Please say valid numbers.")
    elif "divide" in query or "division" in query:
        speak("\nSure, please provide the dividend and divisor.")
        try:
            dividend = float(listen())
            divisor = float(listen())
            result = dividend / divisor
            speak(f"\nThe result of {dividend} divided by {divisor} is {result}")
        except ZeroDivisionError:
            speak("\nDivision by zero is not allowed.")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say valid numbers.")
    elif "absolute value" in query or "absolute" in query:
        speak("\nSure, which number would you like the absolute value of?")
        try:
            number = float(listen())
            result = abs(number)
            speak(f"\nThe absolute value of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "factorial of" in query or "factorial" in query:
        speak("\nSure, which number's factorial would you like to calculate?")
        try:
            number = int(listen())
            result = math.factorial(number)
            speak(f"\nThe factorial of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid integer number.")
    elif "logarithm" in query:
        speak("\nSure, please provide the number and base for logarithm.")
        try:
            number = float(listen())
            base = float(listen())
            result = math.log(number, base)
            speak(f"\nThe logarithm of {number} with base {base} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say valid numbers for logarithm.")
    elif "common log" in query:
        speak("\nSure, which number's common logarithm would you like to calculate?")
        try:
            number = float(listen())
            result = math.log10(number)
            speak(f"\nThe common logarithm of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif  "natural log" in query:
        speak("\nSure, which number's natural logarithm would you like to calculate?")
        try:
            number = float(listen())
            result = math.log(number)
            speak(f"\nThe natural logarithm of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "lower estimate" in query:
        speak("\nSure, please provide the number for which you want the lower estimate.")
        try:
            number = float(listen())
            result = math.floor(number)
            speak(f"\nThe lower estimate of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "higher estimate" in query:
        speak("\nSure, please provide the number for which you want the higher estimate.")
        try:
            number = float(listen())
            result = math.ceil(number)
            speak(f"\nThe higher estimate of {number} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say a valid number.")
    elif "exponential function" in query or "exponentiate" in query:
        speak("\nSure, please provide the base and exponent for exponential function.")
        try:
            base = float(listen())
            exponent = float(listen())
            result = base ** exponent
            speak(f"{base} raised to the power of {exponent} is {result}")
        except ValueError:
            speak("\nSorry, I didn't catch that. Please say valid numbers for base and exponent.")
    else:
        speak("\nI'm sorry, I didn't understand that command.")

# Main function to run the voice assistant
if __name__ == "__main__":
    introduce_jarvis()
    
    while True:
        query = listen().strip()
        if query:
            handle_command(query)
