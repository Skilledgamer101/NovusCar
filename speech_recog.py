import speech_recognition as sr
import re
import text_message
import pyaudio

recognizer = sr.Recognizer() # Instantiating speech recognition class

def listen_for_yes_or_no():
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=5) # Listens to audio (will listen for 5 seconds)

    try:
        text = recognizer.recognize_google(audio) # Google web search API converts speech to text

        # Use regex to check if the words 'yes' or 'no' are present in text
        if re.search(r'\byes\b', text, re.IGNORECASE):
            print("You said 'yes'!")
            return True
        elif re.search(r'\bno\b', text, re.IGNORECASE):
            print("You said 'no'!")
            return False
        else:
            print("You did not say 'yes' or 'no'.")
            return None

    except sr.UnknownValueError: # Possible errors
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Error with the speech recognition service; {0}".format(e))
        return None
    
def return_speech():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None
    
def save_speech(filename='call_file.wav'): # Saves speech in .wav file called 'call_file.wave'
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source, timeout=5)

    try:
        # Save the audio to a file
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"Audio saved as {filename}")

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")