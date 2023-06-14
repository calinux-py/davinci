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
# To save money on the elevenlabs api, download each individual voice clip and use the audio as the downloaded file
# Instead of using the API - this way the API is only used for the speech from ChatGPT


# Set OpenAI API credentials
openai.api_key = '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'  # API FOR OpenAI GOES HERE

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Configure logging
log_folder = "Logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

today = datetime.datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(log_folder, f"LOGGING-{today}.txt")

# Regular logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')




def speak(text):
    audio = generate(
        text=text,
        voice="Josh",
        model='eleven_monolingual_v1',
        api_key='1cc5ad7279217ee6cc943da6ee4a90b8'  # API FROM ElevenLabs GOES HERE
    )
    play(audio)


def log_error(message):
    error_message = str(message)
    error_conditions = [
        "listening timed out while waiting for phrase to start" # do not include this as an error as it is not an error and simply restarting the 5 second cooldown...
    ]

    if any(condition in error_message for condition in error_conditions):
        return  # Do not log the error as it's normal and not an error

    if "cannot access local variable 'audio' where it is not associated with a value" in error_message:
        error_message += " [NO AUDIO INPUT DETECTED]" # this error means the phrase was not detected

    logging.error(f"An error occurred at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {error_message}")

    # logging.error("\n\nERROR DETAILS:\n", exc_info=True)         # uncomment to provide more details about error messages


def listen_for_trigger():
    try:
        with sr.Microphone() as source:
            print("...")
            logging.info("DaVinci is listening for the trigger phrase...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            except Exception as e:
                log_error(e)

        try:
            phrase = recognizer.recognize_google(audio).lower()
            if "okay davinci" in phrase:
                logging.info(f"User: Okay DaVinci at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                response_options = [
                    "I'm listening.",
                    "Yes?",
                    "DaVinci here",
                    "DaVinci reporting.",
                    "It's DaVinci."
                ]
                response = random.choice(response_options)
                speak(response)
                return True
        except sr.UnknownValueError as e:
            log_error(e)
            pass

        return False
    except Exception as e:
        log_error(e)
        return listen_for_trigger()


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
    except Exception as e:
        log_error(e)
        print("Error - Transcribe Speech Error")


def generate_chat_response(user_input):
    try:
        response_options = [
            "Let me check.",
            "Let me investigate.",
            "Allow me to check.",
            "I'll examine that.",
            "Allow me to search.",
            "I'll explore that.",
            "I'll research that.",
            "Leave it to me."
        ]
        response = random.choice(response_options)
        speak(response)
        user_input = "You are DaVinci - personal assistant. You'll respond concisely within 30 words while maintaining proper language etiquette.\n " + user_input
        logging.info(user_input)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=55,
            n=1,
            stop=None,
            temperature=0.7
        )
        generated_response = response.choices[0].text.strip()
        logging.info(generated_response)  # Log the generated response
        return generated_response
    except Exception as e:
        log_error(e)


def prompt_satisfaction():
    response_options = [
        "Is this acceptable?",
        "Is this satisfactory?",
        "Is this sufficient?",
        "Is this adequate?"
    ]
    response = random.choice(response_options)
    speak(response)

    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            print("Timeout occurred. Returning to trigger listening...")
            return False

    try:
        response = recognizer.recognize_google(audio).lower()
        if response in ["yes", "indeed", "sure", "correct", "that's enough", "alright", "I guess", "It is"]:
            response_options = [
                "Great.",
                "Perfect.",
                "Excellent."
            ]
            response = random.choice(response_options)
            speak(response)
            return True
        elif any(word in response for word in
                 ["no", "not at all", "not really", "it is not", "try again", "search again", "no its not",
                  "not helpful", "not satisfied"]):
            response_options = [
                "Let's try again.",
                "Let's retry.",
                "I'll retry",
                "I'll try again"
            ]
            response = random.choice(response_options)
            speak(response)
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
                response_options = [
                    "I didn't quite catch that.",
                    "I missed what you said.",
                    "I didn't hear you properly.",
                ]
                response = random.choice(response_options)
                speak(response)
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