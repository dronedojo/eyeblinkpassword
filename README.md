# eyeblinkpassword
An opencv project for using the blinking of eyes as a password

#####USAGE ON VARIOUS OPERATING SYSTEMS######
This eye blink password script will work on all OS: Windows, Mac and Linux. 

WINDOWS: an anaconda environment .yml config file has been provided for easy dependency installation. 
MAC: Dependency resolving currently must be performed by the user. 
LINUX: Dependency resolving currently must be performed by the user. 
	IF usage is for a raspberry pi, find the Drone Dojo youtube channel and search for the installation walkthrough video.

#####WHAT THIS SCRIPT DOES###################

See youtube video for visual representation: 

Some people type words for their password. This script is a proof of concept allowing you to blink your eyes as a password
by using opencv and a camera.

An example password: 'LRB'

Each digit can be either:
	'L': Left eye closed
	'R': Right eye closed
	'B': Both eyes closed

The password length can be as long as desired. 
To unlock the password:

1. Hold left eye closed, right eye opened
2. Open both eyes (locks in the left eye closed digit)
3. Hold right eye closed, left eye opened 
4. Open both eyes (locks in the left eye closed digit)
5. Hold both eyes closed 
6. Open both eyes (locks in the left eye closed digit)

And the password has matched and the script will exit. It is up to you to decide what actually gets unlocked. 

##########EYE BLINK SAFE#####################

An example application of this eye blink password is drone dojo 'Eye Blink Safe': See youtube video. 

The eye blink safe is powered by a raspberry pi. When the password is matched, the code unlocks
a solenoid lock that opens a 3D printed safe. 

If using this script for the 'Eye Blink Safe', make sure to change the isEyeBlinkSafe variable in the script to True. 

The Eye blink safe uses an LCD screen to output relavant info from the running script to the user. 





