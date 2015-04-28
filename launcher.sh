#!/bin/sh

cd /home/pi/photobooth
/usr/local/bin/gphoto2 --set-config capturetarget=1
sudo python photobooth.py
