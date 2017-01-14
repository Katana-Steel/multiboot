import os


class mkfs:
    """how to create a filesystem """
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
        self.parts = [(1, 'vfat')]

    def __str__(self):
        return self.path

    def format(self, fs, partno=0):
        """
        expects:
        * fs is an mkfs type
        * partno is the idx in the partitions list
        """
        p = str(self.parts[partno][0])
        fs.format(self.path + p)
        self.parts[partno] = (p, str(fs))

    def partitions(self):
        return self.parts


def addFs(fs):
    global fileSystems
    fileSystems.append(fs)


def getUSBDevices():
    usbTab = []
    # copied verbetum from : http://unix.stackexchange.com/a/60335
    usbCmd = os.popen("grep -Hv '^0$' /sys/block/*/removable |"
                      " sed 's/removable:.*$/device\\/uevent/' |"
                      " xargs grep -H '^DRIVER=sd' |"
                      " sed 's/device.uevent.*$/size/' |"
                      " xargs grep -Hv '^0$' | cut -d / -f 4")
    devs = usbCmd.read().split('\n')[0:-1]
    for dev in devs:
        usbTab.append(usbDev('/dev/' + dev))
    return usbTab


fileSystems = []
pfd = os.popen("find /usr/sbin /sbin -name 'mkfs.*'| cut -d. -f2 | sort")
cmds = pfd.read().split('\n')[0:-1]
if 'ext4' in cmds:
    addFs(mkfs('ext4'))
if 'vfat' in cmds:
    addFs(mkfs('vfat'))
if 'xfs' in cmds:
    addFs(mkfs('xfs'))
