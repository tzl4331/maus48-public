import tkinter as tk
from tkinter import ttk, messagebox

import RECORDER, ANALYSER, fileLoader
import ANALYSER
import os
import threading
import time
import logging
import random
import SETTINGS

from pynput.mouse import Button, Controller
from pynput.mouse import Listener as mListener
from pynput import keyboard
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener

root=tk.Tk()
root.geometry('380x150')
root.attributes("-topmost", True)
root.title('maus48 remastered 6.0')

SETTINGS.loadUserSettings()

Frame1 = tk.Frame(root)
Frame1.pack()

Frame2 = tk.Frame(root)
Frame2.pack()

#When playing back a script, ACTIVATEEVERYTHING checks if number is > 1, and will stop the playback if it is:
number = 0

#Keeps track of whether playback is currently active... so Hotkey for Record cannot activate during playback
isPlayingBack = 0

#Number of Loops required for Next Playback:
LoopsRequired = 0
LoopsInfinity = 0

#Hotkeys
playkey='F12'
recordkey= 'F8'

#These are the temporary hotkeys from user input. If save and apply is clicked, this will become the Actual Hotkeys. 



#Playback
def playButton(): 
    
    global number 
    number = 0
    
    #Begins playback:
    def start():
        button_record["state"]="disabled"
        button_save["state"]="disabled"
        button_load["state"]="disabled"
        button_play["state"]="disabled"


        confirm_play = True
        #tk.messagebox.askyesno("Start Playback", "Close this prompt to start playback. Or cancel.")
        if confirm_play == True:
            try:
                global isPlayingBack
                isPlayingBack = 1
                info2["text"]="Playback In Progress = {0}".format(os.path.basename(fileLoader.currentFilename))
                ACTIVATEEVERYTHING()
                isPlayingBack = 0
                #tk.messagebox.showwarning("Done", "Playback Finished, now idle.\n\nIf you see this screen immediately after clicking play just try again, the next playback should work. Might be a bug with the keyboard listener\n")
            except: 
                isPlayingBack = 0
                #tk.messagebox.showwarning("Cancelled", "Couldn't find anything to play. Perhaps you deleted the script or just launched?\n\nTry again after reloading or recording!\n")
        else:
            tk.messagebox.showwarning("Cancelled", "Nothing interesting happens")
        button_record["state"]="normal"
        button_save["state"]="normal"
        button_load["state"]="normal"
        button_play["state"]="normal"
        info2["text"]="Loaded File = {0}".format(os.path.basename(fileLoader.currentFilename))


    #Starts playback thread and updates UI with currently loaded file
    T2 = threading.Thread(target=start)
    T2.start()
    try:
        info2["text"]="Loaded File = {0}".format(os.path.basename(fileLoader.currentFilename))
    except:
        pass
#Record
StopwatchActivateStatus = False
StoredDuration = None

def recordButton():
    def record():
        #Disables all UI buttons
        button_record["state"]="disabled"
        button_save["state"]="disabled"
        button_load["state"]="disabled"
        button_play["state"]="disabled"

        button_record["text"]="SCRL CLICK"
        info2["text"]="Recording in progress..."

        def Start():
            global StopwatchActivateStatus
            StopwatchActivateStatus = True
    
            def Stopwatch():
                hours = 0
                minutes = 0
                seconds = 0
                global StoredDuration
                
                countTo10 = 0
                while StopwatchActivateStatus:
                    time.sleep(0.05)
                    countTo10 +=1
                    if countTo10 == 20:
                        countTo10 = 0
                        if StopwatchActivateStatus == False:
                            StoredDuration = "{0}:{1}:{2}".format(str(hours).zfill(1), str(minutes).zfill(2), str(seconds).zfill(2))
                            break
                        else:
                            seconds+=1

                            if seconds == 60:
                                minutes += 1
                                seconds -= 60

                            if minutes == 60:
                                hours += 1
                                minutes -= 60    
                            
                            info2["text"] = ("Recording in progress: {0}:{1}:{2}".format(str(hours).zfill(1), str(minutes).zfill(2), str(seconds).zfill(2)))
                            #Stores the Stored Duration
                            StoredDuration = "{0}:{1}:{2}".format(str(hours).zfill(1), str(minutes).zfill(2), str(seconds).zfill(2))
                    else:
                        pass
            T122 = threading.Thread(target=Stopwatch)
            T122.start()

        Start()
        #RECORDER.runListener()
        runListener()

        global StopwatchActivateStatus
        StopwatchActivateStatus = False

        #Re-enables UI buttons and updates UI with currently loaded file
        button_record["state"]="normal"
        button_save["state"]="normal"
        button_load["state"]="normal"
        button_play["state"]="normal"

        button_record["text"]="Record"
        info2["text"]="Temporary Save = {0} ({1})".format(fileLoader.currentFilename, StoredDuration)
   
    T1 = threading.Thread(target=record)
    T1.start()

