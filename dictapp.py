import os
import subprocess
import pyautogui
import webbrowser
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Function to speak a given text


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


dictapp = {
    "command prompt": "cmd",
    "paint": "mspaint",
    "word": "winword",
    "notepad": "notepad",
    "camera": "start ms-camera",
    "file explorer": "explorer",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "chrome": "chrome",
    "edge": "msedge"
}


def openappweb(query):
    speak("Launching, sir")

    if ".com" in query or ".co.in" in query or ".org" in query:
        # Clean up the query for web browsing
        query = query.lower().replace("open", "").replace(
            "jarvis", "").replace("launch", "").strip()

        # Open the web browser with the query
        webbrowser.open(f"https://{query}")
    else:
        # Check if the application name is in the dictionary
        for app, command in dictapp.items():
            if app in query.lower():
                try:
                    os.system(f"start {command}")
                    return  # Exit the function after launching the app
                except Exception as e:
                    speak(f"Error opening {app}: {e}")
                break
        else:
            speak("Application not found in the dictionary.")
