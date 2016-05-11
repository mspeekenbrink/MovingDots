import random, math, array
from ParallelCodes import codes
from psychopy import core,visual,event,parallel
from itertools import product

class Task:
    cueTime = 1.5
    fixTime = 0.5
    jitterTime = 1
    preFeedbackTime = .1
    feedbackTime = .4
    postFeedbackTime = .1
    
    language = 'Spanish'
    
    def __init__(self,win,filename,tids,blockSize,speedTime,trialTime,port,responseKeys):
        
        self.datafile = open(filename, 'a') #a simple text file with 'comma-separated-values'

        self.win = win
        self.tids = tids # a list with: direction, instructions, coherence
        self.blockSize = blockSize # this is the block size seen by participants.
        self.speedTime = speedTime
        self.trialTime = trialTime
        
        self.port = port
        
        self.responseKeys = responseKeys
        
        self.typeInstructions = visual.TextStim(win,text="Ac",pos=(0,0))
        
        self.feedback = visual.TextStim(win,text="",pos=(0,0))
        
        self.blockInstructions = visual.TextStim(win,text="",pos=(0,0))
        
        self.dotPatch = visual.DotStim(win, units='pix',color=(1.0,1.0,1.0), dir= 0,
            nDots=120, fieldShape='circle', fieldPos=(0.0,0.0),dotSize=3,fieldSize=250,
            dotLife=-1, #number of frames for each dot to be drawn
            signalDots='different', #are the signal and noise dots 'different' or 'same' popns (see Scase et al)
            noiseDots='position', #do the noise dots follow random- 'walk', 'direction', or 'position'
            speed=.004, coherence=0.5)
        
        self.fixation = visual.ShapeStim(win,
            units='pix',
            lineColor='white',
            lineWidth=2.0,
            vertices=((-25, 0), (25, 0), (0,0), (0,25), (0,-25)),
            closeShape=False,
            pos= [0,0])
        
        self.trialClock = core.Clock()
        
        if self.language == 'Spanish':
            self.tinstructions = ["PRECISO","RAPIDO"]
        else:
            self.tinstructions = ["ACCURATE","FAST"]
        
        self.datafile.write('trial,type(1=Ac;2=Sp),coherence,direction(1=L;2=R),response (1=L;2=R),responsetime,feedback (1=correct;2=incorrect;3=inTime;4=tooSlow;5=noResponse)\n')
        
    def Run(self):
        
        running = True
        trial = 1
        block = 1
        
        while running:#forever
            
            self.dotPatch._dotsXY = self.dotPatch._newDotsXY(self.dotPatch.nDots)
            # set direction
            self.dotPatch.setDir(180 - self.tids[trial - 1][0]*180)
            # set instructions
            self.typeInstructions.setText(self.tinstructions[self.tids[trial - 1][1]])
            # set coherence
            self.dotPatch.setFieldCoherence(self.tids[trial - 1][2])
            
            # show instruction for cueTime
            self.typeInstructions.draw()
            self.win.flip()
            # send parallel port signal
            self.port.setData(codes.instruction_on)
            
            core.wait(self.cueTime)
            # do nothing
                
            # draw jitter time
            jitter = random.random() * self.jitterTime
            self.win.flip()
            # send parallel port signal
            self.port.setData(codes.instruction_off)
            
            #core.wait(jitter)
            
            # show fixation 500 ms
            self.fixation.draw()
            self.win.flip()
            # send parallel port signal
            self.port.setData(codes.fixation_on)
            
            core.wait(self.fixTime)
                # do nothing
                
            # jitter with blank screen
            #self.win.flip()
            core.wait(self.jitterTime - jitter)
            
            # show stimulus 1500 ms
            self.trialClock.reset()
            ttime = -1.0
            rgiven = False
            response = -1
            event.clearEvents(eventType='keyboard')
            event.clearEvents('mouse')
            
            # send parallel port signal
            self.port.setData(codes.fixation_off)
            if self.tids[trial-1] == 0:
                #self.port.setData(codes.dots_left_on)
                if self.tids[trial - 1][2] == .05:
                    self.port.setData(codes.dots_left_on_5)
                if self.tids[trial - 1][2] == .10:
                    self.port.setData(codes.dots_left_on_10)
                if self.tids[trial - 1][2] == .15:
                    self.port.setData(codes.dots_left_on_15)
                if self.tids[trial - 1][2] == .25:
                    self.port.setData(codes.dots_left_on_25)
                if self.tids[trial - 1][2] == .35:
                    self.port.setData(codes.dots_left_on_35)
                if self.tids[trial - 1][2] == .50:
                    self.port.setData(codes.dots_left_on_50)
                if self.tids[trial - 1][2] == 1.0:
                    self.port.setData(codes.dots_left_on_100)
            else:
                #self.port.setData(codes.dots_right_on)
                if self.tids[trial - 1][2] == .05:
                    self.port.setData(codes.dots_right_on_5)
                if self.tids[trial - 1][2] == .10:
                    self.port.setData(codes.dots_right_on_10)
                if self.tids[trial - 1][2] == .15:
                    self.port.setData(codes.dots_right_on_15)
                if self.tids[trial - 1][2] == .25:
                    self.port.setData(codes.dots_right_on_25)
                if self.tids[trial - 1][2] == .35:
                    self.port.setData(codes.dots_right_on_35)
                if self.tids[trial - 1][2] == .50:
                    self.port.setData(codes.dots_right_on_50)
                if self.tids[trial - 1][2] == 1.0:
                    self.port.setData(codes.dots_right_on_100)
            while (self.trialClock.getTime() < self.trialTime):
                if (rgiven == False):
                    self.dotPatch.draw()
                    self.win.flip()
                    for key in event.getKeys():
                        if key in [self.responseKeys[0],self.responseKeys[1],'escape']:
                            ttime = self.trialClock.getTime()
                            rgiven = True
                            if key in [self.responseKeys[0]]:
                                if self.tids[trial-1][0] == 0:
                                    self.port.setData(codes.response_left_correct)
                                else:
                                    self.port.setData(codes.response_left_incorrect)
                                response = 0
                            if key in [self.responseKeys[1]]:
                                if self.tids[trial-1][0] == 1:
                                    self.port.setData(codes.response_right_correct)
                                else:
                                    self.port.setData(codes.response_right_incorrect)
                                response = 1
                            if key in ['escape']:
                                self.win.close()
                                core.quit()
                            self.win.flip() # delete contents of window
                else:
                    break
                       
            # do nothing
            self.win.flip()
            self.port.setData(codes.dots_off)
            core.wait(self.preFeedbackTime)
            
            feedcode = 0
            dfeed = 0
            # show feedback 400 ms
            if (ttime < 0):
                self.feedback.setColor("red")
                if self.language == 'Spanish':
                    self.feedback.setText("Ninguna respuesta")#
                else:
                    self.feedback.setText("No response")#
                feedcode = codes.feedback_noResponse_on
                dfeed = 5
            else:
                if (self.tids[trial - 1][1] == 0):
                    # accuracy
                    if (response == self.tids[trial - 1][0]):
                        if self.language == 'Spanish':
                            self.feedback.setText("Correcto")#
                        else:
                            self.feedback.setText("Correct")
                        self.feedback.setColor("green")
                        feedcode = codes.feedback_correct_on
                        dfeed = 1
                    else:
                        if self.language == 'Spanish':
                            self.feedback.setText("Incorrecto")#
                        else:
                            self.feedback.setText("Incorrect")
                        self.feedback.setColor("red")
                        feedcode = codes.feedback_incorrect_on
                        dfeed = 2
                else:
                    if (ttime < self.speedTime):
                        if self.language == 'Spanish':
                            self.feedback.setText("A tiempo")#
                        else:
                            self.feedback.setText("In time")
                        self.feedback.setColor("green")
                        feedcode = codes.feedback_inTime_on
                        dfeed = 3
                    else:
                        if self.language == 'Spanish':
                            self.feedback.setText("Muy lento")#
                        else:
                            self.feedback.setText("Too slow")
                        self.feedback.setColor("red")
                        feedcode = codes.feedback_tooSlow_on
                        dfeed = 4
            self.feedback.draw()
            self.win.flip()
            self.port.setData(feedcode)
            
            #while (self.trialClock.getTime() < 400):
            core.wait(self.feedbackTime)
                # do nothing
                
            self.datafile.write(
                str(trial) + ',' + 
                str(self.tids[trial - 1][1] + 1) + ',' + 
                str(self.tids[trial - 1][2]) + ',' + 
                str(self.tids[trial - 1][0] + 1) + ',' + 
                str(response + 1) + ',' +
                str(1000*ttime) +  ',' +
                str(dfeed) + '\n')
            
            if(trial == len(self.tids)):
                running = False
            elif(trial == block*self.blockSize):
                # show end of block instructions and wait for response
                txt = "This is the end of block " 
                txt += str(block) + "\n\n" 
                txt += "You can now take a short rest. Please wait for the experimenter to continue the task."
                self.blockInstructions.setText(txt)
                self.blockInstructions.draw()
                self.port.setData(codes.feedback_off)
                self.win.flip()
                self.port.setData(codes.endBlockInstructions_on)
                cont = False
                while (cont == False):
                    for key in event.getKeys():
                        if key in ['enter','return','escape']:
                            if key in ['enter','return']:
                                cont = True
                                block += 1
                                self.port.setData(codes.continueBlockResponse)
                            if key in ['escape']:
                                self.win.close()
                                core.quit()
             
            trial = trial + 1
            
            # remove feedback
            self.win.flip()
            self.port.setData(codes.feedback_off)
            
            
            core.wait(self.postFeedbackTime)
            
        
        self.datafile.close()
