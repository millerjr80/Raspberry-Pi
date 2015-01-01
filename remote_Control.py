# Pi2Go remote control with pan and tilt camera
# Moves: Forward, Reverse, turn Right, turn Left, Stop
# Press Ctrl-C to stop
#
# Also demonstrates writing to the LEDs
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python remote_Control.py


import pi2go
import time

# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 0 # 0 degrees is centre
pVal = 0 # 0 degrees is centre

#======================================================================

# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows
    
def doServos():
    pi2go.setServo(pan, pVal)
    pi2go.setServo(tilt, tVal)

# End of single character reading

speed = 30

pi2go.init()
print "pi2go version: ", pi2go.version()
print "Motors: Use Arrows for direction, Space = Stop, < = slow, > = fast, ^C=Exit:\nServo's: w = up, z = down, a = left, s = right "

# main loop
try: 
	
	while True:
		keyp = readkey()
		if ord(keyp) == 16:
			pi2go.forward(speed)
			print 'Forward', speed
			
		elif ord(keyp) == 17:
			pi2go.reverse(speed)
			print 'Reverse', speed
		
		elif ord(keyp) ==  18:
			pi2go.spinRight(speed)
			print 'Spin Right', speed
		
		elif ord(keyp) == 19:
			pi2go.spinLeft(speed)
			print 'Spin Left', speed
		
		elif keyp == '.' or keyp == '>':
			speed = min(100, speed+10)
			print 'Speed+', speed

		elif keyp == ',' or keyp == '<':
			speed = max (0, speed-10)
			print 'Speed-', speed

		elif keyp == ' ':
			pi2go.stop()
			print 'Stop'

		elif keyp == 'c':
			tVal = 0
			pVal = 0
			doServos()
			print "Servo Centre"
            
		elif keyp == 'q':
			pi2go.stopServos()
			print "Servo Stop"

		elif keyp == 'w':
			pVal += 10
			doServos()
			print "Servo Up" + str(pVal)

		elif keyp == 'a':
			tVal -= 10
			doServos()
			print "Servo Left" + str(tVal)

		elif keyp == 's':
			tVal += 10
			doServos()
			print "Servo Right" + str(tVal)

		elif keyp == 'z':
			pVal -= 10
			doServos()
			print "Servo Down" + str(pVal)

		elif keyp == 'g':
			pi2go.startServos()
			print "Servo Down"

		elif ord(keyp) == 3:
			print "Thanks for playing!!!"
			break

except KeyboardInterrupt:
	print "The End"

finally:
	pi2go.cleanup()
