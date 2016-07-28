# created by Rene Kjellerup 2016
# ISO Multiboot USB the Boot Menu options
# ref: https://wiki.archlinux.org/index.php/Multiboot_USB_drive


class BootMenuOption:
    """Base class for all boot menues"""
    def __init__(self):
        raise NotImplementedError

    def WriteMenu(self):
        raise NotImplementedError


class SubMenu(BootMenuOption):
    def __init__(self,name='more options',options=[]):
        self.options = options
        self.name = name

    def AddEntry(self, menu=None):
        if menu is None:
            return
        self.options.append(menu)

    def WriteMenu(self):
        str = "submenuentry \"{0}\" {\n".format(self.name)
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
        str = "menuentry \"{0}\" {\n".format(self.name)
        str += "  set ISOF={0}\n".format(self.iso)
        str += "  loopback loop \$ISOF \n"
        str += "  linux (loop)/live/vmlinuz boot=live config findiso=\$ISOF"
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
        str = "menuentry \"{0}\" {\n".format(self.name)
        str += "  set ISOF={0}\n".format(self.iso)
        str += "  loopback loop \$ISOF \n"
        str += "  linux16 (loop)/isolinux/gentoo root=/dev/ram0 init=/linuxrc"
        str += " aufs looptype=squashfs loop=/image.squashfs cdroot"
        str += " isoboot=\$ISOF vga=791 splash=silent,theme:default"
        str += " console=tty0"
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
        str = "menuentry \"{0}\" {\n".format(self.name)
        str += "  set ISOF={0}\n".format(self.iso)
        str += "  loopback loop \$ISOF \n"
        str += "  linux (loop)/isolinux/vmlinuz noeject"
        str += " inst.stage2=hd:{0}:$ISOF {1} \n".format(
            self.diskLabel, self.extra)
        str += "  initrd (loop)/isolinux/initrd.img \n"
        str += "}\n"
        return str
