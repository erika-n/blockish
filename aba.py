

#!/usr/bin/env python

from midiutil import MIDIFile
import math
import numpy as np
import sys
import random

# starting with a simple pattern
# recurse such that
# for A
# A => ABA


scale = [60, 62, 64, 65, 67, 69, 71, 72]

def aba_pattern(midi, letter, noteIndex, time1, time2, totalTime, depth):
    if(depth <= 0):
        amp = 80
        
        
        midi.addNote(track, 1,scale[noteIndex], int(time1*totalTime),  int(abs(time2 - time1)*totalTime), amp)
        return


    twidth = time2- time1
    if(letter == 'C'):
        noteIndex = ((noteIndex + random.choice([3, 4])) % len(scale) )
    if (letter == 'A' or letter == 'C'):
        aba_pattern(midi, "A",noteIndex, time1, time1 + twidth/4, totalTime, depth -1)
        bNoteIndex = ((noteIndex + random.choice([4])) % len(scale) )
        print("bNoteIndex: ", bNoteIndex)    
        aba_pattern(midi, "A",noteIndex, time1, time1 + twidth/4, totalTime, depth -1)
        aba_pattern(midi, "B", bNoteIndex, time1 + twidth/4, time1 + 3*twidth/4, totalTime, depth -1)
        aba_pattern(midi, "C", noteIndex, time1 + 3*twidth/4, time2, totalTime, depth -1)
         
        
    elif (letter == 'B'):
        aNoteIndex = ((noteIndex + random.choice([2])) % len(scale) )
        print("aNoteIndex", aNoteIndex)
        aba_pattern(midi, "B", noteIndex, time1, time1 + twidth/2, totalTime, depth -1)
        aba_pattern(midi, "C", aNoteIndex, time1 + twidth/2, time1 + 3*twidth/4, totalTime, depth -1)
        aba_pattern(midi, "B", noteIndex, time1 + 3*twidth/4, time2, totalTime, depth -1)
        aba_pattern(midi, "C", noteIndex, time1 + 3*twidth/4, time2, totalTime, depth -1)

measures =10

tracks =1
track    = 0
channel  = 0
time     = measures*4    # In beats
duration = 1    # In beats
tempo    = 120   # In BPM
volume   = 100  # 0-127, as per the MIDI standard


tempo = 120
ticks_per_quarternote = 100


MyMIDI = MIDIFile(tracks, removeDuplicates=True, deinterleave=False,ticks_per_quarternote=ticks_per_quarternote,eventtime_is_ticks=True) 
MyMIDI.addTempo(track, time, tempo)




totalTime = ticks_per_quarternote*4*measures

aba_pattern(MyMIDI, "A", 0, 0, 1, totalTime,4)

with open("fractal-midi.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)