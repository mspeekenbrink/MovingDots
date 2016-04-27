#!/usr/bin/env python
import random, math, array
from psychopy import visual, event, core, data, gui, misc, parallel
from itertools import product
import SpeedAccuracyInstructions, StartMainInstructions, SpeedAccuracyTaskParallelPort

speedTime = '500'
trialTime = '1500'
myResolution = (1300,800)
responseKeys = ['f','j']
# change to 
# responseKeys = ['b','a']
# for response box owned by Marjan Jahanshahi

# change below to set specific port address, for instance to:
# myPort = parallel.ParallelPort(address=0x0378)
myPort = parallel.ParallelPort()

#create a window to draw in
myWin =visual.Window(myResolution, allowGUI=True,
    bitsMode=None, units='norm', winType='pyglet', color=(-1,-1,-1))

# Admin
expInfo = {'subject':'test','date':data.getDateStr(),'include practice':True,'test mode':False,'speed time':speedTime,'trial time':trialTime}

#present a dialogue to change params
ok = False
while(not ok):
    dlg = gui.DlgFromDict(expInfo, title='Moving Dots', fixed=['date'],order=['date','subject','include practice','test mode','speed time','trial time'])
    if dlg.OK:
        misc.toFile('lastParams.pickle', expInfo)#save params to file for next time
        ok = True
    else:
        core.quit()#the user hit cancel so exit

speedTime = float(int(expInfo['speed time']))/1000
trialTime = float(int(expInfo['trial time']))/1000
practiceTask = expInfo['include practice']
debug = expInfo['test mode']

# setup trials
if debug == True:
    nsubblocks = 1
    nblocks = 1
    blockSize = 24
    ntrials = 28
else:
    nsubblocks = 5
    nblocks = 4
    blockSize = 120
    ntrials = 24 * nsubblocks * nblocks + 24 * nsubblocks

# setup data file
fileName = 'Data/' + expInfo['subject'] + expInfo['date'] + '.csv'
dataFile = open(fileName, 'w') #a simple text file with 'comma-separated-values'
dataFile.write('subject = ' + str(expInfo['subject']) + "; date = " + str(expInfo['date']) + "; speed time = " + str(expInfo['speed time']) + "; trial time = " + str(expInfo['trial time']) + '\n')
dataFile.close()
   
#trialClock = core.Clock()
instr = SpeedAccuracyInstructions.Instructions(myWin,practiceTask,ntrials,blockSize)
instr.Run()


if practiceTask == True:
    # practice task has 2*2*6*1 = 24 trials
    tids = list(product([0,1],[0,1],[.05,.1,.15,.25,.35,.5])) * 1
    random.shuffle(tids)
    practice = SpeedAccuracyTaskParallelPort.Task(myWin,fileName,tids,len(tids) + 1,speedTime,trialTime,myPort,responseKeys)
    practice.Run()
    dataFile = open(fileName, 'a') #a simple text file with 'comma-separated-values'
    dataFile.write('End Practice\n')
    dataFile.close()

    instr = StartMainInstructions.Instructions(myWin)
    instr.Run()
    
    
# following returns a list with: direction, instructions, coherence
tids = list(product([0,1],[0,1],[.05,.1,.15,.25,.35,.5])) * nsubblocks
allTids = []
for i in range(nblocks):
    random.shuffle(tids)
    allTids += tids
# add 100% coherence block
if debug == True:
    tids = list(product([0,1],[0,1],[1.0]))
else:
    tids = list(product([0,1],[0,1],[1.0])) * 6 * nsubblocks 
for i in range(3):
    random.shuffle(tids)
    allTids += tids

task = SpeedAccuracyTaskParallelPort.Task(myWin,fileName,allTids,blockSize,speedTime,trialTime,myPort,responseKeys)
task.Run()

endText = "This is the end of the experiment \n \n"
endText += "Thank your for your participation."
end = visual.TextStim(myWin, pos=[0,0],text=endText)
end.draw()
myWin.flip()

done = False
while not done:
    for key in event.getKeys():
        if key in ['escape','q']:
            done = True
            core.quit()