def saveButton():
    fileLoader.fileToSave()

def loadButton():
    fileLoader.fileToLoad()
    info2["text"]="Loaded File = {0}".format(os.path.basename(fileLoader.currentFilename))

def passButton():
    pass

def Testbutton():
    SETTINGS.PlaybackLooper("Single")
    print(LoopsRequired)



def settingsButton():

    win = tk.Toplevel()
    win.geometry('1150x760')
    win.attributes('-topmost', True)
    win.title('Settings for maus48')
    
    settingsTitle = tk.Label(win, text="Settings")
    settingsTitle.config(font=("Segoe UI", 15))
    settingsTitle.pack()
    
    label = ttk.Label(win, text="maus 48 v7.0", style='Bold.TLabel').pack(pady=(10,0))
    labeltop = ttk.Button(win, text="Currently saved settings: {} Sampling, {} Playback Loop, {} Playback Hotkey, {} Recording Hotkey, Antiban = {}.".format(SETTINGS.Configured_sampling_method, SETTINGS.Configured_looping_method, SETTINGS.Configured_playkey_temp, SETTINGS.Configured_recordkey_temp, SETTINGS.Configured_antiban), style='Bold.TLabel')
    labeltop.pack(pady=(5,8))

    ################# FUNCTIONS FOR SAMPLING METHOD ##############################
    def fidelityButton():
        button_fidelity["state"]="disabled"
        button_efficiency["state"]="normal"
        button_hybrid["state"]="normal"

        button_fidelity["text"]="[Fidelity]"
        button_efficiency["text"]="Efficiency"
        button_hybrid["text"]="Hybrid"
        SETTINGS.User_sampling_method = "Fidelity"

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"

    def efficiencyButton():
        button_efficiency["state"]="disabled"
        button_fidelity["state"]="normal"
        button_hybrid["state"]="normal"

        button_fidelity["text"]="Fidelity"
        button_efficiency["text"]="[Efficiency]"
        button_hybrid["text"]="Hybrid"
        SETTINGS.User_sampling_method = "Efficiency"

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"

    def hybridButton():
        button_hybrid["state"]="disabled"
        button_fidelity["state"]="normal"
        button_efficiency["state"]="normal"

        button_fidelity["text"]="Fidelity"
        button_efficiency["text"]="Efficiency"
        button_hybrid["text"]="[Hybrid]"
        SETTINGS.User_sampling_method = "Hybrid"

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"

    ################# FUNCTIONS FOR PLAYBACK LOOPING ##############################
    def singleButton():
        button_single["state"]="disabled"
        button_infinite["state"]="normal"
        button_custom["state"]="normal"

        button_single["text"]="[Single]"
        button_infinite["text"]="Infinite"
        button_custom["text"]="Custom"
        SETTINGS.User_looping_method = "Single"

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"

    def infiniteButton():
        button_single["state"]="normal"
        button_infinite["state"]="disabled"
        button_custom["state"]="normal"

        button_single["text"]="Single"
        button_infinite["text"]="[Infinite]"
        button_custom["text"]="Custom"
        SETTINGS.User_looping_method = "Infinite"

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"

    def customButton():
        button_single["state"]="normal"
        button_infinite["state"]="normal"
        button_custom["state"]="disabled"

        button_single["text"]="Single"
        button_infinite["text"]="Infinite"
        button_custom["text"]="[Custom]"
        SETTINGS.User_looping_method = "Custom"

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"
    
    ######### FUNCTIONS FOR OSRS ANTIBAN / RANDOMIZATION ############
    def antibanOnButton():
        button_antibanOn["state"]="disabled"
        button_antibanOff["state"]="normal"
        button_antibanOn["text"]="Antiban is enabled"
        button_antibanOff["text"]="Turn off OSRS Randomize Antiban"

        SETTINGS.User_antiban = 1

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"
    
    def antibanOffButton():
        button_antibanOff["state"]="disabled"
        button_antibanOn["state"]="normal"
        button_antibanOff["text"]="Antiban is disabled"
        button_antibanOn["text"]="Turn on OSRS Randomize Antiban"

        SETTINGS.User_antiban = 0

        button_apply["text"]="Save and apply changes"
        button_apply["state"]="normal"



    #Packing the Frames in Settings
    ############ FRAMES FOR SAMPLING METHOD ###############
    WinFrame1 = tk.Frame(win)
    WinFrame1.pack()

    WinFrame2 = tk.Frame(win)
    WinFrame2.pack(pady=10)

    #Window Frame 1
    WinFrame1Labels = tk.Frame(WinFrame1)
    WinFrame1Labels.pack(side=tk.TOP)
    Samplinglabel = ttk.Label(WinFrame1Labels, text="Sampling Method", style='Bold.TLabel', anchor='w').pack(side=tk.LEFT, padx=15)
    SamplingDescription = ttk.Label(WinFrame1Labels, text="This controls how frequently your cursor movements are logged.\nFidelity:  Prioritises cursor positioning - captures each pixel movement. Makes cursor appear smooth on monitor.\nEfficiency:  Prioritises timings - captures cursor periodically. Preserves timings between clicks. Cursor may appear choppy.\nHybrid:  Both prioritised equally. Best of both worlds, recommeded for most use cases. ").pack(side=tk.BOTTOM)

    button_fidelity= ttk.Button(WinFrame2, text="Fidelity", width=10, command=fidelityButton, style='my.TButton' )
    button_fidelity.pack(side=tk.LEFT, padx=8, ipady=20)

    button_efficiency = ttk.Button(WinFrame2, text='Efficiency', width=10, command=efficiencyButton, style='my.TButton' )
    button_efficiency.pack(side=tk.LEFT, padx=8, ipady=20)

    button_hybrid = ttk.Button(WinFrame2, text="Hybrid", width=10, command=hybridButton, style='my.TButton' )
    button_hybrid.pack(side=tk.RIGHT, padx=8, ipady=20)

    ############ FRAMES FOR PLAYBACK LOOPING ###############
    WinFrame3 = tk.Frame(win)
    WinFrame3.pack()

    WinFrame4 = tk.Frame(win)
    WinFrame4.pack(pady=10)

    WinFrame3Labels = tk.Frame(WinFrame3)
    WinFrame3Labels.pack(side=tk.TOP)
    LoopLabel = ttk.Label(WinFrame3Labels, text="Playback Looping", style='Bold.TLabel', anchor='w').pack(side=tk.LEFT, padx=15)
    
    LoopDescription = ttk.Label(WinFrame3Labels, text="This controls playback loops and repeats.                                                                                                                                             \nSingle:  Plays the loaded script once\nInfinite:  Plays the loaded script until the Stop Hotkey is pressed\nCustom:  Repeats n times or until Stop Hotkey pressed ").pack(side=tk.BOTTOM, fill=tk.X)

    button_single= ttk.Button(WinFrame4, text="Single", width=10, command=singleButton, style='my.TButton' )
    button_single.pack(side=tk.LEFT, padx=8, ipady=20)

    button_infinite = ttk.Button(WinFrame4, text='Infinite', width=10, command=infiniteButton, style='my.TButton' )
    button_infinite.pack(side=tk.LEFT, padx=8, ipady=20)

    button_custom = ttk.Button(WinFrame4, text="Custom", width=10, command=customButton, style='my.TButton' )
    button_custom.pack(side=tk.RIGHT, padx=8, ipady=20)



    ############ FRAMES FOR HOTKEY SETTINGS ###############
    WinFrame5 = tk.Frame(win)
    WinFrame5.pack()

    WinFrame6 = tk.Frame(win)
    WinFrame6.pack(pady=20)

    WinFrame5Labels = tk.Frame(WinFrame5)
    WinFrame5Labels.pack(side=tk.TOP)
    HKLabel = ttk.Label(WinFrame5Labels, text="Hotkey Preferences", style='Bold.TLabel', anchor='w').pack(side=tk.LEFT, padx=15)
    
    HKDescription = ttk.Label(WinFrame5Labels, text="\nThis controls user hotkey preferences.                                                                                                                                                       \nNote: The playback hotkey cannot be the recording hotkey").pack(side=tk.BOTTOM, fill=tk.X)

    #PlayHotkey Menu
    def changePlayHotkey(PHKResult):
        play_hotkey_choice = PlayHotkeyChoice.get()
        #list_of_rec_hotkeys.pop(play_hotkey_choice)
        if not play_hotkey_choice == "Choose Playback Hotkey":
            if not play_hotkey_choice == SETTINGS.User_recordkey_temp:
                SETTINGS.User_playkey_temp = play_hotkey_choice
                button_apply["text"]="Save and apply changes"
                button_apply["state"]="normal"
            else:
                tk.messagebox.showwarning("Hotkey In Use", "Your playback and recording hotkey cannot be the same.\n\nPlease choose another hotkey.\n")
                PlayHotkeyChoice.set("Choose Recording Hotkey")
                pass
        #RecHotkey.configure(ttk.OptionMenu(WinFrame6, RecHotkeyChoice, *list_of_rec_hotkeys, command=changeRecHotkey).pack(side=tk.LEFT))
        print(play_hotkey_choice)
    PlayHotkeyChoice = tk.StringVar(value="Select Playback Hotkey...")
    list_of_hotkeys = {'Choose Playback Hotkey':1,'F1':2,'F2':3,'F3':4,'F4':5,'F5':6,'F6':7,'F7':8,'F8':9,'F9':10,'F10':11,'F11':12,'F12':13}
    
    PHKDescription = ttk.Label(WinFrame6, text="Playback:  ", style='Bold.TLabel').pack(side=tk.LEFT, padx = 15)
    PlayHotkey = ttk.OptionMenu(WinFrame6, PlayHotkeyChoice, *list_of_hotkeys, command=changePlayHotkey).pack(side=tk.LEFT)

    #RecordingHotkey Menu
    def changeRecHotkey(RHKResult):
        rec_hotkey_choice = RecHotkeyChoice.get()
        if not rec_hotkey_choice == "Choose Recording Hotkey":
            if not rec_hotkey_choice == SETTINGS.User_playkey_temp:
                SETTINGS.User_recordkey_temp = rec_hotkey_choice
                button_apply["text"]="Save and apply changes"
                button_apply["state"]="normal"
            else:
                tk.messagebox.showwarning("Hotkey In Use", "Your playback and recording hotkey cannot be the same.\n\nPlease choose another hotkey.\n")
                RecHotkeyChoice.set("Choose Recording Hotkey")
                pass
        print(rec_hotkey_choice)
    RecHotkeyChoice = tk.StringVar(value="F6")
    list_of_rec_hotkeys = {'Choose Recording Hotkey':1,'F1':2,'F2':3,'F3':4,'F4':5,'F5':6,'F6':7,'F7':8,'F8':9,'F9':10,'F10':11,'F11':12,'F12':13}

    RHKDescription = ttk.Label(WinFrame6, text="Recording:  ", style='Bold.TLabel').pack(side=tk.LEFT, padx=15)
    RecHotkey = ttk.OptionMenu(WinFrame6, RecHotkeyChoice, *list_of_rec_hotkeys, command=changeRecHotkey).pack(side=tk.LEFT)

    ##########winframe 7 and 8
    WinFrame7 = tk.Frame(win)
    WinFrame7.pack()

    WinFrame8 = tk.Frame(win)
    WinFrame8.pack(pady=10)

    WinFrame7Labels = tk.Frame(WinFrame7)
    WinFrame7Labels.pack(side=tk.TOP)
    LoopLabel = ttk.Label(WinFrame7Labels, text="OSRS Anti-ban Mode", style='Bold.TLabel', anchor='w').pack(side=tk.LEFT, padx=15)
    
    LoopDescription = ttk.Label(WinFrame7Labels, text="This enables more game anti-ban features                                                                                                                                                      \nTime Randomize:  A varying small delay is added on top of the existing recording delays\nThis means even when looping infinitely there will never be an identical timing pattern").pack(side=tk.BOTTOM, fill=tk.X)

    button_antibanOn= ttk.Button(WinFrame8, text="Anti-ban mode is not yet available", width=35, command=antibanOnButton, style='my.TButton', state="disabled")
    button_antibanOn.pack(side=tk.LEFT, padx=8, ipady=20)

    button_antibanOff = ttk.Button(WinFrame8, text="Einstein is still thinking...", width=35, command=antibanOffButton, style='my.TButton', state="disabled" )
    button_antibanOff.pack(side=tk.LEFT, padx=8, ipady=20)

    WinFrameEND = tk.Frame(win)
    WinFrameEND.pack(pady=8)
    SettingsInfo = ttk.Label(WinFrameEND, text="Even if your old settings don't show here yet, they are still saved unless changed.\nSettings will only save once applied. If 'settings.48' is deleted, settings will be defaulted on next launch.",).pack()

    def applyButton():
        #Save all settings
        SETTINGS.UserPressedSave()
        button_apply["state"]="disabled"
        button_apply["text"]="Settings saved"

        labeltop["text"]="Currently saved settings: {} Sampling, {} Playback Loop, {} Playback Hotkey, {} Recording Hotkey, Antiban = {}.".format(SETTINGS.Configured_sampling_method, SETTINGS.Configured_looping_method, SETTINGS.Configured_playkey_temp, SETTINGS.Configured_recordkey_temp, SETTINGS.Configured_antiban)
        info1["text"]="Record = {}    |    Playback = {}".format(SETTINGS.Configured_recordkey_temp, SETTINGS.Configured_playkey_temp)



    WinFrame9 = tk.Frame(win)
    WinFrame9.pack(pady=10)

    button_apply= ttk.Button(WinFrame9, text="Save and apply changes", width=28, command=applyButton, state="disabled" )
    button_apply.pack(side=tk.BOTTOM, padx=8, ipady=5)


    #SETTINGS.banana()
    pass



