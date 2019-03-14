

#!/usr/bin/env python

from midiutil import MIDIFile
import math
import numpy as np
import sys
import random

a = 440
tracks = 4
def freqToMid(f):
    return int(12*math.log(f*(32/a), 2) + 9)

def  fractal_midi(transformations,   midi, totalTime, depth, time1, time2, freq1, freq2, amp1, amp2):
    if(depth <=0):

        track = math.floor(freq1/(100)) 
        note = freqToMid(freq1)

        #print(note)

        #note -= track*36
        note += 18
        
        #print(note, track, time1, int(time1*totalTime), int(amp1*100), track)
        if(note > 10 and note < 100 and track < tracks):
           
            if(time2 -time1 > 0):
                time1 -= abs(time2 -time1)
         
            if(time1 > 0):
                midi.addNote(track, 9, int(note), int(time1*totalTime), int(abs(time2 - time1)*totalTime), int(amp1*70))
           
        return
    
    twidth = time2 - time1
    awidth = amp2 - amp1
    fwidth = freq2 - freq1
    for t in transformations:
        r = random.randint(1, 7)
        if (r == 1):
             freq1 /=2
        elif(r == 2):
            freq1 *= 2
        fractal_midi(transformations, midi, totalTime, depth - 1, time1 + twidth*t[0], time1 + twidth*t[1], freq1 * t[2], freq2 + t[3], amp1 + awidth*t[4], amp1 + awidth*t[5])


measures = 300

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
	# [1, 0.5,        2,  0.5, 0.5, 0],
	# [0.5, 0,     4, 0.5, 0.25, 0.75],
    # [0,  0.75,   1, 0.5,0.5,     0.75],
    # [1,      0.25,       3,   -2,     0.5,      0.75],

#	[0.5, 0.25,        2,  2, 0.5, 0],
	# [0, 0.5,        2, 4, 0.25, 0.75],
    # [0,  0.5    ,   4, 8,0.5,     1],
    # [1, 0.5    ,   3, 8,0,     0.75],

    # [1, 0.5    ,   1,8, 0.5,     0],
	# [0.25,      0.75,       2,   -2,     0.5,      0.75],
    # [1,         0.75,      6,   -6,      0.25,  0],
	# [0.25,        0,      3,      -3,      0.25,     0],
    # [0.25,         1,       3,      -3,      0.5,     0],
    # [0,           0.5,      4,      -4,       1,     0.5],


    [1,         0,      2,   6,      1,         0.5],
	[0,        0.5,      3,      3,      0,     0.5],
    [0.5,         0,       4,      3,      0.5,     1],
    [1,           0.75,      3,      4,       0,     0.5],
    #[0.5,           0.75,      1,      -4,       1,     0.5],
]


depth=9
freq1 =1
freq2 = 0
t1=0
t2=1
amp1=0
amp2=1

totalTime = ticks_per_quarternote*4*measures

fractal_midi(transformations,  MyMIDI, totalTime, depth, t1, t2,freq1,freq2, amp1, amp2)

with open("fractal-midi.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)



    