#Script to make pi2go lite autonomus using Sonar and left left/right IR sensors

#Define script as a python script
#!/usr/bin/env python

#Import the pi2go module as well as the sleep module from time

import pi2go
from time import sleep

#Initialise the pi2go, turns all motors etc off

pi2go.init()

try:
	while True:
		inputleft=pi2go.irLeft()
		inputright=pi2go.irRight()

		#Check if the distance is less than 30cm
		dist = pi2go.getDistance()
		if dist < 20:
        		print "Distance %.1f " % dist + "cm"
			pi2go.stop()
			sleep(0.2)

			#Check for obstacle on the right
			if inputright == 0:
				print "Turning Right"
				pi2go.spinRight(50)
				sleep(0.5)

			#Check for obstacles on the left
			elif inputleft == 0:
				print "Turning Left"
				pi2go.spinLeft(50)
				sleep(0.5)
		# Check if there are any obstacles on the Right
		elif inputright:
			print "Obstacle on Right"
			pi2go.reverse(60)
			sleep(0.5)
			pi2go.stop()
			pi2go.spinLeft(40)
			sleep(0.5)

		# Check if there are any obstacles on the Left
		elif inputleft:
			print "Obstacle on Left"
			pi2go.reverse(50)
			sleep(0.5)
			pi2go.stop()
			pi2go.spinRight(40)
			sleep(0.5)

		# If the distance is greater than 30cm go forward
		else:	
			print "Go forward, Distance %.1f " % dist + "cm"
			pi2go.forward(80)
		# Check every 0.1 seconds
		sleep(0.1)

except KeyboardInterrupt:  
	# exits when you press CTRL+C  
    	print " Thanks for Playing "  
  
finally:  

	#Cleanup the pi2go GPIO
	pi2go.cleanup()
