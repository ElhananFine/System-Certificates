import os

os.system("adb kill-server")

#only for adb over wifi
#os.system("adb connect 192.168.10.189:5555")

#if not connected
devices= os.popen("adb devices").read().split('\n')
if (len(devices)==3):
    print("Could not find device")
    exit()
elif (len(devices)>4):
    print("More than one device is connected")
    exit()

#temp file with su shell commands reading user certs
commands= open("temp", "w+")
commands.write("su\nls /data/misc/user/0/cacerts-added/\n")
commands.close()

#assisng certs to varible
userCer = os.popen("adb shell < temp").read()
print (userCer.split())


#temp file with su shell commands to install certs
commands= open("temp", "w+")
commands.write("su\nmount -o rw,remount /system\ncp /data/misc/user/0/cacerts-added/* /system/etc/security/cacerts/\ncd /system/etc/security/cacerts/\nchmod 644 %s\nreboot"%userCer.replace("\n"," "))
commands.close()

#execute the installation
os.system("adb shell < temp")
os.remove("temp")

#Optional: Restart the phone:
#echo "Rebooting device"
#adb shell "su 0,0 -c reboot"

