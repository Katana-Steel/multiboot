import sys

if 'linux' in sys.platform:
    from .linux import fileSystems
    from .linux import getUSBDevices
    from .linux import getFakeUsb
else:
    raise ImportError
