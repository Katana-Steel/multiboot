import os

pfd = os.popen("find /usr/sbin /sbin -name 'mkfs.*'| cut -d. -f2 | sort")
cmds = pfd.read().split('\n')[0:-1]

fileSystems = []

class mkfs:
    """how to create a filesystem"""
    def __init__(self, type='ext2'):
        self.cmd = 'mkfs.' + type

    def format(self, dev=None):
        if dev is None:
            raise Exception('A device is needed')

    def __str__(self):
        return self.cmd.split('.')[1]

class usbDev:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

def addFs(fs):
    global fileSystems
    fileSystems.append(fs)

def getUSBDevices():
    usbTab = []
    # do logic to locate all attached USB flash drives
    usbTab.append(usbDev('/dev/sdb'))
    usbTab.append(usbDev('/dev/sde'))
    return usbTab

if 'ext4' in cmds:
    addFs(mkfs('ext4'))
if 'vfat' in cmds:
    addFs(mkfs('vfat'))
if 'xfs' in cmds:
    addFs(mkfs('xfs'))

