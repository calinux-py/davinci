# Speech recon modules
import speech_recognition as sr
import pyttsx3
# OpenAI used to query chatgpt
import openai
# Elevenlabs modules used for text-to-speech audio
import elevenlabs
from elevenlabs import generate, play
# Needed for random responses
import random
# Logging modules
import logging
import datetime
import os
# pygame - used to play mp3 files from audio folder to save on API credits
import pygame


# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.txt file
config_file_path = os.path.join(current_directory, 'config', 'config.txt')

# Read API keys from the config file
with open(config_file_path, 'r') as config_file:
    config_data = config_file.readlines()

elevenlabs_key = None
openai_key = None

for line in config_data:
    if line.startswith("elevenlabs.api_key"):
        elevenlabs_key = line.split("'")[1]
    elif line.startswith("openai.api_key"):
        openai_key = line.split("'")[1]

# Check if the keys are found
if not elevenlabs_key or not openai_key:
    raise ValueError("API keys not found in the config file.")


# Set OpenAI API credentials
openai.api_key = openai_key


def speak(text):
    audio = generate(
        text=text,
        voice="Josh",  # Use the "Davinci" voice
        model='eleven_monolingual_v1',
        api_key=elevenlabs_key
    )
    play(audio)

def listen_for_trigger():
    try:
        with sr.Microphone() as source:
            print("...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print("An error occurred:", str(e))
                pass

        try:
            phrase = recognizer.recognize_google(audio).lower()
            if "okay davinci" in phrase:
                print("User: Okay DaVinci")
                # Path to the audio folder
                audio_folder = os.path.join(os.path.dirname(__file__), "audio")

                # Path to the search folder
                search_folder = os.path.join(audio_folder, "listening")

                # Initialize the pygame mixer
                pygame.mixer.init()

                # Get a list of all the MP3 files in the search folder
                mp3_files = [
                    os.path.join(search_folder, file)
                    for file in os.listdir(search_folder)
                    if file.endswith(".mp3")
                ]

                # Check if there are any MP3 files in the search folder
                if mp3_files:
                    # Select a random MP3 file
                    random_mp3 = random.choice(mp3_files)

                    # Load and play the selected MP3 file
                    pygame.mixer.music.load(random_mp3)
                    pygame.mixer.music.play()

                    # Wait for the MP3 file to finish playing
                    while pygame.mixer.music.get_busy():
                        pass
                else:
                    print("No MP3 files found in the search folder.")
                return True
        except sr.UnknownValueError:
            pass

        return False
    except:
        listen_for_trigger()

def transcribe_speech():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio)
            print("User: " + text)
            return text
        except sr.UnknownValueError:
            return ""
    except:
        print("Error - Transcribe Speech Error")

