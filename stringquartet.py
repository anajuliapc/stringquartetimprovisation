# -*- coding: utf-8 -*-

from simpleOSC import initOSCClient, initOSCServer, setOSCHandler, sendOSCMsg, closeOSC, createOSCBundle, sendOSCBundle, startOSCServer
import sys, time
from pprint import pprint
from random import choice
import Tkinter, tkSnack
import tonegenerator as tg
import subprocess

def build_dict(notes):
    """
    Build a dictionary from the notes.
 
    (note1, note2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}

    length = len(notes)

    for i, note in enumerate(notes):

        key = note

        if key not in d:
           d[key] = []

	    # Put values to each key

        # Itself is always a possibility
        value = notes[i]        
        d[key].append(value)

        # 3 notes before 
        try:
            value = notes[i-3]
            d[key].append(value)
        except IndexError:
            pass

        try:
            value = notes[i-2]
            d[key].append(value)
            d[key].append(value)            
        except IndexError:
            pass

        try:
            value = notes[i-1]
            d[key].append(value)
            d[key].append(value)
            d[key].append(value)            
        except IndexError:
            pass

        # 3 notes after
        try:
            value = notes[i+1]
            d[key].append(value)
            d[key].append(value)
            d[key].append(value)            
        except IndexError:
            pass

        try:
            value = notes[i+2]
            d[key].append(value)
            d[key].append(value)
        except IndexError:
            pass

        try:
            value = notes[i+3]
            d[key].append(value)
        except IndexError:
            pass

    return d
 
 
def generate_music(d):
    li = [key for key in d.keys()]

    key = choice(li)

    li = []

    current = key
    li.append(current)

    timeout = time.time() + 0.00015   # 0.01 miliseconds from now
    while True:

        if time.time() > timeout:
            break
        try:
            next = choice(d[key])
        except KeyError:
            print("erro")
            break
        li.append(next)
        key = next
        current = key
 
    return li
 
 
def main():

    initOSCClient('127.0.0.1', 9001)
    sendOSCMsg("/start")

    fname = sys.argv[1]
    f = open(fname, "rt")
    text = f.read()
 
    root = Tkinter.Tk()
    
    # have to initialize the sound system, required!!
    tkSnack.initializeSnack(root)
    # set the volume of the sound system (0 to 100%)
    tg.setVolume(100)

    tg.translateNote('A4')

    notes = text.split()
    d = build_dict(notes)

    sent = generate_music(d)

    j = 0
    for i in sent:  
        # Nota mais grave vai pro cello
        i = tg.translateNote(i)        
        # Sua terça vai pro violino 1
        j = i*(4/5)
        # Sua quinta vai pra viola
        k = j*(3/2)
        # E sua oitava pro violino 2
        l = i*2
        sendOSCMsg("/cello", [i]) 
        sendOSCMsg("/viola", [j])
        sendOSCMsg("/violin1", [k]) 
        sendOSCMsg("/violin2", [l])
               
        time.sleep(0.5)

#    tg.soundStop()
    
    sendOSCMsg("/cello", [0]) 
    sendOSCMsg("/viola", [0])       
    sendOSCMsg("/violin1", [0]) 
    sendOSCMsg("/violin2", [0]) 

    sendOSCMsg("/stop")
    closeOSC()  

    root.withdraw()
 
####################
 
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: provide an input corpus file.")
        sys.exit(1)
    # else
    main()
