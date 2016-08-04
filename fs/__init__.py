import sys

if 'linux' in sys.platform:
    from .linux import fileSystems
    from .linux import getUSBDevices
else:
    raise ImportError
