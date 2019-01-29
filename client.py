import time
from datetime import datetime
import subprocess
from urllib import urlopen
import re

#video_lenght = 45
#timeout_lenght = 30

authkey = "cameracontroller"

cameraID = "1" ##CONFIGURE

state = "0"
downloaded = "0"

def stopProgram(reason):
    print("Program will exit:")
    print(reason)
    killprocess()
    exit()


def killprocess():
    p= subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)


def start_video():
    subprocess.call(["gphoto2", "--set-config", "viewfinder=1", "--set-config", "movierecordtarget=0"])
    print("Record started")

def stop_video():
    subprocess.call(["gphoto2", "--set-config", "viewfinder=1", "--set-config", "movierecordtarget=1"])
    print("Record stopped")

def getState():
    if("false" not in urlopen("http://localhost/client_camera_controller.php?method=GET&authkey=" + authkey).read()):
        if("download" not in urlopen("http://localhost/client_camera_controller.php?method=GET&authkey=" + authkey).read()):
	     return 1
	else:
	     return 2
    else:
	return 0


def startLoop():
    try:
        state = "0"
        global downloaded
	while True:
            if (getState() == 1 and state == "0"):
                start_video()
                state = "1"
		downloaded = "0"
            elif (getState() == 0):
                if(state == "1"):
                    stop_video()
                    state = "0"
		    download_video()
	    elif (getState() == 2 and downloaded == "0"):
		    download_video()
		    downloaded == "1"
            time.sleep(1)
            send_Summary()
    except (KeyboardInterrupt, SystemExit):
        stopProgram("")

def download_video():
    subprocess.call(["gphoto2", "--get-all-files", "--force-overwrite"])
    subprocess.call(["gphoto2", "--delete-all-files", "--recurse"])

def send_Summary():
    summary = 'None'
    try:
        process = subprocess.Popen(["gphoto2", "--summary"], stdout = subprocess.PIPE)
        summary_re = process.communicate()[0]

        battery_re = re.search('Batterie .*', summary_re)
        cardspace_re = re.search('Maximale .*', summary_re)
        emptycardspace_re = re.search('Freier .*', summary_re)

        battery = battery_re.group(0)
        cardspace = cardspace_re.group(0)
        emptycardspace = emptycardspace_re.group(0)
	
	if(downloaded == "0"):
        	summary = cameraID + '\n\n' + battery + '\n\n' + cardspace + '\n\n' + emptycardspace + '\n\n' + downloaded
	else:
		summary = "Downloading..."

        urlopen("http://localhost/client_camera_controller.php?method=STD&authkey=" + authkey + "&text=" + summary)
    except:
        print('Error')


print("------Camera-Controller by Marcin------")
print("Prepare...")
time.sleep(0.1)
print("Kill existing process")
killprocess()
time.sleep(0.5)
print("Starting...")
print("............................")
startLoop()
