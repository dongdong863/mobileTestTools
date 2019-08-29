@echo off
adb tcpip 5555
echo "please take off usb line,and then Enter...."
pause
adb connect %1:5555
ping -n 3 127.0.0.1>nul
adb shell /data/local/tmp/atx-agent server -d