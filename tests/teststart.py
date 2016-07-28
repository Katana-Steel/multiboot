import menu


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
m.append(menu.GentooISO(extra=gentoo_ex))

for x in m:
    print(x.WriteMenu())
