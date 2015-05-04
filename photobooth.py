#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pyscreen
import pyserver
from subprocess import call
import SocketServer
import threading
import subprocess

GPIO.setmode(GPIO.BCM)

# KONFIGURATION
play_sound = True
path_sound = 'html/sounds/beep.wav'
flip_vertically = False
flip_horizontally = False
color_background = (0, 255, 0)
color_foreground = (0, 0, 0)
seconds_countdown = 3
seconds_show_picture_no_interrupt = 3
seconds_show_picture_total = 10
text_anleitung = 'Der Fußtaster startet\nden Countdown\n\nBitte lächeln! :)'
photo_keep_aspect_ratio = True
photo_border = 20
photo_background = (255, 0, 0)
path_photos = 'html/fotos/'	# "/" am Ende nicht vergessen
gpio_shutter = 21
gpio_focus = 20

# program state (0 = anleitung, 1 = countdown, 2 = take picture, 3 = wait)
state = 0

# GPIO 21 = shutter
# GPIO 20 = focus
# Der Fußtaster löst beides gleichzeitig aus und
# zieht die Pins auf GND, die sonst - dank Pullup - auf 3V3 liegen
# Belegung Klinke: Spitze = shutter, Mitte = focus, Ende = GND
GPIO.setup(gpio_focus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_shutter, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callback_shutter(channel):
    global state
    if (state == 0 or state == 3):
	state = 1
    #print "Fußtaster (Shutter) ausgelöst\n"

#def callback_focus(channel):
#    print "Fußtaster (Focus) ausgelöst\n"


print "Bitte den Fußtaster an Klinkenbuchse anschließen!\n"
#GPIO.add_event_detect(gpio_focus, GPIO.RISING, callback=callback_focus, bouncetime=500)
GPIO.add_event_detect(gpio_shutter, GPIO.RISING, callback=callback_shutter, bouncetime=500)


Handler = pyserver.WebRequestHandler
Handler.path_photos = path_photos
server = SocketServer.TCPServer(('0.0.0.0', 80), Handler)

t = threading.Thread(target=server.serve_forever)
t.start()


booth = pyscreen.pyscreen()
seconds_rest = 0

try:
    while True:
	if (state == 0):	# zeige Anleitung
	    booth.display_text(text_anleitung, flip_horizontally, flip_vertically, 10, color_foreground, color_background)
	    time.sleep(1)

	elif (state == 1):	# zeige Countdown
	    if play_sound:
		booth.load_sound(path_sound)

	    for i in range(seconds_countdown, 0, -1):
		if play_sound:
		    booth.play_sound()
		booth.display_text('%d' % i, flip_horizontally, flip_vertically, 1, color_foreground, color_background)
		time.sleep(1)
	    
	    booth.display_text('0', flip_horizontally, flip_vertically, 1, color_foreground, color_background)
	    state = 2

	elif (state == 2):	# Bild aufnehmen und anzeigen
	    try:
		# clear screen
	    	booth.clear( (0, 0, 0) )
	    	filename = path_photos + "pb" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
	    	# USB Webcam (zum testen)
	    	#call(["./takepicture.sh", filename, "usb"])
	    	# Camera	
	    	#call(["./takepicture.sh", filename, "camera"])
			
			p = subprocess.Popen("./takepicture.sh", filename, "camera"])
			time.sleep(1)
			brightness = 0;
			frameTime = 0.1
			incValue = 255 / (2 / frameTime)
			# 2 Sekunden durch 0.1 wären 20 Frames, d.h. bei 255 Abstufungen 12.75 Stufen pro Frame höher gehen
	    	while p.poll() is None and brightness <= 255:
				booth.clear( (brightness, brightness, brightness) )
				brightness = brightness + incValue
				time.sleep(frameTime)
			
			while p.poll() is None:
				pass()
				
			booth.display_image(filename, flip_horizontally, flip_vertically, photo_border, photo_background, photo_keep_aspect_ratio)
	    except:
		print "Fehler beim Bildaufnehmen"


	    time.sleep(seconds_show_picture_no_interrupt)
	    seconds_rest = seconds_show_picture_total - seconds_show_picture_no_interrupt
	    state = 3

	elif (state == 3):	# stiller Countdown
	    if seconds_rest > 0:
		time.sleep(1)
		seconds_rest = seconds_rest - 1
	    else:
		state = 0
	
		
except KeyboardInterrupt:
    print "Photobooth wird beendet ..."
    #GPIO.cleanup()           # clean up GPIO on normal exit

GPIO.cleanup()          # clean up GPIO on normal exit
server.socket.close()	# close socket
