# Raspberry Pi Photobooth Skript


## Vorbereitungen
Damit das Python Skript auf einem Raspberry Pi so läuft wie gedacht sind folgende Schritte auszuführen
 - Raspbian in einer aktuellen Version auf einer Micro-SD-Karte installieren: [Link zur Anleitung](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
 - HDMI muss als default Videoausgabe angegeben sein. Dazu folgendes in `/boot/config.txt` ändern:
```
hdmi_force_hotplug=1
hdmi_drive=2
```
 - Über `raspi-config` unter *Advanced* den Tonausgang auf HDMI stellen
 - `/etc/kbd/config` editieren und dort mit `BLANK_TIME=0` die Bildschirmabschaltung deaktivieren
 - Der Fußtaster wird mittels Adapter (Klinkenbuchse auf Pfostenstecker) am Raspberry Pi angeschlossen. Dabei muss die Klinkenspitze mit GPIO 21, die Mitte mit GPIO 20 und die Basis mit GND verbunden sein. Interne Pull-Ups sorgen dafür, dass der Taster als Interrupt auslösender Schalter funktioniert. Die Belegung entspricht der von Canon Auslösern verwendeten [Link](http://www.doc-diy.net/photo/eos_wired_remote/)
 - Boot Cron Eintrag

## Konfiguration
```
color_background = (0, 255, 0)
color_foreground = (0, 0, 0)
seconds_countdown = 3
seconds_show_picture_no_interrupt = 3
seconds_show_picture_total = 10
text_anleitung = 'Der Fußtaster startet\nden Countdown\n\nBitte lächeln! :)'
path_photos = 'fotos'
gpio_shutter = 21
gpio_focus = 20
```

## Tipps
 - Defaultuser ist `pi` mit Passwort `raspberry`. Es empfiehlt sich das Passwort mit dem Kommand `passwd` oder mit `raspi-config` (sudo nicht vergessen) zu ändern!
 - Damit man testweise auch ein Bild mit einer USB Webcam aufnehmen kann muss *fswebcam* mit folgenden Kommandos installiert werden:
```
sudo apt-get update
sudo apt-get install fswebcam
```
   Im Skript `takepicture.sh` dann die entsprechenden Zeilen vom Kommentarzeichen befreien.
 - Konfiguration der Fotoaufnahme Parameter ebenfalls im Skript `takepicture.sh`


## Samba einrichten
 - Installieren mit `sudo apt-get install samba samba-common-bin`
 - Mit `sudo nano /etc/samba/smb.conf` die Konfiguration editieren. Dort `security = user` eintragen und folgendes hinten anhängen:
```
[Photobooth]
path = /home/pi/photobooth/html
writeable = yes
guest ok = no
```
 - `sudo smbpasswd -a pi` um einen Sambanutzer anzulegen (ohne "-a" um das Passwort zu ändern)
 - `sudo /etc/init.d/samba restart` startet Samba neu

Copyright Sebastian Herp
