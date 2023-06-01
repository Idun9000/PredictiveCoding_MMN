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

# Tetting the date which I will use in the naming of my logfiles
date = data.getDateStr()

# Defining columns for the dataframe
cols = ['id', 'age', 'gender']

# Defining empty dataframe
logfile = pd.DataFrame(columns = cols)

logfile = logfile.append({
            'id':ID,
            'age':Age,
            'gender': Gender},ignore_index=True) 

# Defining window to show stimuli
win = visual.Window(fullscr=True, color = "black")

# Getting video files
video1 = os.path.join('video','button_press_sound.avi')
video2 = os.path.join('video','button_press_no_sound.avi')
video3 = os.path.join('video','no_press_no_sound_2.avi')
video4 = os.path.join('video','no_press_w_sound.avi')

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
    
    while mov.status != visual.FINISHED:
        frameCounter += 1
        triggerSent = False
        mov.draw()
        if frameCounter == 1 and not triggerSent:
            win.callOnFlip(setParallelData, trigger_no)
            triggerSent = True
        if triggerSent:
            win.callOnFlip(setParallelData, 0)
            triggerSent = False
        win.flip()
    mov.seek(0)

triggerSent = False

for trial in range(20):
    prob = random.randrange(0,100)
    print(prob)
    
    if prob < 80:
        PlayMovie(mov1, 11)
        
    elif prob > 80 and prob < 86:
        PlayMovie(mov2, 12)
        
    elif prob > 86 and prob < 93:
        PlayMovie(mov3, 13)
        
    elif prob > 93 and prob < 100:
        PlayMovie(mov4, 14) 
    
    key = get_keypress()
    if key == 'q':
        shutdown()
     
win.close()
core.quit()
    
# Logfile directory
cwd = os.getcwd()
logfile_path = os.path.join(cwd, "logfiles")

# Logfile name
logfile_name = "{}logfile_{}_{}.csv".format(logfile_path, ID, date)

# Save logfile
logfile.to_csv(logfile_name)
