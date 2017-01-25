import fs
import sys

my_USB = fs.linux.usbDev('/dev/null')
print(my_USB.partitions())
ext4fs = fs.linux.mkfs('ext4')
my_USB.format(ext4fs, 0)
if 'ext4' not in my_USB.partitions()[0][1]:
    print('format failed')
    sys.exit(1)
print(my_USB.partitions())
