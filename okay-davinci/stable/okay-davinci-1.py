import speech_recognition as sr
import pyttsx3
import openai
from elevenlabs import generate, play
import elevenlabs

def speak(text):
    audio = generate(
        text=text,
        voice="Josh",
        model='eleven_monolingual_v1',
        api_key='1cc5ad7279217ee6cc943da6ee4a90b8'  # Add the API key parameter
    )
    play(audio)

elevenlabs.api_key = '1cc5ad7279217ee6cc943da6ee4a90b8'
# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Set OpenAI API credentials
openai.api_key = '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'

def listen_for_trigger():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("Error: Timeout occurred while listening for phrase.")
                pass
            except Exception as e:
                print("An error occurred:", str(e))
                pass

        try:
            phrase = recognizer.recognize_google(audio).lower()
            if "okay davinci" in phrase:
                print("User: Okay DaVinci")
                custom_text = "I'm listening, sir."
                speak(custom_text)
                return True
        except sr.UnknownValueError:
            pass

        return False
    except:
        print("Error: Function Error")
        listen_for_trigger()

def transcribe_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        print("User: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""

def generate_chat_response(user_input):
    user_input = "You are a personal assistant. Respond to all input in less than 50 words without affecting proper language etiquette " + user_input
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def prompt_satisfaction():
    custom_text = "Is this satisfactory, sir?."
    speak(custom_text)

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=10)

    try:
        response = recognizer.recognize_google(audio).lower()
        if "yes" in response:                                          # this needs to be edited to only accept input on 5
            custom_text = "Very well, sir."
            speak(custom_text)                                    # second segments - like listen_for_trigger
            return True
        elif "no" in response:
            custom_text = "Let's try again, sir."
            speak(custom_text)
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
                custom_text = "No problem, sir."
                speak(custom_text)
                continue

            if not user_input:
                custom_text = "Sorry, sir, I didn't catch that."
                speak(custom_text)
                print("Sorry sir, I didn't catch that.")
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
