

#!/usr/bin/env python

from midiutil import MIDIFile
import math
import numpy as np
import sys


tracks = 4
octaves = 4




def  fractal_midi(transformations,   midi, totalTime, depth, time1, time2, freq1, freq2, amp1, amp2):
    if(depth <=0):

        scale = [0,2,  5,7, 9]
        note = freq1 +freq2 
        track = int(note % tracks)
        note = note / tracks

        note = 48 + scale[int(note % len(scale))] + 12* (math.ceil(note/(len(scale)))% octaves)
        
        print(freq1, note, track, int(time1*totalTime))
        


        if(note > 0 and note < 100):
            if(time2 -time1 < 0):
                time1 -= (time2 -time1)
            midi.addNote(track, 9, int(note), int(time1*totalTime), int(abs(time2 - time1)*totalTime), int(amp1*100))

        return
    
    twidth = time2 - time1
    awidth = amp2 - amp1
    fwidth = freq2 - freq1
    for t in transformations:
        fractal_midi(transformations, midi, totalTime, depth - 1, time1 + twidth*t[0], time1 + twidth*t[1], freq1 + t[2], freq2*t[3], amp1 + awidth*t[4], amp1 + awidth*t[5])


measures = 300

track    = 0
channel  = 0
time     = measures*4    # In beats
duration = 1    # In beats
tempo    = 120   # In BPM
volume   = 100  # 0-127, as per the MIDI standard


tempo = 120
ticks_per_quarternote = 960


MyMIDI = MIDIFile(tracks, removeDuplicates=True, deinterleave=False,ticks_per_quarternote=ticks_per_quarternote,eventtime_is_ticks=True) 
MyMIDI.addTempo(track, time, tempo)



####################### futz here ####################


# transformations = [
# 	[0.2501,      0.01,    12,   1,     0,      0.75],
#     [0.25,     0.501,       0,   1,      0.75,   0],
# 	[0.75,        0.25,      7,      0.5,      1,     0.75],
#     [0.75,         0.999,      0,      0.5,      0.5,     0.75],
# ]

transformations = [
	# [0.25,      0,    0,   0.5,     0,      0.75],
    # [0,     0.5,       0.5,   1,      0.75,   0],
	# [0.75,        0.25,      0.25,      0.75,      1,     0.75],
    # [0.5,         1,      0.75,      0.25,      0.5,     0.75],

#sierpinsky triad:
	# [1, 0.5,        0,  0.5, 0.5, 0],
	# [0.5, 0,     0, 0.5, 0.25, 0.75],
    # [0.25,  0.75,   1, 0.5,0.5,     0.75],


	# [1, 0.5,        0,  2, 0.5, 0],
	# [0.5, 0,        0, 4, 0.25, 0.75],
    # [0.25,  0    ,   0, 8,0.5,     0.75],


	[0.25,      0,          0,   2,     0,      0.75],
    [0,     0.5,           0,   4,      0.75,   0],
	[0.75,        0.25 ,      0,      3,      1,     0.75],
    [0.5,         1,       0.,      5,      0.5,     0.75],

    # #[0,  0.5,      1,     0.5,0,     0.5],
]


depth=9
freq1 =0
freq2 = 1
t1=0
t2=1
amp1=0
amp2=1

totalTime = ticks_per_quarternote*4*measures

fractal_midi(transformations,  MyMIDI, totalTime, depth, t1, t2,freq1,freq2, amp1, amp2)

with open("fractal-midi.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)