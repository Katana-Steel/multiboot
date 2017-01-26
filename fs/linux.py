import os
import tempfile
from subprocess import call as os_call
import subprocess


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
        self.parts = [('1', 'vfat')]

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


# Makes a 20MB loopback device and creates partition table
class vUsbDev(usbDev):
    def _makeVDisk(self):
        self.parts[0] = ('p1', self.parts[0][1])
        self.image_file = self.path
        os_call(['dd', 'bs=4096', 'count=5000', 'if=/dev/zero',
                'of=' + self.image_file])
        with subprocess.Popen(['sudo', 'losetup', '-f'],
                              stdout=subprocess.PIPE,
                              universal_newlines=True) as lo_list:
            out = lo_list.stdout.read().split('\n')[:-1]
            if len(out) > 0:
                self.path = out[0]
            else:
                self.path = '/dev/loop0'
        os_call(['sudo', 'losetup', '-P', self.path, self.image_file])
        sfdisk_cmd = """
label: dos
label-id: 0x87b7e465
device: /dev/loop0
unit: sectors

/dev/loop0p1 : start=        2048, size=       37952, type=c
"""
        with subprocess.Popen(['sudo', 'sfdisk', self.path],
                              stdin=subprocess.PIPE,
                              universal_newlines=True) as fdisk:
            fdisk.communicate(input=sfdisk_cmd)
        os_call(['sudo', 'mkfs.vfat', self.path + self.parts[0][0]])
        self.__undoLo = ['sudo', 'losetup', '-d', self.path]

    def __init__(self, path):
        super().__init__(path)
        self._makeVDisk()

    def __del__(self):
        os_call(self.__undoLo)
        os.unlink(self.image_file)


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


def getFakeUsb():
    ret = None
    with tempfile.NamedTemporaryFile(delete=False) as f:
        ret = vUsbDev(f.name)
    return ret


fileSystems = []
pfd = os.popen("find /usr/sbin /sbin -name 'mkfs.*'| cut -d. -f2 | sort")
cmds = pfd.read().split('\n')[0:-1]
if 'ext4' in cmds:
    addFs(mkfs('ext4'))
if 'vfat' in cmds:
    addFs(mkfs('vfat'))
if 'xfs' in cmds:
    addFs(mkfs('xfs'))
