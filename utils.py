def drawBlinkingText(SCREEN,myfont, text,x,y, colour=(0, 128, 0),blinkFraction=0.5,fast=False):
    """ Center means giving the far x point """
    textsurface = myfont.render(text, True, colour)
    tw = textsurface.get_rect().width
    th = textsurface.get_rect().height

    if(not fast):
        if time.time() % 1 > blinkFraction:
            SCREEN.blit(textsurface,(x,y))
    else:
        if time.time() % 0.5 > 0.25:
            SCREEN.blit(textsurface,(x,y))

    return(tw,th)



class countDownTimer():
    def __init__(self):
        self.counter = None

    def countDownReal(self,count,game):
        if(self.counter==None): self.counter = count

        self.counter-=game.dt/1000
        if(self.counter<1):
            self.counter= None
            return(True,self.counter)

        return(False,self.counter)


"""
IF SOURCE CHANGES
OR TRACKED OBJECT CHANGES 
OR SPECIFIED TIME CHANGES
STOPWATCH WILL RE-INITIALISE

"""
class stopTimer():
    def __init__(self):
        self.stopWatchInitialised  = False
        self.stopWatchState        = None

    def stopWatch(self,countValue,source,trackedObject,gs,silence=False):
        complete = False
        
        # Re-Initialise automatically
        if(self.stopWatchInitialised):
            if(self.stopWatchState['source']!= source or self.stopWatchState['endCount']!= countValue or self.stopWatchState['trackedObject']!= trackedObject):
                if(silence!=True):
                    print('***initialising counter**** for : ' + str(source))

                self.stopWatchInitialised=False

        # Initialise stop watch 
        if(self.stopWatchInitialised==False):
            self.stopWatchState = {'elapsed': 0,'endCount':countValue,'source':source,'trackedObject':trackedObject}
            self.stopWatchInitialised=True

        if(self.stopWatchInitialised):
            self.stopWatchState['elapsed'] += gs.dt/1000
            #print('Iter: ' + str(self.itercount) + '  elapsed: ' + str(self.stopWatchState['elapsed']))
            if(self.stopWatchState['elapsed']>self.stopWatchState['endCount']):
                complete=True

        return(complete)

    def reset(self):
        self.stopWatchInitialised  = False
        self.stopWatchState        = None




# LOOPS THRU IMAGE REEL

