#!/usr/bin/env python
from psychopy import visual, event, core

class Instructions():
       
    instructionText = []
    
    txt = 'This is the end of the practice task.\n\nIf you have any questions, please ask the experimenter now. Otherwise you can press any key to start the main task.'
    instructionText.append(txt)

    continueText = 'Press any key to continue'
    
    def __init__(self, win):
        
        self.win = win
        self.instructions = visual.TextStim(win, pos=[0,0],text='Press any key to start')
        self.instructions.setHeight(.08)
        self.cont = visual.TextStim(win, pos=[1,-1], text = 'Press any key to continue', alignHoriz = 'right', alignVert = 'bottom')
        self.cont.setHeight(.08)
    
    def Run(self):
        # the following will loop through the instructionText array
        
        for i in range(len(self.instructionText)):
            self.instructions.setText(self.instructionText[i])
            self.instructions.draw()
            if(i < len(self.instructionText) - 1):
                self.cont.draw()
            self.win.flip() #to show our newly drawn 'stimuli'
            event.waitKeys()
