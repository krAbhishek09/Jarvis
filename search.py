import pywhatkit as kit
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


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
        print(
            f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

    return query

# Function to search Google


def google_search(query):
    query = query.replace("jarvis", "").replace(
        "google search", "").replace("google", "").strip()
    speak("This is what I found on Google")

    try:
        kit.search(query)
        result = wikipedia.summary(query, sentences=1)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except Exception:
        speak("No speakable output available")

# Function to search YouTube


def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "").replace(
            "youtube", "").strip()
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        kit.playonyt(query)
        speak("Done, sir")


def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from Wikipedia...")
        query = query.replace("wikipedia", "").replace("jarvis", "").strip()
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia...")
        print(results)
        speak(results)


if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if query:
            if "google" in query:
                google_search(query)
            elif "youtube" in query:
                searchYoutube(query)
            elif "exit" in query or "quit" in query:
                speak("Exiting the program. Goodbye!")
                break
