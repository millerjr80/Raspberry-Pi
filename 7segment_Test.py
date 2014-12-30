#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#Data Pins needed on the RPi
DATAIN=17 #DS
LATCH=27  #STCP
CLOCK=22  #SHCP
CLEAR=25  #MR Low
OE=11     #Output Enable Low

#inter character sleep
icsleep=0.06

#defining all the single LEDs
led1=0x80 #10000000
led2=0x40 #01000000
led3=0x20 #00100000
led4=0x10 #00010000
led5=0x08 #00001000
led6=0x04 #00000100
led7=0x02 #00000010
led8=0x01 #00000001

#definition of all writeable letters and numbers
letter={"0":0xFC,
        "1":0x30,
        "2":0xDA,
        "3":0x7A,
        "4":0x36,
        "5":0x6E,
        "6":0xEE,
        "7":0x38,
        "8":0xFE,
        "9":0x3E,
        "a":0xBE,
        "b":0xE6,
        "c":0xCC,
        "d":0xF2,
        "e":0xCE,
        "f":0x8E,
        "g":0x7E,
        "h":0xB6,
        "i":0x30,
        "j":0xF0,
        "l":0xC4,
        "n":0xBC,
        "o":0xFC,
        "p":0x9E,
        "s":0x6E,
        "t":0x38,
        "u":0xF4,
        "x":0xB4,
        "y":0x76,
        "z":0xDE
}

#loading function sequence
load1=0x06 #00000110
load2=0x22 #00100010
load3=0x60 #01100000
load4=0xC0 #11000000
load5=0x82 #10000010
load6=0x12 #00010010
load7=0x18 #00011000
load8=0x0C #00001100

#up-down loading function sequence
ud1=led8
ud2=led2
ud3=led1+led3
ud4=led7
ud5=led6+led4
ud6=led5

#left-right loading function sequence
lr1=led1+led6
lr2=led2+led5+led7
lr3=led3+led4
lr4=led8

#rotational loading function sequence
rot1=led2+led5
rot2=led1+led6+led3+led4+led7

#putting all segments of the sequences in a list
letterrange=[]
hexrange=[]
for value in letter.values():
    letterrange.append(value)
for value in letter.values():
    if value != "g":
        hexrange.append(value)
loadrange=[load1,load2,load3,load4,load5,load6,load7,load8]
udrange=[ud1,ud2,ud3,ud4,ud5,ud6]
ledrange=[led1,led2,led3,led4,led5,led6,led7,led8]
lrrange=[lr1,lr2,lr3,lr4]
rotrange=[rot1,rot2]
spinrange=[led1,led2,led3,led4,led5,led6]

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
    GPIO.output(CLEAR,True)  #Clear must always be true. False clears registers
    GPIO.output(OE,False)    #Output Enable speaks for itself. Must be False to display
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
   GPIO.output(CLOCK,GPIO.HIGH)
   GPIO.output(CLOCK,GPIO.LOW)
   GPIO.output(DATAIN,GPIO.LOW)

#writes the stored data from register out to pins
def writeout():
   #Display LEDs
   GPIO.output(LATCH,GPIO.HIGH)
   #needed to read characters. otherwise the characters would be display to fast after each other
   time.sleep(icsleep)
   GPIO.output(LATCH,GPIO.LOW)

#writes a character to the register
def writenumber(number):
    for x in range(0,8):
        shift((number>>x)%2)

#writes a range of character to the display        
def writerange(range):
    for x in range:
        writenumber(x)
        writeout()

#additive and following substractive writeout of a range of characters
def writeaddrange(range):
    character=0
    for x in range:
        character+=x
        writenumber(character)
        writeout()
    for x in range:
        character-=x
        writenumber(character)
        writeout()

#additive and following substractive writeout with reversed call of a range of characters
def writeaddremrange(range):
    character=0
    for x in range:
        character+=x
        writenumber(character)
        writeout()
    for x in range:
        character-=x
        writenumber(character)
        writeout()
    for x in reversed(range):
        character+=x
        writenumber(character)
        writeout()
    for x in reversed(range):
        character-=x
        writenumber(character)
        writeout()

#additive and following reversed substractive writeout of characters        
def writeaddbackrange(range):
    character=0
    for x in range:
        character+=x
        writenumber(character)
        writeout()
    for x in reversed(range):
        character-=x
        writenumber(character)
        writeout()

#chained XORed and reversed XORed writeout of characters
def writexorrange(range):
    #close the chain to have no interrupts while displaying
    character=range[0]&range[-1]
    for x in range:
        character^=x
        writenumber(character)
        writeout()
    for x in range:
        character^=x
        writenumber(character)
        writeout()
    for x in reversed(range):
        character^=x
        writenumber(character)
        writeout()
    for x in reversed(range):
        character^=x
        writenumber(character)
        writeout()

print("####Setup####")
setup()

#Tryout of most ranges and displayfunctions
try:
    print("####Write Stuff####")
    while True:
        writerange(letterrange)
        writerange(hexrange)
        writerange(loadrange)
        writeaddremrange(udrange)
        writexorrange(loadrange)
        writexorrange(udrange)
        writexorrange(ledrange)
        writexorrange(lrrange)
        writexorrange(rotrange)
        writexorrange(spinrange)
        writeaddrange(ledrange) 
        writeaddbackrange(ledrange)
#Wait for KeyboardInterrupt or SystemExit (called by kill or others)
except (KeyboardInterrupt, SystemExit):
    print("Exit...")

finally:
    cleanup()
