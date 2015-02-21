import cv2
import urllib 
import numpy as np
from common import clock, draw_str
import sys
import getopt
import serial

def move(servo, angle):
	'''Moves the specified servo to the supplied angle.

	Arguments: servo the servo number to command, an integer from 1-4 angle the desired servo angle, an integer from 0 to 180

	(e.g.) >>> servo.move(2, 90)
	... # "move servo #2 to 90 degrees"'''

	if (min_pwm <= angle <= max_pwm):
		ser.write(chr(255))
		ser.write(chr(servo))
		print 'Servo ID: ', servo
		ser.write(chr(angle))
		print 'Angle: ', angle
	else:
		print "Servo angle must be an integer between 0 and 180.\n"

max_pwm = 179
min_pwm = 1
# acceptable 'error' for the center of the screen.
mid_Screen_Window = 20 
# degree of change for each pan update 
pan_Step_Size = 1 
# degree of change for each tilt update
tilt_Step_Size = -1 
# initial pan position
servo_Pan_Pos = 90 
# initial tilt position
servo_Tilt_Pos = 45 
# arduino pan servo id 
pan_Servo_ID = 0  
# arduino tilt servo id 
tilt_Servo_ID = 1  
# Define the width of the captued image
width = 320
# Define the height of the captured image
height = 240
# Determine the mid point of the screen
mid_Screen_X = (width/2)
mid_Screen_Y = (height/2)

# Define where the stream will be captured from
stream = urllib.urlopen('http://192.168.1.150:8080/?action=stream')
bytes=''

# Define the location of the haarcascade algorithm used to detect the face
cascade_fn = "/home/h3d0n15t/opencv-3.0.0-beta/data/haarcascades/haarcascade_frontalface_alt2.xml"

# Tell openCV which cascade classifier to use for face detection
face_cascade = cv2.CascadeClassifier(cascade_fn)

# Define the serial connection to the Arduino Uno R3
ser=serial.Serial(port='/dev/ttyACM0',baudrate=9600,timeout=1)

#Set the pan servo to the middle
move(pan_Servo_ID, servo_Pan_Pos)

# Set the tilt servo to an inital value
move(tilt_Servo_ID, servo_Tilt_Pos)

while True:
	
	#Exxtract the jpg images from the mjpeg stream
	bytes+=stream.read(1024)
	a = bytes.find('\xff\xd8')
	b = bytes.find('\xff\xd9')
	if a!=-1 and b!=-1:
		jpg = bytes[a:b+2]
		bytes= bytes[b+2:]
		
		# Decode the captured images for use in OpenCV
		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.COLOR_BGR2GRAY)
		
		# Convert the captured image into gray scale.
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		# Equalise the gray scale image to remove noise
		gray = cv2.equalizeHist(gray)
		
		mid_Face_X = None
		
		# Use the gray scale image and specified Haar cascade to detect the face
		# Set scaling factor to 1.4 and min Neighbors to 5
		rects = face_cascade.detectMultiScale(gray, 1.3, 4)
		for (x,y,w,h) in rects:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
			
			# x and y co-ordinates of the corners of the rectangle
			x1 = x
			x2 = x+w
			y1 = y
			y2 = y+h
			
			# X co-ordinates of the middle of the face
			mid_Face_X = x1+((x2-x1)/2)
			
			# X co-ordinates of the middle of the face
			mid_Face_Y = y1+((y2-y1)/2)
			
			# X and Y co-ordinates for the middle of the detected face
			mid_Face = (mid_Face_X, mid_Face_Y)
			
			if mid_Face is not None:
				mid_Face_Y = mid_Face[0]
				mid_Face_Y = mid_Face[1]
				
				#Find out if the X component of the face is to the left of the middle of the screen.
				if(mid_Face_X < (mid_Screen_X - mid_Screen_Window)):
					#Update the pan position variable to move the servo to the right.
					servo_Pan_Pos += pan_Step_Size
					print str(mid_Face_X) + " > " + str(mid_Screen_X) + " : Pan Right : " + str(servo_Pan_Pos)
					
				#Find out if the X component of the face is to the right of the middle of the screen.
				elif(mid_Face_X > (mid_Screen_X + mid_Screen_Window)):
					#Update the pan position variable to move the servo to the left.
					servo_Pan_Pos -= pan_Step_Size
					print str(mid_Face_X) + " < " + str(mid_Screen_X) + " : Pan Left : " + str(servo_Pan_Pos)
				else:
					print str(mid_Face_X) + " ~ " + str(mid_Screen_X) + " : " + str(servo_Pan_Pos)
				
				servo_Pan_Pos = min(servo_Pan_Pos, max_pwm)
				servo_Pan_Pos = max(servo_Pan_Pos, min_pwm)
				move(pan_Servo_ID, servo_Pan_Pos)
				
				#Find out if the Y component of the face is below the middle of the screen.
				if(mid_Face_Y < (mid_Screen_Y - mid_Screen_Window)):
					if(servo_Tilt_Pos <= max_pwm):
						#Update the tilt position variable to lower the tilt servo.
						servo_Tilt_Pos += tilt_Step_Size
						print str(mid_Face_Y) + " > " + str(mid_Screen_Y) + " : Tilt Down : " + str(servo_Tilt_Pos)
				
				#Find out if the Y component of the face is above the middle of the screen.
				elif(mid_Face_Y > (mid_Screen_Y + mid_Screen_Window)):
					if(servo_Tilt_Pos >= 1):
						#Update the tilt position variable to raise the tilt servo.
						servo_Tilt_Pos -= tilt_Step_Size
						print str(mid_Face_Y) + " < " + str(mid_Screen_Y) + " : Tilt Up : " + str(servo_Tilt_Pos)
					
				
				servoTiltPosition = min(servo_Tilt_Pos, max_pwm)
				servoTiltPosition = max(servo_Tilt_Pos, min_pwm)
				move(tilt_Servo_ID, servo_Tilt_Pos)
				
		# Display image with overlay rectangle of detected face
		cv2.imshow('facedetect', img)
			
		if cv2.waitKey(1) ==27:
			exit(0)   
