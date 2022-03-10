#!/bin/bash
DISPLAY=:0.0 xrandr --output HDMI-2 --same-as HDMI-1
xrandr --output HDMI-1 --panning 1920x2160+0+0/0x0+0+0/0/0/0/0
xrandr --output HDMI-2 --pos 0x1080

python /home/pi/Inflyt-Projection/manage.py runserver &
chromium-browser --start-fullscreen http://127.0.0.1:8000/astroProjection/ &