#Opens save file, formats each line into a Dictionary entry, then activates every entry
def ACTIVATEEVERYTHING():
    maus = Controller()
    kb = keyboard.Controller()
    

    #ANALYSER.ANALYSE stores each text file line into a formatted dictionary
    clickHistory = ANALYSER.ANALYSE()

    def parse_boolean(b):
        return b == "True"

    global number
    
    TotalPlaybacksNeeded = SETTINGS.loopingPlaybacks() 

    PlayCount = 0
    while PlayCount < TotalPlaybacksNeeded:
        PlayCount += 1 
        for key in clickHistory:
            #Checks if number < 1, otherwise script playback will stop
            if number < 1:
                if clickHistory[key]['whichButton'] == 'Button.middle':
                    break
                else:
                    #MOUSE INPUTS:
                    if clickHistory[key]['whichButton'] == 'CursorMovement' or (clickHistory[key]['whichButton'] == 'Button.left' or clickHistory[key]['whichButton'] == 'Button.right'):
                        time.sleep(clickHistory[key]['delay'])
                        
                        #Relocates cursor to destination
                        maus.position=(clickHistory[key]['x'], clickHistory[key]['y'])
    
                        #Determines whether to Left click or Right click, using the analysed data
                        if parse_boolean(clickHistory[key]['press']):
                            if clickHistory[key]['whichButton'] == 'Button.left':
                                maus.press(Button.left)
                            elif clickHistory[key]['whichButton'] == 'Button.right':
                                maus.press(Button.right)
                        else:
                            if clickHistory[key]['whichButton'] == 'Button.left':
                                maus.release(Button.left)
                            elif clickHistory[key]['whichButton'] == 'Button.right':
                                maus.release(Button.right)
                    else:
                    #KEYBOARD INPUTS
                        #Makes the timing between clicks and mouse movements equal to the User recording's timing.
                        time.sleep(clickHistory[key]['delay'])
                        
                        #Determines whether to press Down or Up on a key, using the analysed data
                        if clickHistory[key]['press'] == 'DOWN':
                            try:
                                buttontopress = clickHistory[key]['whichButton']
                                print(buttontopress)
                                #In pynput, non alphanumeric keys are formatted as Key.enter, Key.esc, Key.shift etc..., so check for this so they can be activated properly
                                if clickHistory[key]['whichButton'][0:3] == 'Key':
                                    
                                    if (clickHistory[key]['whichButton'] == 'Key.ctrl_l') or (clickHistory[key]['whichButton'] == 'Key.ctrl_r'):
                                        kb.press(Key.ctrl)
                                    else:
                                        kb.press(eval(buttontopress))
                                
                                else:
                                    kb.press(buttontopress[1:-1])
                            except Exception as e: 
                                print(e)
                        else:
                            try:
                                buttontopress = clickHistory[key]['whichButton']
                                if clickHistory[key]['whichButton'][0:3] == 'Key':
                                    
                                    if (clickHistory[key]['whichButton'] == 'Key.ctrl_l') or (clickHistory[key]['whichButton'] == 'Key.ctrl_r'):
                                        kb.release(Key.ctrl)
                                    else:
                                        kb.release(eval(buttontopress))
                                else:
                                    kb.release(buttontopress[1:-1])
                            except Exception as e: 
                                print(e)
            else:
                break
          
    number = 0
    PlayCount = 0
    print('done')
    #if press True then click else release etc. Im goign back to add a junk variable to get rid of the \n in the Analyser


