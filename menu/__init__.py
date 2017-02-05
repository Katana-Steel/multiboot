# created by Rene Kjellerup 2016
# ISO Multiboot USB the Boot Menu options
# ref: https://wiki.archlinux.org/index.php/Multiboot_USB_drive


class BootMenuOption:
    """Base class for all boot menues"""
    def __init__(self):
        raise NotImplementedError

    def WriteMenu(self):
        raise NotImplementedError

    def SetMenuName(self, name):
        self.name = name

    def SetIsoImage(self, iso):
        self.iso = iso


class MenuSetup(BootMenuOption):
    def __init__(self, extra):
        self.extra = extra

    def WriteMenu(self):
        str = """set default="0"
insmod all_video
font=unicode

insmod part_msdos
insmod loopback
insmod gzio

set root='hd0,msdos1'

set gfxmode=auto
insmod gfxterm
set lang=en_US
insmod gettext

set timeout=5

{0}
""".format(self.extra)
        return str


class SubMenu(BootMenuOption):
    def __init__(self, name='more options', options=[]):
        self.options = options
        self.name = name

    def AddEntry(self, menu=None):
        if menu is None:
            return
        self.options.append(menu)

    def WriteMenu(self):
        str = "submenu \"{0}\" ".format(self.name)
        str += "{\n"
        for m in self.options:
            str += m.WriteMenu()
        str += "}\n"
        return str


class DebianLiveISO(BootMenuOption):
    def __init__(self, iso='/debian.iso', name='Debian', extra=''):
        self.iso = iso
        self.name = name
        self.extra = extra

    def WriteMenu(self):
        str = "menuentry \"{0}\" ".format(self.name)
        str += "{\n"
        str += "  set ISOF=\"{0}\"\n".format(self.iso)
        str += "  loopback loop $ISOF \n"
        str += "  linux (loop)/live/vmlinuz boot=live config findiso=$ISOF"
        str += " {0} \n".format(self.extra)
        str += "  initrd (loop)/live/initrd.img \n"
        str += "}\n"
        return str


class GentooISO(BootMenuOption):
    def __init__(self, iso='/gentoo.iso', name='Gentoo', extra=''):
        self.iso = iso
        self.name = name
        self.extra = extra

    def WriteMenu(self):
        str = "menuentry \"{0}\" ".format(self.name)
        str += "{\n"
        str += "  set ISOF=\"{0}\"\n".format(self.iso)
        str += "  loopback loop $ISOF \n"
        str += "  linux16 (loop)/isolinux/gentoo root=/dev/ram0 init=/linuxrc"
        str += " looptype=squashfs loop=/image.squashfs cdroot"
        str += " isoboot=$ISOF vga=791"
        str += " {0} \n".format(self.extra)
        str += "  initrd16 (loop)/isolinux/gentoo.xz \n"
        str += "}\n"
        return str


class CentOSISO(BootMenuOption):
    def __init__(self, iso='/centos.iso', name='CentOS', extra='', disk=''):
        self.iso = iso
        self.name = name
        self.extra = extra
        self.diskLabel = disk

    def WriteMenu(self):
        str = "menuentry \"{0}\" ".format(self.name)
        str += "{\n"
        str += "  set ISOF=\"{0}\"\n".format(self.iso)
        str += "  loopback loop $ISOF \n"
        str += "  linux (loop)/isolinux/vmlinuz noeject"
        str += " inst.stage2=hd:{0}:$ISOF {1} \n".format(
            self.diskLabel, self.extra)
        str += "  initrd (loop)/isolinux/initrd.img \n"
        str += "}\n"
        return str
