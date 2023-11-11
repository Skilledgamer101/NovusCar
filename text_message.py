import pyttsx3
import speech_recog

engine = pyttsx3.init()

# All of these functions are scripted outputs from the car
def speak_text():
    engine.say("Received text from Daniel: how far are you from home?")
    engine.runAndWait() # Wait before saying next thing
    
def respond():
    engine.say("Do you want to respond to this text? Say yes or no.")
    engine.runAndWait()
    
def response():
    engine.say("What would you like to say? ")
    engine.runAndWait()
    
def speech_exit():
    engine.say("Alright, nothing will be sent.")
    engine.runAndWait()
    
# This function repeats what user said back to them and sends the text 
def sent_text():
    final_text = speech_recog.return_speech()
    engine.say("You said: " + final_text + " Sending now.")
    engine.runAndWait()