#UI: Title, greeting
greeting = tk.Label(Frame1, text="maus 48 v6.0")
greeting.config(font=("Segoe UI", 15))
greeting.pack()


#UI: Button Styles
s = ttk.Style()
s.configure('my.TButton', font=('Segoe UI', 10, 'bold'))
s.theme_use()

#UI: Buttons
button_play = ttk.Button(Frame1, text="Play", width=10, command=playButton, style='my.TButton' , )
button_play.pack(side=tk.LEFT, padx=5, ipady=20)

FrameInFrame = tk.Frame(Frame1)
FrameInFrame.pack(side=tk.LEFT)

button_save = ttk.Button(FrameInFrame, text='Save', width=15, command=saveButton, )
button_save.pack(side=tk.TOP, padx=5, pady=2, ipady=2)

button_settings = ttk.Button(Frame1, text='Settings', width=10, command=settingsButton, )
button_settings.pack(side=tk.LEFT, padx=5, ipady=20)

button_load = ttk.Button(FrameInFrame, text='Load', width=15, command=loadButton, )
button_load.pack(side=tk.TOP, padx=5, pady=3, ipady=2)

button_record = ttk.Button(Frame1, text="Record", width=10, command=recordButton, style='my.TButton' )
button_record.pack(side=tk.RIGHT, padx=5, ipady=20)

