
import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# Load the environment variable for the OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client with your API key
client = OpenAI(api_key=api_key)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Pre-initialize the recognizer
recognizer = sr.Recognizer()

def recognize_and_respond():
    with sr.Microphone() as source:
        print("Say something!")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

                # Send recognized text to OpenAI
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": text}]
                )

                reply = response.choices[0].message.content.strip()
                print(reply)

                # Use TTS to speak the response
                engine.say(reply)
                engine.runAndWait()

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    recognize_and_respond()