class imageAnimateAdvanced():
    def __init__(self,imageFrames,changeDuration):
        self.frameTimer      = stopTimer()
        self.changeDuration  = changeDuration
        self.changeCount     = 0

        self.currentFrame    = 0
        self.imageFrames     = imageFrames
        self.reelComplete    = False

    def reset(self):
        self.currentFrame    = 0
        self.reelComplete    = False
        self.changeCount     = 0

    def animate(self,gui,trackedName,blitPos,game,rotation=None,centerOfRotation=(0.5,0.5),repeat=True,skipBlit=False):
        # TIMER THAT ITERATES THROUGH A FRAME EACH GIVEN INTERVAL
        changeFrame = self.frameTimer.stopWatch(self.changeDuration,trackedName, str(self.changeCount) + trackedName, game,silence=True)
       
        if(changeFrame):
            self.changeCount +=1
            self.currentFrame +=1
            if(self.currentFrame>=len(self.imageFrames)):
                if(repeat==False):
                    self.currentFrame = len(self.imageFrames)-1
                else:
                    self.currentFrame = 0
                self.reelComplete = True
            else:
                # LATE ADDITION MIGHT NEED ROLLED BACK
                self.reelComplete = False
        if(skipBlit):
            return(self.reelComplete,{})

        if(rotation==None): rotation = 0
        rotation = wrapAngle(rotation)

        # GET ORIGINAL AND ROTATED LEN AND WIDTH
        rotated_image = pygame.transform.rotate(self.imageFrames[self.currentFrame], rotation)
        rotatedWidth,rotatedHeight     = rotated_image.get_width(),rotated_image.get_height()
        imgW,imgH = self.imageFrames[self.currentFrame].get_width(), self.imageFrames[self.currentFrame].get_height()

        # GET MUTATED COORDINATES
        blitx,blity         = blitPos[0]+centerOfRotation[0]*(imgW-rotatedWidth),blitPos[1]+centerOfRotation[1]*(imgH-rotatedHeight)
        gui.screen.blit(rotated_image, (blitx,blity))



        # GET MUTATED COORDINATES
        midTopX,midTopY     = (blitPos[0]+0.5*imgW + imgW * 0.5*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH  -imgH*0.5*math.sin(wrapAngle(rotation+90)*math.pi/180))
        # HORIZONTAL OFFSET OF MIDTOP
        offx = 30 * math.cos(math.radians(360-rotation))
        offy = 30 * math.sin(math.radians(360-rotation))
        rightTopX, rightTopY = midTopX + offx, midTopY + offy
        leftTopX, leftTopY   = midTopX - offx, midTopY - offy

        centerX,centerY   = (blitPos[0]+0.5*imgW + rotatedWidth*0.01*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH -rotatedHeight*0.01*math.sin(wrapAngle(rotation+90)*math.pi/180))

        smallOx,smallOy = 20 * math.cos(math.radians(360-rotation)), 20 * math.sin(math.radians(360-rotation))
        centerRx,CenterRy = centerX + smallOx, centerY + smallOy
        centerLx,CenterLy = centerX - smallOx, centerY - smallOy

        behindX,behindY   = (blitPos[0]+0.5*imgW - imgW*1.3*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH +imgH*1.3*math.sin(wrapAngle(rotation+90)*math.pi/180))
       

        #pygame.draw.circle(gui.screen, (220,100,100), (blitPos[0],blitPos[1]), 10, 0)


        return(self.reelComplete,{'center':(centerX,centerY ), 'centerL':(centerLx,CenterLy ),'centerR':(centerRx,CenterRy ), 'midTop':(midTopX,midTopY),'leftTop':(leftTopX, leftTopY),'rightTop':(rightTopX, rightTopY),'behind':(behindX,behindY) , 'rotatedDims': (rotatedWidth,rotatedHeight)})



    def animateNoRotation(self,gui,trackedName,blitPos,game,repeat=True):
        # TIMER THAT ITERATES THROUGH A FRAME EACH GIVEN INTERVAL
        changeFrame = self.frameTimer.stopWatch(self.changeDuration,trackedName, str(self.changeCount) + trackedName, game,silence=True)
       
        if(changeFrame):
            self.changeCount +=1
            self.currentFrame +=1
            if(self.currentFrame>=len(self.imageFrames)):
                if(repeat==False):
                    self.currentFrame = len(self.imageFrames)-1
                else:
                    self.currentFrame = 0
                self.reelComplete = True
            else:
                # LATE ADDITION MIGHT NEED ROLLED BACK
                self.reelComplete = False


        # GET ORIGINAL AND ROTATED LEN AND WIDTH
        imgW,imgH = self.imageFrames[self.currentFrame].get_width(), self.imageFrames[self.currentFrame].get_height()
        gui.screen.blit(self.imageFrames[self.currentFrame], (blitPos[0],blitPos[1]))

        return(self.reelComplete)


    def animateLowCompute(self,gui,trackedName,blitPos,game,repeat=True,rotation=None,skipBlit=False):
        # TIMER THAT ITERATES THROUGH A FRAME EACH GIVEN INTERVAL
        changeFrame = self.frameTimer.stopWatch(self.changeDuration,trackedName, str(self.changeCount) + trackedName, game,silence=True)
       
        if(changeFrame):
            self.changeCount +=1
            self.currentFrame +=1
            if(self.currentFrame>=len(self.imageFrames)):
                if(repeat==False):
                    self.currentFrame = len(self.imageFrames)-1
                else:
                    self.currentFrame = 0
                self.reelComplete = True
            else:
                # LATE ADDITION MIGHT NEED ROLLED BACK
                self.reelComplete = False

        # SKIP BLIT
        if(skipBlit):
            return(self.reelComplete)

        if(rotation==None): rotation = 0
        rotation = wrapAngle(rotation)

        # GET ORIGINAL AND ROTATED LEN AND WIDTH
        rotated_image = pygame.transform.rotate(self.imageFrames[self.currentFrame], rotation)
        rotatedWidth,rotatedHeight     = rotated_image.get_width(),rotated_image.get_height()
        imgW,imgH = self.imageFrames[self.currentFrame].get_width(), self.imageFrames[self.currentFrame].get_height()

        # GET MUTATED COORDINATES
        blitx,blity         = blitPos[0]+0.5*(imgW-rotatedWidth),blitPos[1]+0.5*(imgH-rotatedHeight)
        gui.screen.blit(rotated_image, (blitx,blity))


        # GET ORIGINAL AND ROTATED LEN AND WIDTH
        imgW,imgH = self.imageFrames[self.currentFrame].get_width(), self.imageFrames[self.currentFrame].get_height()

        return(self.reelComplete)

