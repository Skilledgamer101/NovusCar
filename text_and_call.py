import keyboard
import text_message
import call
import speech_recog
import time

def text_message_speech():
    key1 = "t" # Defining keys for 'text' and 'call'
    key2 = "c"
    time.sleep(2)
    while True: # Need a while loop so user has time to press a key
        print(f"Waiting for {key1} or {key2} to be pressed")
        if keyboard.read_key() == key1: # If key pressed is t
            print(f"{key1} pressed")
            print("You have received this text message: \n")
            text_message.speak_text() # speak the text
            text_message.respond() # Does user want to respond?
            print("Say yes or no...")
            result = speech_recog.listen_for_yes_or_no() # Result stores boolean True for 'yes' and False for 'no'
            if result is not None:
                if result:
                    text_message.response()
                    text_message.sent_text()
                    continue
                else:
                    text_message.speech_exit()
                    continue
            else:
                continue
            
        elif keyboard.read_key() == key2: # If key is 'c'
            print(f"{key2} pressed")
            print("Daniel is calling you.")
            call.calling() # Daniel is calling
            call.respond_to_call() # Do you want to respond to the call?
            print("Say yes or no...")
            result = speech_recog.listen_for_yes_or_no() # Result stores boolean True for 'yes' and False for 'no'
            if result is not None:
                if result:
                    call.yes_call()
                    speech_recog.save_speech() # Saves call as audio file
                    print("Call saved as audio file.")
                    continue
                else:
                    call.no_call()
                    continue
            else:
                continue
        else:
            print("No call or text")
            continue
        
if __name__ == '__main__':
    text_message_speech()