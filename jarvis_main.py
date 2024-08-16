import datetime
from bs4 import BeautifulSoup
import pyttsx3
import requests
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Function to speak a given text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice commands from the microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out, please try again.")
            return "None"

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please say that again.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

    return query

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()

        if "wake up" in query:
            try:
                from Greet_me import greetme
                greetme()
            except ImportError:
                print("The module 'Greet_me' is missing or not properly configured.")
                break

            while True:
                query = takeCommand().lower()

                if "go to sleep" in query:
                    speak("Ok sir, you can call me anytime.")
                    break
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("That's great, sir!")
                elif "how are you" in query:
                    speak("Perfect, sir!")
                elif "thank you" in query:
                    speak("You are welcome, sir!")
                elif "google" in query:
                    from search import google_search
                    google_search(query)
                elif "youtube" in query:
                    from search import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from search import searchWikipedia
                    searchWikipedia(query)
                elif "temperature" in query or "weather" in query:
                    search = "temperature in Muzaffarpur"
                    url = f"https://www.google.com/search?q={search}"
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                    data = BeautifulSoup(response.text, "html.parser")
                    temp = data.find("div", class_="BNeawe iBp4i AP7Wnd")
                    if temp:
                        if "temperature" in query:
                            speak(f"Current temperature in Muzaffarpur is {temp.get_text()}.")
                        else:
                            speak(f"Current weather in Muzaffarpur is {temp.get_text()}.")
                    else:
                        speak("Temperature or weather information for Muzaffarpur not found.")
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"The current time is {strTime}.")
                elif "finally sleep" in query:
                    speak("Going to sleep")
                    exit()
