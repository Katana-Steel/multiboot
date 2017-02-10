import menu
import tempfile
from subprocess import call as os_call


m = [menu.MenuSetup(
    "set WIFI_EXEC='file:///lib/live/mount/findiso/install_wifi_driver.sh'"
    )
]
deb_hook = "hooks=$WIFI_EXEC"
gentoo_ex = ''
# gentoo_ex = 'aufs splash=silent,theme:default console=tty0'
m.append(menu.DebianLiveISO(extra=deb_hook))
sm = menu.SubMenu()
m.append(sm)
sm.AddEntry(menu.DebianLiveISO('/debian-xfce.iso',
                               name='Debian Xfce', extra=deb_hook))
sm.AddEntry(menu.CentOSISO(disk='/dev/sda1'))
sm.AddEntry(menu.UbuntuLiveISO())
m.append(menu.GentooISO(extra=gentoo_ex))

st = ''
for x in m:
    st += x.WriteMenu() + '\n'

script_check = None
# setting text mode here as I don't need binary
with tempfile.NamedTemporaryFile(mode='w') as f:
    d = f.write(st)
    del d
    f.flush()
    script_check = os_call(['grub-script-check', f.name])

if script_check is not None and script_check > 0:
    print('bad grub-menu generated')
else:
    print('the valid grub2 config is %d bytes' % len(st))