#UI: Information Styles
s1 = ttk.Style()
s1.configure('my.TLabel', font=('Segoe UI', 10,))
s1.theme_use()

s2 = ttk.Style()
s2.configure('Bold.TLabel', font=('Segoe UI', 10, 'bold'))
s2.theme_use()

#UI: Information
info1 = ttk.Label(Frame2, text="Record = {}    |    Playback = {}".format(SETTINGS.Configured_recordkey_temp, SETTINGS.Configured_playkey_temp), style='my.TLabel')
info1.config()
info1.pack()

info2 = ttk.Label(Frame2, text="Loaded File = {0}".format(fileLoader.currentFilename), style='Bold.TLabel')
info2.config()
info2.pack(side=tk.BOTTOM)


#TESTING
'''
def on_move(x, y):
    if RECORDER.HotkeyStopRec == 1:
        print('The function activated.')
        return False
    else: 
        RECORDER.counting+=1
        
        if RECORDER.counting%20==0:
            logging.info('{0} {1} {2} {3}'.format(x, y, 'CursorMovement', 'idle'))
'''

def runListener():
    RECORDER.isRecording = 1
                
    logging.basicConfig(filename='mouselogbeta.maus', filemode='w', level=logging.DEBUG, force=True, format='%(created)f %(message)s End')
    
    with mListener(on_click=RECORDER.on_click, on_move=RECORDER.on_move) as listener:
        listener.join()
        time.sleep(0.2)
    
    RECORDER.changeFileAfterRecord()
    RECORDER.initLogging()

    RECORDER.HotkeyStopRec = 0

    RECORDER.isRecording = 0



