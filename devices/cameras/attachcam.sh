#!/bin/bash
sudo usbip list --remote=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
sudo usbip attach --remote=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}') --busid=1-3
sudo chmod 777 /dev/video0
ffplay -f video4linux2 -input_format mjpeg -framerate 30 -video_size 640*480 /dev/video0