import tkinter as tk
from tkinter import messagebox
import time


###### User Chosen Settings: ####

#Sampling Method:
User_sampling_method = "Hybrid"
User_looping_method = "Single"
User_playkey_temp = "F12"
User_recordkey_temp = "F8"
User_antiban = 0

#Configured Settings. THESE SHOULD BE THE ONES THE MAIN APPLICATIONS USE.
Configured_sampling_method = None
Configured_looping_method = None
Configured_playkey_temp = None
Configured_recordkey_temp = None
Configured_antiban = None

#Default Resets incase something went wrong
dUser_sampling_method = "Hybrid"
dUser_looping_method = "Single"
dUser_playkey_temp = "F12"
dUser_recordkey_temp = "F8"
dUser_antiban = 0



def SamplingMethod():
    if Configured_sampling_method == "Fidelity":
        return 5
    elif Configured_sampling_method == "Efficiency":
        return 20
    elif Configured_sampling_method == "Hybrid":
        return 12
    else:
        print('NAH CRIP DIDNT WORK')


def IsSaveValid():
    openCheck = open("settings.48", "r")
    SettingsFIRSTLINE = openCheck.readline()
    print(SettingsFIRSTLINE + 'magragra')
    (samplingS, loopingS, playkeyS, recordkeyS, antibanS) = SettingsFIRSTLINE.split(' ')

    openCheck.seek(0)
    openCheck.close()

    validCheck = 0
    if (samplingS == "Fidelity" or samplingS == "Hybrid") or samplingS == "Efficiency":
        validCheck += 10
    if (loopingS == "Single" or loopingS == "Infinite") or loopingS == "Custom":
        validCheck += 10
    if playkeyS[0] == "F" and (len(playkeyS) <= 3):
        validCheck += 10
    if recordkeyS[0] == "F" and (len(recordkeyS) <= 3):
        if not playkeyS == recordkeyS:
            validCheck += 10
    if eval(antibanS) == 1 or eval(antibanS) == 0:
        validCheck += 10
    
    if validCheck == 50:
        return True
    else:
        return False



def loadUserSettings():
    global Configured_sampling_method, Configured_looping_method, Configured_playkey_temp, Configured_recordkey_temp, Configured_antiban
    
    if IsSaveValid():
        openCheck = open("settings.48", "r")
 
        SettingsFIRSTLINE = openCheck.readline()
        (samplingS, loopingS, playkeyS, recordkeyS, antibanS) = SettingsFIRSTLINE.split(' ')

        openCheck.seek(0)
        openCheck.close()

        Configured_sampling_method = samplingS
        Configured_looping_method = loopingS
        Configured_playkey_temp = playkeyS
        Configured_recordkey_temp = recordkeyS
        Configured_antiban = antibanS
        print('Everything should have loaded well.')

    else:
        print('Save was not valid. We gonna roll with the defaults.')
        resettingDefaults()

        openCheck = open("settings.48", "r")
 
        SettingsFIRSTLINE = openCheck.readline()
        (samplingS, loopingS, playkeyS, recordkeyS, antibanS) = SettingsFIRSTLINE.split(' ')

        openCheck.seek(0)
        openCheck.close()

        Configured_sampling_method = samplingS
        Configured_looping_method = loopingS
        Configured_playkey_temp = playkeyS
        Configured_recordkey_temp = recordkeyS
        Configured_antiban = antibanS

        tk.messagebox.showwarning("User Settings Generation", "Your settings are missing or invalid. Default settings are applied.\n\nIf this is your first time launching, please dismiss this message\n")
        print("Default settings were applied.")
    
    #Need to somehow REFRESH the hotkeys.


def UserPressedSave():
    #Makes a new file and saves the settings.
    settingsFile = open("settings.48", "w")
    settingsFile.write("{} {} {} {} {}".format(User_sampling_method, User_looping_method, User_playkey_temp, User_recordkey_temp, User_antiban))
    settingsFile.seek(0)
    settingsFile.close()

    #Now, loads the file. But first, checks if file is valid
    IsSaveValid()
    
    #Then, will re-access the file and add
    loadUserSettings()

def resettingDefaults():
    #Makes a new file and saves the settings.
    settingsFile = open("settings.48", "w")
    settingsFile.write("{} {} {} {} {}".format(dUser_sampling_method, dUser_looping_method, dUser_playkey_temp, dUser_recordkey_temp, dUser_antiban))
    settingsFile.seek(0)
    settingsFile.close()

def loopingPlaybacks():
    if Configured_looping_method == "Single" or Configured_looping_method == "Custom":
        return 1
    elif Configured_looping_method == "Infinite":
        return 99999
    else:
        return 1




    

