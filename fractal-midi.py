

#!/usr/bin/env python

from midiutil import MIDIFile
import math
import numpy as np
import sys


tracks = 4

def frequency_to_note(f):
    if(f > 0):
        return math.floor(12*math.log(f/440.0, 2))+57
    else:
        print('<= zero encountered in frequency_to_note')
        return 57


def  fractal_midi(transformations,   midi, totalTime, depth, time1, time2, freq1, freq2, amp1, amp2):
    if(depth <=0):
  
        
        # freq = freq1 - track*(est_max/tracks)

        #factor = 2
        #freq = factor*freq1
        #note = int(frequency_to_note(freq))
        note = freq1
        est_max = 140
        est_min = 10
        track = math.floor(((note - est_min)/est_max)*tracks) # split midi notes across tracks
       
        tuning = [(note, int(freq1))]
        #MyMIDI.changeNoteTuning(0, tuning, tuningProgam=0)
        note += 36 - 24*track


        print(track, note)
        if(note > 0):
            midi.addNote(track, 9, int(note), int(time1*totalTime), int((time2 - time1)*totalTime), int(amp1*100))

        return
    
    twidth = time2 - time1
    awidth = amp2 - amp1
    fwidth = freq2 - freq1
    for t in transformations:
        fractal_midi(transformations, midi, totalTime, depth - 1, time1 + twidth*t[0], time1 + twidth*t[1], freq1 + t[2], freq2*t[3], amp1 + awidth*t[4], amp1 + awidth*t[5])


track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 120   # In BPM
volume   = 100  # 0-127, as per the MIDI standard


tempo = 120
ticks_per_quarternote = 960

MyMIDI = MIDIFile(tracks, removeDuplicates=True, deinterleave=False,ticks_per_quarternote=ticks_per_quarternote,eventtime_is_ticks=True) 
MyMIDI.addTempo(track, time, tempo)



####################### futz here ####################
measures = 100

transformations = [
	[0,     0.5,    -7,   1,     0,      0.75],
    [0.5,     1,    12,   1,      0.75,   0],
	#[0,  0.5,      0,      0.5,      1,     0.75],
    [1,  0.75,      19,      0.5,      0.5,     0.75],
]

depth=7
freq1 =0
freq2 = 0
t1=0
t2=1
amp1=0
amp2=1

totalTime = ticks_per_quarternote*4*measures
for track in range(tracks):
    MyMIDI.addNote(track, 0, 1, totalTime-1, 1, 1)



fractal_midi(transformations,  MyMIDI, totalTime, depth, t1, t2,freq1,freq2, amp1, amp2)

with open("fractal-midi.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)