# written for klte running on RR-N-v5.8.0-20170117-klte-Official
# no guarantees of working with other devices or other ROMs
# requires android debugging enabled on the device and adb installed on the pc
# adb easy install: https://forum.xda-developers.com/showthread.php?t=2588979
import subprocess
import re

class AndroidDebuggingError(Exception): pass
    
def load(camerapath, target):
    try:
        output = subprocess.check_output('adb shell ls "{0}" -t | head -n 1'.format(camerapath))
    except subprocess.CalledProcessError:
        msg = "Android debbuging is disabled on the phone\n or the phone is disconnected."
        raise AndroidDebuggingError(msg)
    filename = re.search("IMG.*\.jpg", str(output))
    if not filename:
        msg = "No such file or directory on the phone."
        raise FileNotFoundError(msg)
    filename = filename[0]
    subprocess.run('adb pull "{0}/{1}" "{2}"'.
                   format(camerapath, filename, target))
    return True

def delimage():
    subprocess.run('del "cache.jpg"')
    return True        
