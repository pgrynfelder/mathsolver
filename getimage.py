# written for klte running on RR-N-v5.8.0-20170117-klte-Official
# no guarantees of working with other devices or other ROMs
# requires android debugging enabled on the device and adb installed on the pc
# adb easy install: https://forum.xda-developers.com/showthread.php?t=2588979
import subprocess
from re import search
    
def getimage(camerapath = "storage/emulated/0/dcim/camera"):
    try:
        output = subprocess.check_output('adb shell ls -t "{0}" | head -n 1'.
                                         format(camerapath))
    except subprocess.CalledProcessError:
        msg = "Android debbuging is disabled on the phone\n or the phone is disconnected"
        print("Error!\n", msg)
        return None
    #print(output)
    filename = search("IMG.*jpg", str(output))[0]
    print(filename)
    subprocess.run('adb pull "{0}/{1}" "cache.jpg"'.
                   format(camerapath, filename))
    
if __name__ == '__main__':
    getimage()
