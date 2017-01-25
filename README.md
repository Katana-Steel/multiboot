# multiboot
project to create a multi iso boot USB flash drive

## running

should be as simple as:
`python multiboot.py`

## test
```
for t in tests/*; do
  echo $(basename $t)
  cat $t | python3 - 
done
```

## requirements

* python-qt5 or python3-pyqt5
* grub2 or grub
* filesystem creation tools of your choice, supported:
  * ext4
  * vfat
  * xfs

## todo

I still need to correctly detect the actual filesystem on the USB drive
although the general default 'vfat' as most USBs come preformatted as.

next need to install grub and write the generated grub.cfg to the seleted USB.
something simple like this:
```
sudo sfdisk /dev/sdb --part-type 1 83
sudo sfdisk -A /dev/sdb 1
sudo mkfs.xfs /dev/sdb1
sudo grub-install /dev/sdb
```
with
```
import menu

def CreateBootMenu(mnt_pnt):
    m = [menu.MenuSetup()]
    deb_hook = ""
    gentoo_ex = ''

    m.append(menu.DebianLiveISO(extra=deb_hook))
    sm = menu.SubMenu()
    m.append(sm)
    sm.AddEntry(menu.DebianLiveISO('/debian-xfce.iso',
                            name='Debian Xfce', extra=deb_hook))
    sm.AddEntry(menu.CentOSISO(disk='/dev/sda1'))
    m.append(menu.GentooISO(extra=gentoo_ex))

    with open(mnt_pnt + '/grub/grub.cfg', 'w') as grub_menu:
        for x in m:
            grub_menu.write(x.WriteMenu() + '\n')
```
