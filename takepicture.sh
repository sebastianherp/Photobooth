#!/bin/sh

# Nimmt ein Bild auf

filename=$1
mode=$2

if [ "$1" = "" ]; then
    filename=pb_$(date -u +"%Y%m%d_%H%M%S").jpg
fi

if [ "$2" = "" ]; then
    mode="usb"
fi


if [ "$mode" = "camera" ]; then
    # Aufnahme über angeschlossene Kamera
    #/usr/local/bin/gphoto2 --set-config capturetarget=1
    /usr/local/bin/gphoto2 --keep --capture-image-and-download --filename $filename
else
    # Aufnahme über USB Webcam
    fswebcam -q -d /dev/video0 -r 640x480 --no-banner $filename
fi

chown pi:pi $filename
