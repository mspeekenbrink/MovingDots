#!/usr/bin/env python
from psychopy import visual, event, core

class Instructions():
    
    def __init__(self, win, practice, ntrials, blockSize):
        
        instructionText = []
        txt = 'In this experiment you will be required to decide whether a cloud of dots is moving to the right, or to the left of the screen.\n\n'
        txt += 'On each trial, you will need to indicate your response by pressing one of two buttons. Use your right index finger to press the right '
        txt += 'button, if you have decided that the dots are moving to the right. Likewise, if you have decided that the dots are moving to the left, '
        txt += 'use your left index finger to press the left button.'
        instructionText.append(txt)

        txt = 'On some trials, before the moving dots are shown, the word "FAST" will appear on the screen. In this case, you should try to respond '
        txt += 'as quickly as possible.\n\nOn other trials, the word "ACCURATE" will appear. In this case, please try to respond as accurately as possible.'
        instructionText.append(txt)

        txt = 'At the end of each trial, you will receive feedback that will depend both on your performance and on the instructions '
        txt += '(i.e. "FAST" or "ACCURATE"). After a trial emphasizing speed, we will let you know whether you were "in time" or "too slow". '
        txt += 'After a trial emphasizing accuracy, we will let you know whether your response was "correct" or "incorrect".\n\n' 
        txt += 'Based on the feedback you receive, you should try to adapt your responses to be as "correct" or "in time" as possible.' 
        instructionText.append(txt)
        
        txt = 'The task involves completion of a total of ' + str(ntrials) + ' trials. This should take about 20 minutes. '
        txt += 'Please try to concentrate on the task for the total duration.\n\n'
        txt += 'Every ' + str(blockSize) + ' trials, you will be allowed to rest for a short period.\n\n'
        
        if practice == True:
            txt += 'To familiarize yourself with the task, you can now try a small number of practice trials.'
        else:
            txt += 'If you have any questions, please ask the experimenter now. Otherwise you can press any key to start the task.'

        instructionText.append(txt)

        self.instructionText = instructionText
        self.continueText = 'Press any key to continue'
        
        self.win = win
        self.instructions = visual.TextStim(win, pos=[0,0],text='Press any key to start')
        self.instructions.setHeight(.07)
        self.cont = visual.TextStim(win, pos=[1,-1], text = 'Press any key to continue', alignHoriz = 'right', alignVert = 'bottom')
        self.cont.setHeight(.07)
    
    def Run(self):
        self.instructions.draw()
        self.win.flip()#to show our newly drawn 'stimuli'
        #pause until there's a keypress
        event.waitKeys()
        # the following will loop through the instructionText array
        
        for i in range(len(self.instructionText)):
            self.instructions.setText(self.instructionText[i])
            self.instructions.draw()
            if(i < len(self.instructionText)):
                self.cont.draw()
            self.win.flip() #to show our newly drawn 'stimuli'
            event.waitKeys()
