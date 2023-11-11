import pyttsx3
import speech_recog

engine = pyttsx3.init()

def calling():
    engine.say("Daniel is calling you.")
    engine.runAndWait()
    
def respond_to_call():
    engine.say("Do you want to pick up this call? Say yes or no")
    engine.runAndWait()
    
def no_call():
    engine.say("Alright, not picking up call")
    engine.runAndWait()
    
def yes_call():
    engine.say("Picking up Daniel's call")
    engine.runAndWait()