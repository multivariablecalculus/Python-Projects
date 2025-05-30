#Still WIP. does not use realtime ML and NLP... this is a disappointment tbh

import datetime
import webbrowser
import psutil
from transformers import pipeline
import wolframalpha
import wikipediaapi
import re
import requests
import numpy as np
import tensorflow as tf
from keras.api.models import Sequential
from keras.api.layers import Dense, LSTM

#This is for RPS (the only part using hardcore NNs
moves = ['rock', 'paper', 'scissors']
mov_num = {move: i for i, move in enumerate(moves)}
num_move = {i: move for move, i in mov_num.items()}


np.random.seed(0)
data_sz = 10000
seq_len = 3

sequences = []
nx_mov = []

for _ in range(data_sz):
    sequence = np.random.choice(moves, size=seq_len)
    sequences.append([mov_num[move] for move in sequence])
    nx_mov.append(mov_num[np.random.choice(moves)])

X = np.array(sequences)
y = np.array(nx_mov)

model = Sequential([
    LSTM(10, input_shape=(seq_len, 1)), 
    Dense(3, activation='softmax') 
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

X = np.reshape(X, (X.shape[0], seq_len, 1))

model.fit(X, y, epochs=10, batch_size=32, verbose=1)

#Weather client
api_key = "an api key maybe?" #use openweatherapi

#NLP approach
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

#WFA client
wolfram_client = wolframalpha.Client('an API key pls')

#MS client
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,  #better form
    user_agent='Jarvis AI Chatbot/1.0'  #identifier
)

def response(query):
    response = chatbot(query, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

def pred_mov(prev_mov):
    in_seq = np.array([[mov_num[move]] for move in prev_mov])
    
    if len(in_seq) < seq_len:
        in_seq = np.pad(in_seq, ((seq_len - len(in_seq), 0), (0, 0)), 'constant')
    else:
        in_seq = in_seq[-seq_len:]

    in_seq = np.reshape(in_seq, (1, seq_len, 1))

    probs = model.predict(in_seq)[0]
    pred_movs = num_move[np.argmax(probs)]
    return pred_movs

def play_game():
    print("\nJarvis: Welcome to Rock-Paper-Scissors against AI!")
    print("          You can choose rock, paper, or scissors. To quit, type 'quit'.")
    
    prev_mov = []
    
    while True:
        us_mov = input("          Enter your move (rock/paper/scissors): ").lower()
        
        if us_mov == 'quit':
            print("          Exiting the game.")
            break
        
        if us_mov not in moves:
            print("          Invalid move. Please enter rock, paper, or scissors.")
            continue
        
        prev_mov.append(us_mov)
        
        if len(prev_mov) > seq_len:
            prev_mov = prev_mov[-seq_len:]
        
        ai_move = pred_mov(prev_mov)
        
        print(f"          You chose: {us_mov}")
        print(f"          AI chose: {ai_move}")
        
        winner =  winner(us_mov, ai_move)
        if winner == 'user':
            print("          You win!") #yay
        elif winner == 'ai':
            print("          AI wins!") #boo
        else:
            print("          It's a tie!") #not good, not terrible (there's a reference)
        
        print("---------------------------")

def winner(us_mov, ai_move):
    if us_mov == ai_move:
        return 'tie'
    elif (us_mov == 'rock' and ai_move == 'scissors') or \
         (us_mov == 'paper' and ai_move == 'rock') or \
         (us_mov == 'scissors' and ai_move == 'paper'):
        return 'user'
    else:
        return 'ai'

def gt_tm():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def gt_dt():
    today = datetime.datetime.now()
    return today.strftime("%d/%m/%Y")

def op_app(app_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.terminate()
            proc.wait()
            break
    webbrowser.open(app_name)

def op_web(url):
    webbrowser.open("{}".format(url))

def sh_google(search):
    webbrowser.open("https://www.google.com/search?q={}".format(search))

def calc_wfa(query):
    try:
        res = wolfram_client.query(query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return "\nJarvis: I'm sorry, I couldn't calculate that."

def sh_wiki(query):
    page = wiki_wiki.page(query)
    if page.exists(): 
        return page.summary[:3000]  #Summary upto 2000 chars.
    else:
        return "\nJarvis: I couldn't find information on that topic."

def gt_wth(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather = data['weather'][0]
        
        print(f"      Location: {city}")
        print(f"      Temperature: {main['temp']}\u00B0C")
        print(f"      Humidity: {main['humidity']}%")
        print(f"      Pressure: {main['pressure']} hPa")
        print(f"      Weather: {weather['description'].capitalize()}")
        print(f"      Wind Speed: {wind['speed']} m/s")
    else:
        print("       Error fetching weather data. Please check the city name or API key.")

#My least favourite (loop)
if __name__ == "__main__":
    print("\nJarvis: Hello! I am Jarvis, an AI chatbot developed by Abhradeep Roy. How can I assist you today?".rjust(30))
    while True:
        query = input("\nYou: ").lower()
        if any(word in query for word in ["exit", "goodbye", "bye", "good day", "bye bye", "ta ta"]):
            print("\nJarvis: Goodbye!".rjust(30))
            break
        elif query:
            if vulgar(query):
                print("\nJarvis: Sir/Madam, I am an AI, not a mirror. :)".rjust(30))
            elif any(word in query for word in ["what's your name?", "what's your name", "what is your name?", "what is your name", "name yourself.", "name yourself", "introduce yourself.", "introduce yourself"]):
                print("\nMy name is Jarvis, I am an AI Assistant.")
            elif any(word in query for word in ["how are you?", "how are you", "you good?", "you good", "sup?", "sup", "whats up?", "what's up?", "whats up", "what's up"]):
                print("I am fine! Thank you for asking.")
            elif "time" in query:
                time = gt_tm()
                print(f"\nJarvis: The time is {time}".rjust(30))
            elif "date" in query:
                date = gt_dt()
                print(f"\nJarvis: Today's date is {date}".rjust(30))
            elif "website" in query:
                website = query.split("website")[-1].strip()
                op_web(website)
                print(f"\nJarvis: Opening {website}".rjust(30))
            elif "application" in query:
                app = query.split("application")[-1].strip()
                op_app(app)
                print(f"\nJarvis: Opening {app}".rjust(30))
            elif "calculate" in query or "what is" in query:
                answer = calc_wfa(query)
                print(f"\nJarvis: {answer}".rjust(30))
            elif "search" in query:
                topic = query.split("search")[-1].strip()
                result = sh_wiki(topic)
                print(f"\nJarvis: {result}".rjust(30))
            elif "google" in query:
                search = query.split("google")[-1].strip()
                sh_google(search)
            elif "weather" in query:
                city = input("   Please enter the location: ")
                gt_wth(city, api_key)
            elif "game" in query:
                print("\nJarvis: Actually, the games are WIP, so let's just play Rock-Paper-Scissors. PLease Wait.")
                play_game()
            else:
                response = response(query)
                print(f"\nJarvis: {response}".rjust(30))
