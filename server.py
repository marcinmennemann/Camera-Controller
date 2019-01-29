import time
from datetime import datetime
import subprocess
from urllib import urlopen
import threading
import os
import keyboard

cameraONEhost_ip = 'localhost' ##CONFIGURE
cameraTWOhost_ip = ''
cameraTHREEhost_ip = ''

video_lenght = 600
timeout_lenght = 240

authkey = "cameracontroller"

isOneInLoop = False
isTwoInLoop = False
isThreeInLoop = False

def stopProgram(reason):
    stop_video(1)
    stop_video(2)
    stop_video(3)

    print("Program will exit:")
    print(reason)
    exit()


def start_video(camera):
    if(camera == 1):
        sendSignal(1,1)
    elif(camera == 2):
        sendSignal(2, 1)
    elif(camera == 3):
        sendSignal(3,1)


def stop_video(camera):
    if(camera == 1):
        sendSignal(1,0)
    elif(camera == 2):
        sendSignal(2, 0)
    elif(camera == 3):
        sendSignal(3, 0)

def download_MOV(camera):
    if(camera == 1):
	sendSignal(1,3)
    elif(camera == 2):
	sendSignal(2,3)
    elif(camera == 3):
	sendSignal(3,3)

def sendSignal(camera, state):
    if(state == 1):
        if((camera == 1) and (len(cameraONEhost_ip) > 0)):
            urlopen("http://" + cameraONEhost_ip + "/client_camera_controller.php?method=START_RECORD&authkey=" + authkey)
        if((camera == 2) and (len(cameraTWOhost_ip) > 0)):
            urlopen("http://" + cameraTWOhost_ip + "/client_camera_controller.php?method=START_RECORD&authkey=" + authkey)
        if((camera == 3) and (len(cameraTHREEhost_ip) > 0)):
            urlopen("http://" + cameraTHREEhost_ip + "/client_camera_controller.php?method=START_RECORD&authkey=" + authkey)
    elif(state == 0):
        if((camera == 1) and (len(cameraONEhost_ip) > 0)):
            urlopen("http://" + cameraONEhost_ip + "/client_camera_controller.php?method=STOP_RECORD&authkey=" + authkey)
        if((camera == 2) and (len(cameraTWOhost_ip) > 0)):
            urlopen("http://" + cameraTWOhost_ip + "/client_camera_controller.php?method=STOP_RECORD&authkey=" + authkey)
        if((camera == 3) and (len(cameraTHREEhost_ip) > 0)):
            urlopen("http://" + cameraTHREEhost_ip + "/client_camera_controller.php?method=STOP_RECORD&authkey=" + authkey)
    elif(state == 2):
        if((camera == 1) and (len(cameraONEhost_ip) > 0)):
            return urlopen("http://" + cameraONEhost_ip + "/client_camera_controller.php?method=SUMMARY&authkey=" + authkey).read()
        if((camera == 2) and (len(cameraTWOhost_ip) > 0)):
            return urlopen("http://" + cameraTWOhost_ip + "/client_camera_controller.php?method=SUMMARY&authkey=" + authkey).read()
        if((camera == 3) and (len(cameraTHREEhost_ip) > 0)):
            return urlopen("http://" + cameraTHREEhost_ip + "/client_camera_controller.php?method=SUMMARY&authkey=" + authkey).read()
    elif(state == 3):
	if((camera == 1) and (len(cameraONEhost_ip) > 0)):
	    return urlopen("http://" + cameraONEhost_ip + "/client_camera_controller.php?method=DOWNLOAD&authkey=" + authkey).read()
	if((camera == 2) and (len(cameraTWOhost_ip) > 0)):
	    return urlopen("http://" + cameraTWOhost_ip + "/client_camera_controller.php?method=DOWNLOAD&authkey=" + authkey).read()
	if((camera == 3) and (len(cameraTHREEhost_ip) > 0)):
       	    return urlopen("http://" + cameraTHREEhost_ip + "/client_camera_controller.php?method=DOWNLOAD&authkey=" + authkey).read()


def get_camera_summary(camera):
    if(camera == 1):
        return sendSignal(1,2)
    if(camera == 2):
        return sendSignal(2,2)
    if(camera == 3):
        return sendSignal(3,2)

