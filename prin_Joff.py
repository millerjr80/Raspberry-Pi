import RPi.GPIO as GPIO
import time
 
#Data Pins needed on the RPi
DATAIN=17 #DS
LATCH=27  #STCP
CLOCK=22  #SHCP
CLEAR=25  #MR Low
OE=11     #Output Enable Low
 
#inter character sleep
icsleep=0.5

#loading JOFF
loadj=0xF0
loado=0xFC
loadn=0xBC
loada=0xBE
loadt=0x38
loadh=0xB6

joff = [loadj,loado,loadn,loada,loadt,loadh,loada,loadn]

#GPIO definition
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(DATAIN,GPIO.OUT)
    GPIO.setup(CLOCK,GPIO.OUT)
    GPIO.setup(LATCH,GPIO.OUT)
    GPIO.setup(CLEAR,GPIO.OUT)
    GPIO.setup(OE,GPIO.OUT)
 
    GPIO.output(LATCH,False) #Latch is used to output the saved data
    GPIO.output(CLEAR,True)  #Clear must always be true. False clears registers
    GPIO.output(OE,False)    #Output Enable speaks for itself. Must be False to display
    GPIO.output(CLOCK,False) #Used to shift the value of DATAIN to the register
    GPIO.output(DATAIN,False)#Databit to be shifted into the register 
 
    #Clean up GPIO, set display to no character
def cleanup():
    #Set all leds to off
    writenumber(0)
    #writeout stored in character
    writeout()
    #writeout "nothing"
    writeout()
    time.sleep(0.7)
    GPIO.cleanup()
 
#shifts in a bit (but does not write it yet)
def shift(input):
   if input == 1:
       input=True
   else:
       input=False
 
   GPIO.output(DATAIN,input)
   print(input)
   GPIO.output(CLOCK,GPIO.HIGH)
   print("Clock High")
   GPIO.output(CLOCK,GPIO.LOW)
   print("Clock Low")
   GPIO.output(DATAIN,GPIO.LOW)

#writes the stored data from register out to pins
def writeout():
   #Display LEDs
   GPIO.output(LATCH,GPIO.HIGH)
   print("Latch High")
   #needed to read characters. otherwise the characters would be display to fast after each other
   time.sleep(icsleep)
   GPIO.output(LATCH,GPIO.LOW)
   print("Latch Low")

#writes a character to the register
def writenumber(number):
    for x in range(0,8):
        print "Input bit ",x," into the shift register"
        shift((number>>x)%2)

#writes a range of character to the display        
def writerange(range):
    for x in range:
	print "Write "+hex(x)+" to the shift register"
        writenumber(x)
        print("Write to the 7 segment display")
        writeout()

print("####Setup####")
setup()
 
#Tryout of most ranges and displayfunctions
try:
    print("####Write Stuff####")
    while True:
        writerange(joff)
#Wait for KeyboardInterrupt or SystemExit (called by kill or others)
except (KeyboardInterrupt, SystemExit):
    print("Exit...")
 
finally:
    cleanup()