class scrollingDialogueSimple():
    def __init__(self):
        self.initialised        = False
        self.trackedText        = ''

        # TIMER BETWEEN LETTERS
        self.scrollTimer        = stopTimer()
        self.scrollCount        = 0
        self.scrollInterval     = 0.03

        # STARTUP TIMER
        self.startupTimer       = stopTimer()
        self.startupDelay       = 1

        # TIMER TO END OUT
        self.closeOutTimer      = stopTimer()
        self.closeOutCount      = 0
        self.closeOutDelay      = 3

        self.pageTimer          = stopTimer()

        self.textBuffer         = []
        self.baseArray          = []
        self.currentArrayIndex  = 0
        self.arrIndex           = 0
        self.senPos             = 0
        self.colour             = (255,2552,55)
        self.y                  = 0
        self.y2                 = 0


    def drawScrollingDialogue(self,gui,game,w,h,myfont, text, textStartingPos=(-1,-1),colour=None,interval=0,skipEnabled=False,closeOutDelay=True,startupDelay=True,vertInc= 1.2,maxLines=5,scrollInterval=0.03,pageWait=False):
        
        self.scrollInterval = scrollInterval

        #---------DELAY STARTUP UP 

        if(startupDelay):
            startup = self.startupTimer.stopWatch(self.startupDelay, 'start up timer', str(text),game,silence=True)
            if(not startup):
                return(False)


        # SET STARTING POSITION

        if(textStartingPos==(-1,-1)):
            xStart,yStart      = gui.x + 500,gui.y+70
        else:
            xStart,yStart = textStartingPos[0],textStartingPos[1]
        x,y        = xStart,yStart
        maxWidth   = w
        maxHeight  = h

        clicked    = gui.clicked
        hovered    = gui.mouseCollides(x,y,maxWidth,maxHeight)
        
        
        if(colour==None): colour = self.colour
        
        # ONLY ENABLE SKIP IF SPECIFIED
        skip = False 
        if(skipEnabled):
            pass # ENABLE SKIP LATER

        #----------------------------------------------------------
        #
        #    INITIALISE DIALOGUE   REINITIALISE IF TEXT CHANGES OR SET EXTERNALLY 
        #
        #----------------------------------------------------------


        if(self.initialised== False or text!=self.trackedText):
            
            self.trackedText       = text
            # format paragraph into array of fitted sentences
            self.textBuffer        = []
            self.baseArray         = []
            self.y                 = yStart
            self.senPos            = 0
            self.currentArrayIndex = 0
            self.arrIndex          = 0
            self.finished          = False

            dialogueArray,para = [], ""
            for word in text.split(' '):
                pre   = para
                para += word + " "
                textsurface = myfont.render(para, True, colour)
                w = textsurface.get_rect().width
                if(w>= maxWidth):
                    dialogueArray.append(pre)
                    para = word + " "
            dialogueArray.append(para)

            self.baseArray       = dialogueArray   # Full Dialogue
            self.textBuffer      = dialogueArray   # Actual Dialogue being printed
            self.arrIndex        = maxLines        # array index is the last line of page(array slice)
            

            # SET TEMPORARY TEXT ARRAY BASED UPON LINE LIMIT 
            if(len(self.textBuffer)>maxLines): 
                self.textBuffer = self.baseArray[0:self.arrIndex]
            self.initialised  = True


        #----------------------------------------------------------
        #
        #    NEXT PAGE & SKIP
        #
        #----------------------------------------------------------
        if((hovered and clicked) or gui.input.returnedKey.upper()=='RETURN'): 
            
            # IF BEFORE THE LAST PAGE 
            # array index is the last line of given array slice
            if(self.arrIndex<len(self.baseArray)):
                self.textBuffer = self.baseArray[self.arrIndex:(self.arrIndex+maxLines)] # GO TO NEXT PAGE
                self.arrIndex  = self.arrIndex + maxLines
                self.currentArrayIndex     = 0
                self.senPos     = 0
                self.y          = yStart
            else:
                if(skip):
                    self.finished            = True
                    self.scrollSpeedOverride = None

        # GOING TO NEXT PAGE
        if(type(pageWait)==int):
            # Adding in these values means if anythign changes the timer resets state
            nextPage = self.pageTimer.stopWatch(pageWait, 'waiting to go to next page','next page' + str([self.arrIndex,self.baseArray,self.currentArrayIndex,self.senPos]),game,silence=True)
            if(nextPage and self.arrIndex<len(self.baseArray)):
                self.textBuffer = self.baseArray[self.arrIndex:(self.arrIndex+maxLines)] # GO TO NEXT PAGE
                self.arrIndex  = self.arrIndex + maxLines
                self.currentArrayIndex     = 0
                self.senPos     = 0
                self.y          = yStart
                self.pageTimer.reset()





        # -----------PRINT PRECEEDING ROWS

        self.y2 = yStart
        for row in range(0,self.currentArrayIndex):
            currentSentence = self.textBuffer[row]
            ts = myfont.render(currentSentence, True, colour)
            h = ts.get_rect().height
            gui.screen.blit(ts,(x,self.y2))
            self.y2=self.y2+ vertInc*h


        #----------------------------------------------------------
        #
        #    SCROLL CURRENT LINE
        #
        #----------------------------------------------------------

        currentSentence = self.textBuffer[self.currentArrayIndex]
        for word in (range(0,len(currentSentence[self.senPos]) )):
            printSentence = currentSentence[:self.senPos]
            ts = myfont.render(printSentence, True, colour)
            h = ts.get_rect().height
        gui.screen.blit(ts,(x,self.y))
        x=xStart


        # -----------PRINT SKIP IF NEED BE 

        if(skip and self.currentArrayIndex<(len(self.textBuffer)-1)): 
            self.currentArrayIndex = len(self.textBuffer)-1
            self.senPos=0
            self.y=self.y+vertInc *(len(self.textBuffer)-1)*h


        #----------------------------------------------------------
        #
        #    PROCESS NEXT WORD 
        #
        #----------------------------------------------------------


        nextWordReady = self.scrollTimer.stopWatch(self.scrollInterval, 'textScroll', str(self.scrollCount) + str(text),game,silence=True)
        if(nextWordReady):
            self.scrollCount +=1
            
            # keep increementing sentence position until it is the len of the full sen for this line
            if(len(currentSentence)-2 >=self.senPos):
                self.senPos+=1
            elif(len(self.textBuffer)-2>=self.currentArrayIndex):
                self.currentArrayIndex +=1
                self.y= self.y+vertInc *h
                self.senPos=0
            else:
                # If at end of array, end of elem and true end
                if(self.arrIndex>=len(self.baseArray)):
                    self.finished    = True

        #---------DELAY CLOSING OUT 

        if(closeOutDelay and self.finished):
            closeOut = self.closeOutTimer.stopWatch(self.closeOutDelay, 'close out timer', str(self.closeOutCount) + str(text),game,silence=True)
            if(closeOut):
                self.closeOutCount +=1
                self.finished = True
            else:
                return(False)

        return(self.finished)