def generate_chat_response(user_input):
    # Path to the audio folder
    audio_folder = os.path.join(os.path.dirname(__file__), "audio")

    # Path to the search folder
    search_folder = os.path.join(audio_folder, "search")

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Get a list of all the MP3 files in the search folder
    mp3_files = [
        os.path.join(search_folder, file)
        for file in os.listdir(search_folder)
        if file.endswith(".mp3")
    ]

    # Check if there are any MP3 files in the search folder
    if mp3_files:
        # Select a random MP3 file
        random_mp3 = random.choice(mp3_files)

        # Load and play the selected MP3 file
        pygame.mixer.music.load(random_mp3)
        pygame.mixer.music.play()

        # Wait for the MP3 file to finish playing
        while pygame.mixer.music.get_busy():
            pass
    else:
        print("No MP3 files found in the search folder.")
    user_input = "You are DaVinci - personal assistant. You'll respond concisely within 30 words while maintaining proper language etiquette.\n " + user_input
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=55,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def prompt_satisfaction():
    # Path to the audio folder
    audio_folder = os.path.join(os.path.dirname(__file__), "audio")

    # Path to the search folder
    search_folder = os.path.join(audio_folder, "sat")

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Get a list of all the MP3 files in the search folder
    mp3_files = [
        os.path.join(search_folder, file)
        for file in os.listdir(search_folder)
        if file.endswith(".mp3")
    ]

    # Check if there are any MP3 files in the search folder
    if mp3_files:
        # Select a random MP3 file
        random_mp3 = random.choice(mp3_files)

        # Load and play the selected MP3 file
        pygame.mixer.music.load(random_mp3)
        pygame.mixer.music.play()

        # Wait for the MP3 file to finish playing
        while pygame.mixer.music.get_busy():
            pass
    else:
        print("No MP3 files found in the search folder.")

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=10)

    try:
        response = recognizer.recognize_google(audio).lower()
        if response in ["yes", "indeed", "sure", "correct", "that's enough", "alright", "I guess", "It is"]:
            # Path to the audio folder
            audio_folder = os.path.join(os.path.dirname(__file__), "audio")

            # Path to the search folder
            search_folder = os.path.join(audio_folder, "good")

            # Initialize the pygame mixer
            pygame.mixer.init()

            # Get a list of all the MP3 files in the search folder
            mp3_files = [
                os.path.join(search_folder, file)
                for file in os.listdir(search_folder)
                if file.endswith(".mp3")
            ]

            # Check if there are any MP3 files in the search folder
            if mp3_files:
                # Select a random MP3 file
                random_mp3 = random.choice(mp3_files)

                # Load and play the selected MP3 file
                pygame.mixer.music.load(random_mp3)
                pygame.mixer.music.play()

                # Wait for the MP3 file to finish playing
                while pygame.mixer.music.get_busy():
                    pass
            else:
                print("No MP3 files found in the search folder.")
            return True
        elif any(word in response for word in
                 ["no", "not at all", "not really", "it is not", "try again", "search again", "no its not",
                  "not helpful", "not satisfied"]):
            # Path to the audio folder
            audio_folder = os.path.join(os.path.dirname(__file__), "audio")

            # Path to the search folder
            search_folder = os.path.join(audio_folder, "retry")

            # Initialize the pygame mixer
            pygame.mixer.init()

            # Get a list of all the MP3 files in the search folder
            mp3_files = [
                os.path.join(search_folder, file)
                for file in os.listdir(search_folder)
                if file.endswith(".mp3")
            ]

            # Check if there are any MP3 files in the search folder
            if mp3_files:
                # Select a random MP3 file
                random_mp3 = random.choice(mp3_files)

                # Load and play the selected MP3 file
                pygame.mixer.music.load(random_mp3)
                pygame.mixer.music.play()

                # Wait for the MP3 file to finish playing
                while pygame.mixer.music.get_busy():
                    pass
            else:
                print("No MP3 files found in the search folder.")
            return False

    except sr.UnknownValueError:
        pass

    return True  # Assume 'yes' if no valid response within 10 seconds

def main():
    while True:
        triggered = listen_for_trigger()

        if triggered:
            user_input = transcribe_speech()
            if any(keyword in user_input for keyword in ["nevermind", "exit", "quit"]):
                response_options = [
                    "No problem.",
                    "No worries.",
                ]
                response = random.choice(response_options)
                speak(response)
                continue

            if not user_input:
                # Path to the audio folder
                audio_folder = os.path.join(os.path.dirname(__file__), "audio")

                # Path to the search folder
                search_folder = os.path.join(audio_folder, "nohear")

                # Initialize the pygame mixer
                pygame.mixer.init()

                # Get a list of all the MP3 files in the search folder
                mp3_files = [
                    os.path.join(search_folder, file)
                    for file in os.listdir(search_folder)
                    if file.endswith(".mp3")
                ]

                # Check if there are any MP3 files in the search folder
                if mp3_files:
                    # Select a random MP3 file
                    random_mp3 = random.choice(mp3_files)

                    # Load and play the selected MP3 file
                    pygame.mixer.music.load(random_mp3)
                    pygame.mixer.music.play()

                    # Wait for the MP3 file to finish playing
                    while pygame.mixer.music.get_busy():
                        pass
                else:
                    print("No MP3 files found in the search folder.")
                continue

            response = generate_chat_response(user_input)
            speak(response)

            while True:
                if prompt_satisfaction():
                    break

                response = generate_chat_response(user_input)
                speak(response)

if __name__ == "__main__":
    main()
