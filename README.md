# multiboot
project to create a multi iso boot USB flash drive

## test
```
cat test/teststart.py | python - | tee grub.cfg
```

## requirements

* python-qt5
* fsutils (for the filesystem you want on the USB drive)
* grub2
* python-usb (to ensure we are writing to a USB drive)
