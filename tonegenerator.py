# play a note of a given frequency and duration via the PC sound card
# needs Python module  tkSnack  developed at KTH in Stockholm, Sweden
# free download: snack229-py.zip
# from: http://www.speech.kth.se/snack/
# on my system I copied tkSnack.py to D:\Python24\Lib and the folder snacklib to D:\Python24\tcl
# tested with Python24     vegaseat     28oct2005

import Tkinter
import tkSnack

def setVolume(volume=50):
    """set the volume of the sound system"""
    if volume > 100:
        volume = 100
    elif volume < 0:
        volume = 0
    tkSnack.audio.play_gain(volume)

def playNote(freq, duration):
    """play a note of freq (hertz) for duration (seconds)"""
    snd = tkSnack.Sound()
    filt = tkSnack.Filter('generator', freq, 30000, 0.0, 'sine', int(11500*duration))
    snd.stop()
    snd.play(filter=filt, blocking=1)

def soundStop():
    """stop the sound the hard way"""
    try:
        root = root.destroy()
        filt = None
    except:
        pass

# Turn table of notes into dictionary
def createDict():
    notesDict = {}
    with open('noteTable.txt','r') as notes:        
        for line in notes:
            freq, letter = line.split('    ')

            letter = letter.rstrip()

            notesDict[letter] = freq    

    return notesDict

def translateNote(note):
    # translate given note to frequency
    d = createDict()

    if note in d.keys():
        key = note
        freq = (float)(d[key])
    else:
        print("Error.")

    return freq
