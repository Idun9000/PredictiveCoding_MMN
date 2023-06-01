# Forsøg loop

# Loading packages
from psychopy import core, visual, event, gui, data
import pandas as pd
from psychopy import parallel
import platform
import os
import random
from triggers import setParallelData

# Defining dialogue prompt
dialog = gui.Dlg(title = "EEG Experiment")
dialog.addField("Participant ID:")
dialog.addField("Age:")
dialog.addField("Gender:", choices = ["female", "male", "other"])
dialog.show()
if dialog.OK:
    ID = dialog.data[0]
    Age = dialog.data[1]
    Gender = dialog.data[2]
elif dialog.Cancel:
    core.quit()

oddballs = [12,12,12,13,13,13,14,14,14]
minutes = 1
standards = [3,9]
stand_trigger = 100

# Telling the date which I will use in the naming of my logfiles
date = data.getDateStr()

dir = "/Users/tildeidunsloth/Desktop/Cognitive Neuroscience/neuro_exam/EEG_exp"

# Defining columns for the dataframe
columns = ['id', 'age', 'gender']

# Defining empty dataframe
logfile = pd.DataFrame(columns = columns)

if not os.path.exists('video'):
    if not os.path.exists(os.path.join(dir,"logfiles")):
        os.makedirs(os.path.join(dir,"logfiles"))
        logpath = os.path.join(dir,"logfiles")
    elif os.path.exists("logfiles"):
        os.makedirs("logfiles")
        logpath = "logfiles"

logfilename = os.path.join("logfiles","logfile_{}_{}.csv".format(ID, date))


# Defining window to show stimuli
win = visual.Window(fullscr=True, color = "black")

# Getting video files
if not os.path.exists("video"):
    videodir = os.path.join(dir,"video")
else:
    videodir = "video"

video1 = os.path.join(videodir,'button_press_sound.avi')
video2 = os.path.join(videodir,'button_press_no_sound.avi')
video3 = os.path.join(videodir,'no_press_no_sound_2.avi')
video4 = os.path.join(videodir,'no_press_w_sound.avi')

# Creating video object
mov1 = visual.MovieStim3(win, video1)
mov2 = visual.MovieStim3(win, video2)
mov3 = visual.MovieStim3(win, video3)
mov4 = visual.MovieStim3(win, video4)

def get_keypress():
    keys = event.getKeys()
    if keys:
        return keys[0]
    else:
        return None

def shutdown():
    win.close()
    core.quit()


def PlayMovie(mov, trigger_no):
    mov.play()
    frameCounter = 0
    triggerSent = False
    while mov.status != visual.FINISHED:
        frameCounter += 1
        mov.draw()
        if frameCounter == 1 and not triggerSent:
            win.callOnFlip(setParallelData, trigger_no)
            triggerSent = True
            print(trigger_no)
        win.flip()
        if triggerSent:
            win.callOnFlip(setParallelData, 0)
            triggerSent = False
            print(0)
    mov.seek(0)

for trial in range(minutes):
    oddballs = random.shuffle(oddballs)
    for sequence in oddballs:
        counter = 1
        for standard in random.randrange(standards[0], standards[1]):
            PlayMovie(mov1, stand_trigger+counter)
            counter = counter + 1
            key = get_keypress()
            if key == 'q':
                shutdown()
        if sequence == 12:
            mov_spec = mov2
        elif sequence == 13:
            mov_spec = mov3
        elif sequence == 14:
            mov_spec = mov4
        PlayMovie(mov_spec, sequence)
        key = get_keypress()
        if key == 'q':
            shutdown()     
win.close()


# logfile append
logfile = logfile.append({
        'id':ID,
        'age':Age,
        'gender': Gender},ignore_index=True) 

core.wait(0.5)

# Save logfile
logfile.to_csv(logfilename)
