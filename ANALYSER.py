import time
import fileLoader


#ANALYSE loads the User save file, checks if valid, stores info in a dictionary, and returns the dictionary
def ANALYSE():
    SetLoad = fileLoader.currentFilename
    count = 0 
    with open(SetLoad, 'r') as f:
        #Reads the first line to see the Initial Starting Time
        FirstLine = f.readline()
        InitialTime = FirstLine.split()[0]
        clickHistory = {}

        for line in f:
            count+=1
            (timestamp, posx, posy, buttonName, press, End) = line.split(' ')
            #For each line after the first, the delay will be the Difference in Recorded Time between the current and previous line. The delay for the first line is a fixed 0.5
            if count > 1:
                Delay = float(timestamp) - clickHistory[count - 1]['timestamp']
            else:
                Delay = 0

            #Adds a dictionary entry for each line in the Text File
            clickHistory[count] = {'delay':float(Delay), 'whichButton':buttonName, 'x':int(posx), 'y':int(posy), 'timestamp':float(timestamp), 'press':press, }
    return clickHistory

#ANALYSEVALID checks if the file is a valid maus script. Used when user loads a file
def ANALYSEVALID(userfile):
    count = 0 
    with open(userfile, 'r') as f:
        #Reads the first line to see the Initial Starting Time
        FirstLine = f.readline()
        InitialTime = FirstLine.split()[0]
        TEMPclickHistory = {}

        for line in f:
            count+=1
            (timestamp, posx, posy, buttonName, press, End) = line.split(' ')
            #For each line after the first, the delay will be the Difference in Recorded Time between the current and previous line. First line delay is fixed 0.5 for smoothness.
            if count > 1:
                Delay = float(timestamp) - TEMPclickHistory[count - 1]['timestamp']
            else:
                Delay = 0
            #Adds a dictionary entry for each line in the Text File
            TEMPclickHistory[count] = {'delay':float(Delay), 'whichButton':buttonName, 'x':int(posx), 'y':int(posy), 'timestamp':float(timestamp), 'press':press, }
    return TEMPclickHistory




#The Dictionary is now ready to be used

#  MouseLog[currentAct] = {'delay':delay, 'type':button, 'action':'press', 'posx':x, 'posy':y}
