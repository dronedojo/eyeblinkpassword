import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils.video import WebcamVideoStream
import imutils


import time
import os
import platform
######################SCRIPT CHANGING VARIABLES##################################
password='LLRRB' ##L for left eye closed, R for right eye closed, B for both eyes closed. 
##Each digit of the password can be either L, R or B.


isRaspberryPi='' ##If running from Raspberry Pi don't display video output
isEyeBlinkSafe=False
osType=platform.system() ##Output is either: 'Linux' or 'Darwin' or 'Windows'

if osType=='Windows' or osType=='Darwin':
    isRaspberryPi=False
else: ##This is Linux, now see if ran from a raspberry pi
    print(os.uname())
    systemInfo=os.uname()[1] ##This is the hostname of your RPi. This will not work if you changed the hostname from default 'raspberrypi'
    if systemInfo =='raspberrypi': 
        isRaspberryPi=True
        print("Assuming raspberry pi is wired for the eye blink safe.")
print("Is running machine a Raspberry Pi: "+str(isRaspberryPi))

######################GLOBAL VARIABLES###########################################

##Initialize variables for RPi usage with LCD and GPIO

solenoidPin=''
if isEyeBlinkSafe==True:
    import RPi.GPIO as GPIO
    import lcddriver
    
    solenoidPin=21
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(solenoidPin,GPIO.OUT)
    
    lcd = lcddriver.lcd()

##Pass in the file path to the haar cascades.


l_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_lefteye_2splits.xml')
r_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_righteye_2splits.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

scale = 1.2
left_eye_found=False
right_eye_found=False

l_eye_x=0
l_eye_y=0

r_eye_x=0
r_eye_y=0

frame_x=0
frame_y=0

l_eye_blink_state='closed' ## 'notfound','open' or 'closed'
r_eye_blink_state='closed' ## 'notfound','open' or 'closed'

frameForDrawing=''
##Initialize the webcam thread that updates frames in the background
cap = WebcamVideoStream(src=0).start()


counter=0
eyeStateSequence='' ##L for left closed, R for right closed, B for both closed, O for both open
eyeStateCounter=0
eyeStateCountConfirmed=2
lastState=''
eyesNotFoundCounter=0
eyeStateQueue=''


##########################FUNCTIONS###############################################

def detect_left_and_right_eyes(frame_for_detection):
    
    global left_eye_found,right_eye_found,l_eye_x,l_eye_y,r_eye_x,r_eye_y,r_eye_y,l_eye_blink_state,r_eye_blink_state,scale,frameForDrawing
    
    l_eyes_rects = l_eye_cascade.detectMultiScale(frame_for_detection,scaleFactor=scale,minNeighbors=5)
    
    left_most_eye=()
    left_eye_found=False
    counter=0
    biggestArea=0
    
    for (x,y,w,h) in l_eyes_rects:
        left_eye_found=True
        tempArea=w*h
        
        if counter==0:
            left_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        elif x>left_most_eye[0]:
            left_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        counter=counter+1
    
    if left_eye_found == True:
        x,y,w,h=left_most_eye
        if isRaspberryPi==False:
            cv2.rectangle(frameForDrawing,(x,y),(x+w,y+h),(255,0,0),10)
        l_eye_x=x
        l_eye_y=y
        
    r_eyes_rects = r_eye_cascade.detectMultiScale(frame_for_detection,scaleFactor=scale,minNeighbors=5)
    
    right_most_eye=()
    right_eye_found=False
    counter=0
    biggestArea=0
    
    for (x,y,w,h) in r_eyes_rects:
        right_eye_found=True
        tempArea=w*h
        
        if counter==0:
            right_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        elif x<right_most_eye[0]:
            right_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        counter=counter+1
        
        
    if right_eye_found == True:
        x,y,w,h=right_most_eye
        if isRaspberryPi==False:
            cv2.rectangle(frameForDrawing,(x,y),(x+w,y+h),(0,255,0),10)
        r_eye_x=x
        r_eye_y=y

        
    return None


def detect_eyes(frame_for_detection):
    
    global l_eye_found,r_eye_found,l_eye_x,l_eye_y,r_eye_x,r_eye_y,l_eye_blink_state,r_eye_blink_state,scale,frameForDrawing
    
    l_eye_blink_state='closed'
    r_eye_blink_state='closed'
    
    eyes_rects = eye_cascade.detectMultiScale(frame_for_detection,scaleFactor=scale,minNeighbors=40)
    
    counter=0
    for (x,y,w,h) in eyes_rects:
        if counter>=2:
            break
        if isRaspberryPi==False:
            cv2.rectangle(frameForDrawing,(x,y),(x+w,y+h),(255,255,255),3)
        
        if abs(l_eye_x-x)<frame_x*.05 and abs(l_eye_y-y)<frame_y*.05 and left_eye_found == True:
            l_eye_blink_state='open'
        elif abs(r_eye_x-x)<frame_x*.05 and abs(r_eye_y-y)<frame_y*.05 and right_eye_found == True:
            r_eye_blink_state='open'
        counter=counter+1
        
    return None

