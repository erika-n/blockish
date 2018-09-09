

#!/usr/bin/env python

from midiutil import MIDIFile
import math
import numpy as np
import sys


tracks = 4

def  fractal_midi(transformations,   midi, totalTime, depth, time1, time2, freq1, freq2, amp1, amp2):
    if(depth <=0):
  
        
        track = math.floor(freq1*(tracks - 1)) # split midi notes across tracks

        note = freq1 + freq2
        
        track = math.floor(note / 60) % tracks
        note = note % 60 
        note += 36
        

        print(freq1, note, track)
        midi.addNote(track, 9, int(note), int(time1*totalTime), int(abs(time2 - time1)*totalTime), int(amp1*100))

        return
    

    
    twidth = time2 - time1
    awidth = amp2 - amp1
    fwidth = freq2 - freq1
    for t in transformations:
        fractal_midi(transformations, midi, totalTime, depth - 1, time1 + twidth*t[0], time1 + twidth*t[1], freq1+t[2], freq2- fwidth*t[3], amp1 + awidth*t[4], amp1 + awidth*t[5])


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
measures = 300

transformations = [

	# [0.2501,      0.01,    12,   1,     0,      0.75],
    # [0.25,     0.501,       0,   1,      0.75,   0],
	# [0.75,        0.25,      7,      0.5,      1,     0.75],
    # [0.75,         0.999,      0,      0.5,      0.5,     0.75],

	[0,        0.25,        12,        0,     0,      0.5],
    [1,        0.5,       12,        0,      0.5,   0],
	[0.5,        1,      7,      0,      0.75,     0.5],
    [0.5,         0,      7,        0,      0.5,     0.75],    
    #[0.75,         1,      0,        2,      0.5,     0.75],

# 	[0.5, 1,        1,   0.5,   0, 0.5],
# 	[0, 0.5,       0.5,0.25,      0.5, 0],
#     [0.25,  0.75,   0.75,0.25,          1,     0.5],
#    # [0,  0.75,      1,     0,   1,     0.5],
]


depth=7
freq1 =0
freq2 =0
t1=0
t2=1
amp1=0
amp2=1

totalTime = ticks_per_quarternote*4*measures
for track in range(tracks):
    MyMIDI.addNote(track, 0, 1, totalTime-1, 1, 1)




fractal_midi(transformations,  MyMIDI, totalTime, depth, t1, t2,freq1,freq2, amp1, amp2)

print("writing file...")
with open("fractal-midi.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)