import speech_recognition as sr
import pyttsx3
import os
import json
import pyjokes
import wikipedia
import requests
from bs4 import BeautifulSoup

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

# Function to save new command and response to a file
def save_command(command, response):
    data = {}
    try:
        with open("learned_commands.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    data[command] = response

    with open("learned_commands.json", "w") as file:
        json.dump(data, file, indent=4)

    speak(f"I've learned how to respond to '{command}'.")

# Function to check if a command has been learned
def check_learned_command(command):
    try:
        with open("learned_commands.json", "r") as file:
            data = json.load(file)
        if command in data:
            speak(data[command])
            return True
    except FileNotFoundError:
        pass
    return False

# Function to execute basic commands
def execute_command(command):
    if check_learned_command(command):
        return
    elif "learn" in command:
        speak("What should I learn?")
        new_command = listen()
        speak(f"What should I respond when you say '{new_command}'?")
        response = listen()
        save_command(new_command, response)
    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad")
    elif "play music" in command:
        speak("Playing music.")
        os.system("start path_to_your_music.mp3")  # Replace with your music path
    elif "tell me a joke" in command:
        tell_joke()
    elif "help me with" in command:
        topic = command.replace("help me with", "").strip()
        get_subject_help(topic)
    elif "summarize" in command or "search for" in command:
        query = command.replace("summarize", "").replace("search for", "").strip()
        google_search_summary(query)
    elif "shutdown" in command:
        speak("Shutting down.")
        os.system("shutdown /s /t 1")
    elif "stop" in command or "bye" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I don't know that yet. You can teach me by saying 'learn'.")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to get a subject summary from Wikipedia
def get_subject_help(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(f"Here’s a brief summary on {topic}: {summary}")
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any information on that topic.")

# Function to search and summarize using Google Search
def google_search_summary(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    snippets = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    full_text = " ".join([snippet.get_text() for snippet in snippets[:5]])
    summarized_text = summarize_text(full_text, num_sentences=3)
    speak(f"Here’s what I found about {query}: {summarized_text}")

# Function to summarize text
def summarize_text(text, num_sentences=3):
    sentences = text.split(". ")
    return ". ".join(sentences[:num_sentences]) + "."

# Main program
if __name__ == "__main__":
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        execute_command(command)