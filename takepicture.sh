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
    # Aufnahme �ber angeschlossene Kamera
    gphoto2 -q --capture-image-and-download --filename $filename
else
    # Aufnahme �ber USB Webcam
    fswebcam -q -d /dev/video0 -r 640x480 --no-banner $filename
fi

chown pi:pi $filename
