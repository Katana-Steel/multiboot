# multiboot
project to create a multi iso boot USB flash drive

## running

should be as simple as:
`python multiboot.py`

## test
```
cat test/teststart.py | python - | tee grub.cfg
```

## requirements

* python-qt5 or python3-pyqt5
* grub2 or grub
* filesystem creation tools of your choice, supported:
  * ext4
  * vfat
  * xfs