#----------------------------------------
#    FOR TEXT THAT FLICKS LEFT TO RIGHT
#----------------------------------------

class scrollingDialogue():

    def __init__(self,gui,x,y,w,h,borderColour):
        self.x                      = x
        self.y                      = y
        self.w                      = w
        self.h                      = h
        self.scrollInitialised      = False
        self.origText               = ''
        self.tempWriterArray        = []
        self.colour                 = (0,0,0)
        self.y                      = 0
        self.y2                     = 0
        
        self.timer                  = 15
        self.senPos                 = 0
        self.arrPos                 = 0
        self.arrIndex               = 0
        self.scrollSpeedOverride    = None
        self.finished               = False
        self.stopTimer              = stopTimer()
        self.borderColour           = borderColour

        #-----INITIALISE RESPONSE
        self.requiresResponse = False 
        self.responseOptions  = ["Yes.", "No."]
        self.buttonFillColour = (0,0,0)
        self.buttonTxtColour  = (255,255,255)
        self.response1        = button(200,30,0,0,self.responseOptions[0],self.buttonFillColour,gui.font,textColour=self.buttonTxtColour)
        self.response2        = button(200,30,0,0,self.responseOptions[1],self.buttonFillColour,gui.font,textColour=self.buttonTxtColour )
        self.response3        = button(200,30,0,0,self.responseOptions[1],self.buttonFillColour,gui.font,textColour=self.buttonTxtColour)

        self.cutOutDuration   = 'normal' # Time to pause when cutting out
    
    # POS[X,Y] ARE LEFT SIDE AND BOTTOM OF AVATAR
    def drawScrollingDialogue(self,gui, game,myfont, text,maxWidth,maxHeight,textStartingPos=(-1,-1),colour=None,scrollSpeed=10,vertInc=1.2,maxLines=5,cutOutWaitTime=5,skip=False):
        """
        function to scroll text, top/bottom with paging.
        """
        

        #   - starting text positions
        sx,sy      = textStartingPos[0],textStartingPos[1]
        x,y        = sx,sy
        
        clicked    = gui.clicked
        hovered    = gui.mouseCollides(x,y,maxWidth,maxHeight)
        
        # OVERRIDE COLOUR FROM CALLING FUNCTION
        if(colour!=None):
            self.colour = colour

        # RESET IF THE TEXT CHANGES FROM THE TEXT STORED IN STATE 
        if(self.origText!= text):

            self.scrollInitialised =False
            self.origText = text






        #----------------------------------------------------------
        #
        #    INITIALISE DIALOGUE
        #
        #----------------------------------------------------------

        if(self.scrollInitialised == False):
            self.colour      = (0,0,0)       # reset colour
            self.timer       = 15

            self.origText   = text
            # format paragraph into array of fitted sentences
            self.tempWriterArray   = []
            self.baseArray   = []
            self.y           = sy
            self.senPos      = 0
            self.arrPos      = 0
            self.arrIndex    = 0
            self.finished    = False
            

            #  BUILDING FULL DIALOGUE ARRAY FOR TEXT
            print('******************************************')
            print('BUILDING FULL DIALOGUE ARRAY FOR ' + str(text))
            print('******************************************')
            dialogueArray,para = [], ""
            for word in text.split(' '):
                pre   = para
                para += word + " "
                textsurface = myfont.render(para, True, self.colour)
                w = textsurface.get_rect().width
                if(w>= maxWidth):
                    dialogueArray.append(pre)
                    para = word + " "
            dialogueArray.append(para)

            
            self.baseArray       = dialogueArray   # Full Dialogue
            self.tempWriterArray = dialogueArray   # Actual Dialogue being printed
            self.arrIndex  = 5               # array index is the last line of given array slice
            

            # SET TEMPORARY TEXT ARRAY BASED UPON LINE LIMIT 
            if(len(self.tempWriterArray)>maxLines): 
                self.tempWriterArray = self.baseArray[0:self.arrIndex]
            self.scrollInitialised  = True




        #----------------------------------------------------------
        #
        #    OVERRIDE SPEED (SET EXTERNALLY VIA PLOT->MESSAGEUPDATE->HERE)
        #
        #----------------------------------------------------------
        if(self.scrollSpeedOverride=='fast'):
            scrollSpeed    = 0
        if(self.scrollSpeedOverride=='normal'):
            scrollSpeed    = 1
        if(self.scrollSpeedOverride=='slow'):
            scrollSpeed    = 3

        if(self.cutOutDuration=='instant'):
            cutOutWaitTime = 0
        if(self.cutOutDuration=='fast'):
            cutOutWaitTime = 1
        if(self.cutOutDuration=='normal'):
            cutOutWaitTime = 3
        if(self.cutOutDuration=='slow'):
            cutOutWaitTime = 4
        if(self.cutOutDuration=='verySlow'):
            cutOutWaitTime = 7
        if(self.cutOutDuration=='untilClicked'):
            cutOutWaitTime = 3




        #----------------------------------------------------------
        #
        #    NEXT PAGE & SKIP
        #
        #----------------------------------------------------------
        if((hovered and clicked) or gui.input.returnedKey.upper()=='RETURN'): 
            
            # IF BEFORE THE LAST PAGE 
            # array index is the last line of given array slice
            if(self.arrIndex<len(self.baseArray)):
                self.tempWriterArray = self.baseArray[self.arrIndex:(self.arrIndex+maxLines)] # GO TO NEXT PAGE
                self.arrIndex  = self.arrIndex + maxLines
                self.arrPos     = 0
                self.senPos     = 0
                self.y          = sy
            else:
                if(skip):
                    self.finished            = True
                    self.scrollSpeedOverride = None


        

        #----------------------------------------------------------
        #
        #    PRINT ALL PREVIOUS LINES
        #
        #----------------------------------------------------------
        
        self.y2 = sy
        for row in range(0,self.arrPos):
            currentSentence = self.tempWriterArray[row]
            ts = myfont.render(currentSentence, True, self.colour)
            h = ts.get_rect().height
            gui.screen.blit(ts,(x,self.y2))
            self.y2=self.y2+ vertInc*h


        #----------------------------------------------------------
        #
        #    SCROLL CURRENT LINE
        #
        #----------------------------------------------------------

        currentSentence = self.tempWriterArray[self.arrPos]
        for word in (range(0,len(currentSentence[self.senPos]) )):
            printSentence = currentSentence[:self.senPos]
            ts = myfont.render(printSentence, True, self.colour)
            h = ts.get_rect().height
        gui.screen.blit(ts,(x,self.y))
        x=sx


        #--------------increment sen/array
        self.timer-=1
        if(self.timer<1):
            self.timer=scrollSpeed

            # Increment sentence print position
            if(len(currentSentence)-2 >=self.senPos):
                self.senPos+=1
            else:
                # Increment array Position
                if(len(self.tempWriterArray)-2>=self.arrPos):
                    self.arrPos +=1
                    self.y=self.y+vertInc*h
                    self.senPos=0
                else:
                    # If at end of array, end of elem and true end
                    if(self.arrIndex>=len(self.baseArray)):
                        self.finished    = 'End of Text'
        

        #================================================
        #
        #               FINISH UP
        #       
        #   ADD DELAY BEFORE FINISHING (DEFINED BY cutOutWaitTime 
        #   WHICH IS SCROLLOVERRIDE VALUE)
        #
        #   IF REQUIRES RESPONSE SET THEN THAT HAPPENS FIRST
        #
        #================================================

        # WRAP UP AND WAIT FOR CUTOUT TIME
        if(self.finished=='End of Text' and self.requiresResponse==False and self.cutOutDuration!='untilClicked'):
            swComplete = self.stopTimer.stopWatch(cutOutWaitTime,'displayAlert',text,game)
            if(swComplete):
                self.scrollSpeedOverride = None
                self.finished            = True
        # OR WAIT UNTIL RESPONSE GIVEN
        elif(self.finished=='End of Text' and self.requiresResponse==True):
            
            # GET DIMENSIONS TO POSITION BUTTON BETTER
            rw1,rh1      = self.response1.displayReturnButtonDimensions(gui,textOverride=self.responseOptions[0], widthOverride='tight',fontOverride=self.response1.font)
            rw2,rh2      = self.response2.displayReturnButtonDimensions(gui,textOverride=self.responseOptions[1], widthOverride='tight',fontOverride=self.response2.font)

            horizontalGap = 0.05*self.w
            x_response   = self.x + 0.5*(self.w-(rw1+rw2+horizontalGap))
            y_response   = self.y+self.h - 1.5*rh1 - 7 # 7 is border 
            optionOne,bw,bh = self.response1.display(gui,textOverride=self.responseOptions[0], widthOverride='tight',noBorder=False,fillColour=darken(self.buttonFillColour),updatePos=[x_response,y_response],                             hoverBoxCol=lighten(self.buttonFillColour),hoverTextCol=self.buttonTxtColour,borderColour=self.borderColour)
            optionTwo,bw,bh = self.response2.display(gui,textOverride=self.responseOptions[1], widthOverride='tight',noBorder=False,fillColour=darken(self.buttonFillColour),updatePos=[x_response + bw + horizontalGap,y_response],        hoverBoxCol=lighten(self.buttonFillColour),hoverTextCol=self.buttonTxtColour,borderColour=self.borderColour)

            
            # --- wrap up once response captured
            if(optionOne):
                game.plotTracker[game.state]['response'] = self.responseOptions[0]
                self.requiresResponse = False
                self.responseOptions = ['Yes','No']
            if(optionTwo):
                game.plotTracker[game.state]['response'] = self.responseOptions[1]
                self.requiresResponse = False
                self.responseOptions = ['Yes','No']
        # OR WAIT UNTIL CLICKED
        elif(self.finished=='End of Text' and self.requiresResponse==False and self.cutOutDuration=='untilClicked'):
            swComplete = self.stopTimer.stopWatch(cutOutWaitTime,'displayAlert',text,game)
            if(swComplete):
                if( (hovered and clicked) or gui.user_input.returnedKey=='return'):
                    self.scrollSpeedOverride = None
                    self.finished            = True


        return(self.finished)


