import os
import tempfile
from subprocess import call as os_call
import subprocess
import parted


class MkFSException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class mkfs:
    """how to create a filesystem """
    def __init__(self, type='ext2'):
        self.cmd = 'mkfs.' + type
        self.cmdlst = ['sudo', self.cmd, '-q']

    def format(self, dev=None):
        if dev is None:
            raise MkFSException('A device is needed')
        os_call(self.cmdlst + [dev])

    def __str__(self):
        return self.cmd.split('.')[1]


class mk_vfat(mkfs):
    def __init__(self, type='vfat'):
        self.cmd = 'mkfs.' + type
        self.cmdlst = ['sudo', self.cmd]


class usbDev:
    def __init__(self, path):
        self.path = path
        self.device = parted.getDevice(path)
        self.part_prefix = ''
        self.parts = self.partitions()

    def __str__(self):
        return self.path

    def __eq__(self, other):
        if isinstance(other, str):
            return (other == self.path)
        return (self == other)

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
        pts = []
        disk = parted.Disk(self.device)
        for part in disk.partitions:
            pts.append((self.part_prefix + str(part.number),
                        part.fileSystem.type))
        return pts


# Makes a 20MB loopback device and creates partition table
class vUsbDev(usbDev):
    def _makeVDisk(self):
        self.parts = [('p1', 'junk')]
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
            self.part_prefix = 'p'
        os_call(['sudo', 'losetup', '-P', self.path, self.image_file])
        self.device = parted.getDevice(self.path)
        disk = parted.freshDisk(self.device, 'msdos')
        geom = parted.Geometry(self.device, start=1,
                               length=self.device.getLength() - 1)
        fs = parted.FileSystem('fat16', geom)
        new_part = parted.Partition(disk=disk, type=parted.PARTITION_NORMAL,
                                    fs=fs, geometry=geom)
        disk.addPartition(partition=new_part,
                          constraint=self.device.getConstraint())
        new_part.setFlag(parted.PARTITION_BOOT)
        try:
            disk.commit()
        except:
            pass
        self.format(mk_vfat(), 0)
        self.parts = self.partitions()
        self.__undoLo = ['sudo', 'losetup', '-d', self.path]

    def __init__(self, path):
        self.path = path
        self._makeVDisk()

    def __del__(self):
        for p in self.parts:
            os_call(['sudo', 'umount', self.path + p[0]])
        os_call(self.__undoLo)
        os.unlink(self.image_file)


def addFs(fs):
    global fileSystems
    fileSystems.append(fs)


def getUSBDevices(usbTab=[]):
    # copied verbetum from : http://unix.stackexchange.com/a/60335
    usbCmd = os.popen("grep -Hv '^0$' /sys/block/*/removable |"
                      " sed 's/removable:.*$/device\\/uevent/' |"
                      " xargs grep -H '^DRIVER=sd' |"
                      " sed 's/device.uevent.*$/size/' |"
                      " xargs grep -Hv '^0$' | cut -d / -f 4")
    devs = usbCmd.read().split('\n')[0:-1]
    if len(devs) == 0:
        usbTab.clear()
    for dev in devs:
        if len([d for d in usbTab if d == ('/dev/' + dev)]) == 0:
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
    addFs(mk_vfat())
if 'xfs' in cmds:
    addFs(mkfs('xfs'))
