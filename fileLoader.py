from pynput import mouse
from pynput.mouse import Button, Controller, Listener
import logging
import time
import threading
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
import ANALYSER
import shutil
startTime=time.time()

currentFilename = None

def fileToLoad():
    Filename = filedialog.askopenfilename(initialdir = "/", title="Select a Script", filetypes = [('MAUS48 File', '*.maus')])

    try:
        with open(Filename, 'r') as f:
            #Reads the first line to see the Initial Starting Time
            LineOne = f.readline()
            if len(LineOne)==0:
                tk.messagebox.showwarning("Warning", "The file you selected was likely empty (the first line seemed empty, which is odd).\n\nNothing interesting happens.")
            else:
                try:
                    ANALYSER.ANALYSEVALID(Filename)
                    global currentFilename
                    currentFilename = Filename
                    tk.messagebox.showwarning("Something Interesting Happens", "SUCCESSFULLY IMPORTED:\n\n{0}\n".format(currentFilename))
                except:
                    tk.messagebox.showwarning("Warning", "The file you selected is invalid. Please double check your file.\n\nNothing interesting happens.")
    except:
        tk.messagebox.showwarning("Cancelled", "Nothing interesting happens.\n\nHopefully that was intended.\n")

#logging.basicConfig(filename=currentFilename, level=logging.DEBUG, format='%(created)f %(message)s End')

def fileToSave():
    TemporarySave = currentFilename
    UserDestination = filedialog.asksaveasfilename(initialdir = "/", title="Save Script As", filetypes=[("Maus48 File", "*.maus")])
    print(UserDestination)
    try:
        if len(UserDestination)>0:
            shutil.copyfile(TemporarySave, UserDestination+'.maus')
            tk.messagebox.showwarning("Complete", "Your script was saved to:\n\n{0}.maus\n".format(UserDestination))
        else:
            tk.messagebox.showwarning("Warning", "Nothing interesting happens.\n\n(hopefully you cancelled otherwise there is an issue)")
    except:
        tk.messagebox.showwarning("Warning", "Nothing interesting happens.\n\n(hopefully you cancelled otherwise there is an issue)")
