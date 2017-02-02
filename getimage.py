# written for klte running on RR-N-v5.8.0-20170117-klte-Official
# no guarantees of working with other devices or other ROMs
# requires android debugging allowed on the device and adb installed on the pc
# https://forum.xda-developers.com/showthread.php?t=2588979
import subprocess
import datetime

def getimage(camerapath = "storage/emulated/0/dcim/camera"):
    output = subprocess.check_output('adb shell ls "{0}" | grep "{1}"'.
                                     format(camerapath,
                                            datetime.
                                            datetime.
                                            now().
                                            strftime('%Y%m%d')))
    # getting files only with today's date to prevent searching
    # through thousands of strings
    output = str(output)
    output = output[2:-1:]
    output = output.split('\\r\\n')
    output = output[:-1:]
    filename = (max(output, key = lambda x: x[13:19:]))
    subprocess.run('adb pull "{0}/{1}" "cache.jpg"'.
                   format(camerapath,
                          filename))
    # download the latest file to the pc
    
if __name__ == '__main__':    
    getimage()