def startLoop(treadname):
    global isOneInLoop
    global isTwoInLoop
    global isThreeInLoop
    try:
        while True:
            print("Loop-Record Start\n\nCamera-States:\nOne: %r\nTwo: %r\nThree: %r\n\n\n\n" % (isOneInLoop,isTwoInLoop,isThreeInLoop))
            time.sleep(5)
            if(isOneInLoop):
                start_video(1)
            if(isTwoInLoop):
                start_video(2)
            if(isThreeInLoop):
                start_video(3)
            if(len(cameraONEhost_ip) > 0):
                print("------------------------")
                print(get_camera_summary(1) + "\n\n")
            time.sleep(10)
            if(len(cameraTWOhost_ip) > 0):
                print("------------------------")
                print(get_camera_summary(2) + "\n\n")
            time.sleep(10)
            if(len(cameraTHREEhost_ip) > 0):
                print("------------------------")
                print(get_camera_summary(3) + "\n\n")
            print("------------------------")
            time.sleep(video_lenght - 25)
            print("Loop-Record Pause")
            stop_video(1)
            stop_video(2)
            stop_video(3)
            time.sleep(timeout_lenght)
    except (KeyboardInterrupt, SystemExit):
        stopProgram("")


def key_trigger(threadname):
    global isOneInLoop
    global isTwoInLoop
    global isThreeInLoop
    try:
        while True:
            if(keyboard.is_pressed('q')):
                time.sleep(0.3)
                #start_video(1)
                isOneInLoop = True
            if(keyboard.is_pressed('w')):
                time.sleep(0.3)
                #start_video(2)
                isTwoInLoop = True
            if(keyboard.is_pressed('e')):
                time.sleep(0.3)
                #start_video(3)
                isThreeInLoop = True
            if(keyboard.is_pressed('a')):
                time.sleep(0.3)
                stop_video(1)
                isOneInLoop = False
            if(keyboard.is_pressed('s')):
                time.sleep(0.3)
                stop_video(2)
                isTwoInLoop = False
            if(keyboard.is_pressed('d')):
                time.sleep(0.3)
                stop_video(3)
                isThreeInLoop = False
	    if(keyboard.is_pressed('y')):
		time.sleep(0.3)
		stop_video(1)
		isOneInLoop = False
		time.sleep(2)
		download_MOV(1)
		time.sleep(0.2)
		print("\nDownlaod 1 Started")
		time.sleep(180)
		print("\nDownloaded")
	    if(keyboard.is_pressed('x')):
                time.sleep(0.3)
		stop_video(2)
		isTwoInLoop = False
		time.sleep(2)
                download_MOV(2)
                time.sleep(0.2)
                print("\nDownlaod 2 Started")
		time.sleep(180)
                print("\nDownloaded")
	    if(keyboard.is_pressed('c')):
                time.sleep(0.3)
		stop_video(3)
		isThreeInLoop = False
		time.sleep(2)
                download_MOV(3)
                time.sleep(0.2)
                print("\nDownlaod 3 Started")
		time.sleep(180)
                print("\nDownloaded")
	    if(keyboard.is_pressed('t')):
		time.sleep(0.3)
		print(get_camera_summary(1))
	    if(keyboard.is_pressed('g')):
                time.sleep(0.3)
                print(get_camera_summary(2))
	    if(keyboard.is_pressed('b')):
                time.sleep(0.3)
                print(get_camera_summary(3))

    except (KeyboardInterrupt, SystemExit):
        stopProgram("")

def loopCheck():
    global isOneInLoop
    global isTwoInLoop
    global isThreeInLoop
    if(len(cameraONEhost_ip) > 0):
        isOneInLoop = True
    if(len(cameraTWOhost_ip) > 0):
        isTwoInLoop = True
    if(len(cameraTHREEhost_ip) > 0):
        isThreeInLoop = True


print("------Camera-Controller by Marcin------")
print("Prepare...")
time.sleep(0.1)
loopCheck()
time.sleep(0.5)
print("Checking if Web Servers are available...")
print("Starting...")
if __name__ == '__main__':
    loop_process =  threading.Thread(target=startLoop, args=('Thread-1',))
    trigger_process = threading.Thread(target=key_trigger, args=('Thread-2',))

    loop_process.start()
    trigger_process.start()

    loop_process.join()
    trigger_process.join()