##############################MAIN SCRIPT#############################################

lcdstate='' ##found, not
while True:
    
    tempState=''
    
    frameForDetection = cap.read()
    frameForDetection = cv2.resize(frameForDetection,(320,240))
    
    
    if isRaspberryPi==True: ##Convert to grayscale if RPI
        frameForDetection=cv2.cvtColor(frameForDetection,cv2.COLOR_BGR2GRAY)
    else: ##Create image to draw on if not RPI
        frameForDrawing=frameForDetection.copy()
        

    if counter==0:
        frame_y=frameForDetection.shape[1]
        frame_x=frameForDetection.shape[0]
    
    #####FRAME DRAWING AND VARIABLE FETCHING#######
    
    detect_left_and_right_eyes(frameForDetection)
    
    detect_eyes(frameForDetection)
    
    if isRaspberryPi==False:
        cv2.imshow('EYE WINDOW',frameForDrawing)
    
    #####EYE BLINK LOGIC###########################
    
    if left_eye_found == True and right_eye_found == True:
        eyesNotFoundCounter=0
        
        if isEyeBlinkSafe==True:
            if lcdstate!='found' and eyeStateSequence=='':

                lcd.lcd_clear()
                lcd.lcd_display_string("Both eyes found",1)###Find tempState of eyes###
                lcd.lcd_display_string("Please attempt pw",2)
                lcdstate='found'
        
        if l_eye_blink_state=='open' and r_eye_blink_state=='open':
            tempState='O'
        elif l_eye_blink_state=='closed' and r_eye_blink_state=='open':
            tempState='L'
        elif l_eye_blink_state=='open' and r_eye_blink_state=='closed':
            tempState='R'
        elif l_eye_blink_state=='closed' and r_eye_blink_state=='closed':
            tempState='B'
        ############################
        
        
        if lastState == tempState and eyeStateCounter < eyeStateCountConfirmed:
            eyeStateCounter = eyeStateCounter+1
        elif lastState == tempState and eyeStateCounter >= eyeStateCountConfirmed:
            
            if eyeStateQueue=='' and tempState!='O':
                eyeStateQueue=tempState
                eyeStateCounter=0
            elif eyeStateQueue!='' and tempState=='O':
                
                eyeStateSequence=eyeStateSequence+eyeStateQueue
                eyeStateCounter=0
                eyeStateQueue=''
                print("Current eye state sequence: "+str(eyeStateSequence))
                if isEyeBlinkSafe==True:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Current progress:",1)
                    lcd.lcd_display_string(str(eyeStateSequence),2)
        elif lastState != tempState:

            eyeStateCounter = 0
        
        lastState=tempState
        
        if eyeStateSequence == password:
            print("PASSWORD MATCHED!!!! OPEN SESAME!!!!")
            if isEyeBlinkSafe==True:
                lcd.lcd_clear()
                lcd.lcd_display_string("PASSWORD MATCH!!",1)
                lcd.lcd_display_string("Door will unlock for 4 seconds",2)
                GPIO.output(solenoidPin,GPIO.HIGH)
                time.sleep(4)
                GPIO.output(solenoidPin,GPIO.LOW)
                time.sleep(1)
                GPIO.cleanup()
            break
    else:
        if isEyeBlinkSafe==True:
            if lcdstate!='notfound':
                lcd.lcd_clear()
                lcd.lcd_display_string("EYES NOT FOUND!",1)
                lcdstate='notfound'
        if counter%100==0:
            print("Left and/or Right eye not detected. Please face the camera directly around 1 ft away from the camera.")
            
        if eyesNotFoundCounter > eyeStateCountConfirmed+5:
            if eyeStateSequence!='':
                print("Resetting eye blink sequence. Try password again.")
                eyesNotFoundCounter=0
                eyeStateSequence=''
                lastState=''
                if isEyeBlinkSafe==True:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("EYES NOT FOUND!",1)
                    lcd.lcd_display_string("RESETTING PASSWORD",2)
        eyesNotFoundCounter=eyesNotFoundCounter+1
        
    
    print("Left/Right Eye State: "+str(l_eye_blink_state)+"/"+str(r_eye_blink_state)+"   Current eye state sequence: "+str(eyeStateSequence))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    counter=counter+1

time.sleep(2)
cap.stop()
cv2.destroyAllWindows()

if isEyeBlinkSafe==True:
    lcd.lcd_clear()