#Following commands are for the keyboard listener, to look for Hotkeys while script is running
def on_press(key):
    logging.info('{0} {1} {2} {3}'.format(0,0, key, 'DOWN'))
    print('{0} pressed DOWN'.format(key))

def on_functionf8(key):

    playKeyCombo = "keyboard.Key." + SETTINGS.Configured_playkey_temp.lower()
    recordKeyCombo = "keyboard.Key." + SETTINGS.Configured_recordkey_temp.lower()
    print(playKeyCombo)
    print(recordKeyCombo)

    if key==eval(playKeyCombo):
        print('playkey is pressed. I will call this TOGGLEPLAY') 
        #If playback is present, then this will stop the playback. This changes the global var number to above 1, which triggers stop playback
        if isPlayingBack == 1:
            global number
            number+=10
        #But if not playing back, we will start the playback BUT ONLY IF NOT RECORDING.
        else:
            if RECORDER.isRecording == 0:
                playButton() 
            else:
                print('Bro you are recording right now. I will not start a playback right now.')

    elif (key==eval(recordKeyCombo)):
        print('reckey pressed which is the recording hotkey.')
        try:
            #Tries to start Recording through the hotkey. If currently already recording, or playback is on, then prevent this from happening
            if isPlayingBack == 1:
                print("You're replaying a script at the moment! Can't start recording.")
            elif RECORDER.isRecording == 1:
                print("Stopping the recording, command issued.")
                RECORDER.HotkeyStopRec = 1
                RECORDER.on_move(12345, 67890)
                info2["text"]="Stopping..."
                
                #Spaz moves the mouse a very tiny amount to trigger a Recording stop. 
                Spaz = Controller()
                Spaz.move(0,1)
                Spaz.move(0,-1)

            elif RECORDER.isRecording == 0:   
                recordButton()
        except Exception as e:
            print(e)
    else:
        logging.info('{0} {1} {2} {3}'.format(0,0, key, 'UP'))

key_listener = keyboard.Listener(on_press=on_press, on_release=on_functionf8)
key_listener.start()

def on_close_window():
    if RECORDER.isRecording == 1:
        print("Stopping the recording, command issued.")
        RECORDER.HotkeyStopRec = 1
        RECORDER.on_move(12345, 67890)
        info2["text"]="Stopping..."
        root.destroy()
    elif isPlayingBack == 1:
        global number
        number += 10
        info2["text"]="Stopping playback..."
        time.sleep(1)
        root.destroy()
    else:
        info2["text"]="Stopping..."
        root.destroy()



#Loops GUI

root.protocol("WM_DELETE_WINDOW", on_close_window)
root.mainloop()


