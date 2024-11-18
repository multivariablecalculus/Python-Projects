#Still WIP.
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

#This is for Rock-Paper-Scissors.
moves = ['rock', 'paper', 'scissors']
move_to_num = {move: i for i, move in enumerate(moves)}
num_to_move = {i: move for move, i in move_to_num.items()}


np.random.seed(0)
data_size = 10000
sequence_length = 3

sequences = []
next_moves = []

for _ in range(data_size):
    sequence = np.random.choice(moves, size=sequence_length)
    sequences.append([move_to_num[move] for move in sequence])
    next_moves.append(move_to_num[np.random.choice(moves)])

X = np.array(sequences)
y = np.array(next_moves)

model = Sequential([
    LSTM(10, input_shape=(sequence_length, 1)), 
    Dense(3, activation='softmax') 
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

X = np.reshape(X, (X.shape[0], sequence_length, 1))

model.fit(X, y, epochs=10, batch_size=32, verbose=1)

#Loading Weather cient.
api_key = "0a82367a29f4061ad1ca1da8a2c54336"

#NLP for normal conversation.
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

#Initializing WolframAlpha client.
wolfram_client = wolframalpha.Client('7Q76TP-X2QQ9AG652')

#Initializing Microsoft Client.
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,  #WIKI for better format.
    user_agent='Jarvis AI Chatbot/1.0'  #Agent Identifier.
)

def get_response(query):
    response = chatbot(query, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

def predict_next_move(previous_moves):
    input_sequence = np.array([[move_to_num[move]] for move in previous_moves])
    
    if len(input_sequence) < sequence_length:
        input_sequence = np.pad(input_sequence, ((sequence_length - len(input_sequence), 0), (0, 0)), 'constant')
    else:
        input_sequence = input_sequence[-sequence_length:]

    input_sequence = np.reshape(input_sequence, (1, sequence_length, 1))

    probabilities = model.predict(input_sequence)[0]
    predicted_move = num_to_move[np.argmax(probabilities)]
    return predicted_move

def play_game():
    print("\nJarvis: Welcome to Rock-Paper-Scissors against AI!")
    print("          You can choose rock, paper, or scissors. To quit, type 'quit'.")
    
    previous_moves = []
    
    while True:
        user_move = input("          Enter your move (rock/paper/scissors): ").lower()
        
        if user_move == 'quit':
            print("          Exiting the game.")
            break
        
        if user_move not in moves:
            print("          Invalid move. Please enter rock, paper, or scissors.")
            continue
        
        previous_moves.append(user_move)
        
        if len(previous_moves) > sequence_length:
            previous_moves = previous_moves[-sequence_length:]
        
        ai_move = predict_next_move(previous_moves)
        
        print(f"          You chose: {user_move}")
        print(f"          AI chose: {ai_move}")
        
        winner =  winner(user_move, ai_move)
        if winner == 'user':
            print("          You win!")
        elif winner == 'ai':
            print("          AI wins!")
        else:
            print("          It's a tie!")
        
        print("---------------------------")

def winner(user_move, ai_move):
    if user_move == ai_move:
        return 'tie'
    elif (user_move == 'rock' and ai_move == 'scissors') or \
         (user_move == 'paper' and ai_move == 'rock') or \
         (user_move == 'scissors' and ai_move == 'paper'):
        return 'user'
    else:
        return 'ai'

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def get_date():
    today = datetime.datetime.now()
    return today.strftime("%d/%m/%Y")

def open_application(app_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.terminate()
            proc.wait()
            break
    webbrowser.open(app_name)

def open_website(url):
    webbrowser.open("{}".format(url))

def search_google(search):
    webbrowser.open("https://www.google.com/search?q={}".format(search))

def calculate_wolframalpha(query):
    try:
        res = wolfram_client.query(query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return "\nJarvis: I'm sorry, I couldn't calculate that."

def search_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists(): 
        return page.summary[:3000]  #Summary upto 2000 chars.
    else:
        return "\nJarvis: I couldn't find information on that topic."

def vulgar(text):
    # Define a list of vulgar words or use a more comprehensive filter
    vulgar_words = ["fuck you", "fuck off", "fuck", "bitch", "fuck yourself", "bitchass", "dumbass", "dogshit", "asshole", "jerk", "jerkass", "motherfucker", "mf", "nigga", "nigger", "niga", "niger", "bastard"]  # Add more words as needed
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, vulgar_words)))
    if re.search(pattern, text, re.IGNORECASE):
        return True
    return False

def get_weather(city, api_key):
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

# Main loop
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
                time = get_time()
                print(f"\nJarvis: The time is {time}".rjust(30))
            elif "date" in query:
                date = get_date()
                print(f"\nJarvis: Today's date is {date}".rjust(30))
            elif "website" in query:
                website = query.split("website")[-1].strip()
                open_website(website)
                print(f"\nJarvis: Opening {website}".rjust(30))
            elif "application" in query:
                app = query.split("application")[-1].strip()
                open_application(app)
                print(f"\nJarvis: Opening {app}".rjust(30))
            elif "calculate" in query or "what is" in query:
                answer = calculate_wolframalpha(query)
                print(f"\nJarvis: {answer}".rjust(30))
            elif "search" in query:
                topic = query.split("search")[-1].strip()
                result = search_wikipedia(topic)
                print(f"\nJarvis: {result}".rjust(30))
            elif "google" in query:
                search = query.split("google")[-1].strip()
                search_google(search)
            elif "weather" in query:
                city = input("   Please enter the location: ")
                get_weather(city, api_key)
            elif "game" in query:
                print("\nJarvis: Actually, the games are WIP, so let's just play Rock-Paper-Scissors. PLease Wait.")
                play_game()
            else:
                response = get_response(query)
                print(f"\nJarvis: {response}".rjust(30))
