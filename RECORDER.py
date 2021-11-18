from pynput import mouse
from pynput.mouse import Button, Controller, Listener
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Listener as KeyboardListener
import logging
import time
import threading
from datetime import datetime
import fileLoader

startTime=time.time()
isRecording = 0


#Removes current logging handler. (activated after recording, so when a new recording is started the old one gets deleted, instead of continued)
def initLogging():
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    #Recreate the log
    #fh = logging.FileHandler(NewRecName)
    #fh.setLevel(logging.DEBUG)

#Every time the cursor moves counting goes up by 1. The logger only records every 20 intervals for practical purposes. This can be changed in the function on_move after the %.
counting = 0
HotkeyStopRec = 0

#This function determines what happens when the mouse moves.

def on_move(x, y):
    if HotkeyStopRec == 1:
        print('The function activated.')
        return False
    else:
        global counting
        counting+=1
        
        if counting%10==0:
            logging.info('{0} {1} {2} {3}'.format(x, y, 'CursorMovement', 'idle'))

#This function determines what happens when the mouse is clicked
def on_click(x, y, button, pressed):
    logging.info('{0} {1} {2} {3}'.format(x,y, button, pressed))
    if button == mouse.Button.middle:
        return False
    if HotkeyStopRec == 1:
        return False
        

#Makes the currenty loaded file equal to the one that just got recorded.
def changeFileAfterRecord():
    if fileLoader.currentFilename:
        fileLoader.currentFilename='mouselogbeta.maus'
    else:
        fileLoader.currentFilename='mouselogbeta.maus'


def stopMouseHotkey():
    mouse.Listener.stop()

def stopMouseV2():
    return False



'''
def runListener():
    global isRecording
    isRecording = 1


                
    logging.basicConfig(filename='mouselogbeta.maus', filemode='w', level=logging.DEBUG, force=True, format='%(created)f %(message)s End')
    
    with Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()
        time.sleep(0.2)
    
    changeFileAfterRecord()
    initLogging()

    global HotkeyStopRec
    HotkeyStopRec = 0

    isRecording = 0
'''










