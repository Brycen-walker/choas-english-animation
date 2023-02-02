import os
import re
import colorama
from colorama import init, Fore, Back, Style

colorama.init(autoreset = True)

print("\n")
input("are you teeing output (python3 script.py | tee script.out)? ")

os.system("mkdir backups")
os.system("cp /etc/passwd backups/")
os.system("cp /etc/group backups/")
os.system("cp /etc/shadow backups/")
os.system("cp /etc/sysctl.conf backups/")
os.system("cp -r /etc/pam.d backups/")
os.system("cp /etc/fstab backups/")



print("\n\n")
print(Fore.YELLOW + Back.WHITE +"Questions")
main_user = input("who is your main user: ")

vsftpd_ask = input("is vsftpd a critical service(y/n): ")
vsftpd_ask = vsftpd_ask.lower()
apache2_ask = input("is apache2 a critical service(y/n): ")
apache2_ask = apache2_ask.lower()
"""
#for practice
os.system(f"cat /home/{main_user}/Desktop/ReadMe.desktop | grep \".html\" | cut -d \" \" -f2 > location.txt")
with open("location.txt", "r") as file:
        readme_loc = file.read().split()
for i in readme_loc:
        readme_loc = i
readme_loc = re.sub("\n",'', readme_loc)
"""

#for comps

readme_loc = "readme.html"


os.system("cat /etc/passwd | grep 'sh$' | grep -v root | cut -d':' -f1 > users.txt")

with open("users.txt","r") as file:
	users = file.read().lower().split("\n")
os.system("rm users.txt")

if users[-1] == '':
	users = users[:-1]

os.system(f'cat {readme_loc} | grep "Authorized Administrators:"  -A 15 | sed "s/<.>//" | sed "s/<..>//"  | sed "s/<...>//" | sed "s/<....>//" | sed "s/<.....>//"  | grep -v "Authorized" | grep -v "password" | cut -d" " -f1 | sed "/^[[:space:]]*$/d"  > al_users.txt')

with open("al_users.txt", "r") as file:
	allowed_users = file.read().lower().split("\n")
if allowed_users[-1] == '':
	allowed_users = allowed_users[:-1]

os.system(f"cat {readme_loc} | grep \"Authorized Administrators:\"  -A 15 | sed \"s/<.>//\" | sed \"s/<..>//\"  | sed \"s/<...>//\" | sed \"s/<....>//\" | sed \"s/<.....>//\"  | sed \"/^[[:space:]]*$/d\" | grep \"Authorized Users:\" -A 10 | grep -v \"Authorized Users:\" > non_auth_users.txt")

with open("non_auth_users.txt", "r") as file:
	non_auth_users = file.read().lower().split("\n")

if non_auth_users[-1] == '':
	non_auth_users = non_auth_users[:-1]
os.system("rm non_auth_users.txt; rm al_users.txt")


auth_users = []

for i in allowed_users:
	if i not in non_auth_users:
		auth_users.append(i)

os.system('cat /etc/group | grep "sudo" | cut -d ":" -f4 > sudo_users.txt')

with open("sudo_users.txt","r") as file:
	sudo_users = file.read().lower().split(",")
os.system("rm sudo_users.txt")
sudo_users[-1] = re.sub("\n", '', sudo_users[-1])

not_auth_sudoers = []

for i in sudo_users:
	if i not in auth_users:
		not_auth_sudoers.append(i)

not_sudoed_auth = []

for i in auth_users:
	if i not in sudo_users:
		not_sudoed_auth.append(i)

adm_users = os.popen('cat /etc/group | grep "^adm:" | cut -d ":" -f4 | sed "s/syslog//" | sed "s/^,//" | sed "s/,$//" | sed "s/,,/,/" | tr -d "\n"').read().split(",")

not_auth_admers = []

for i in adm_users:
	if i not in auth_users:
		not_auth_admers.append(i)

not_admed_auth = []

for i in auth_users:
	if i not in adm_users:
		not_admed_auth.append(i)
yes_list = ["y","yes","ya","ye","yas","t","u","i","h","g","j"]


print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Add needed users to sudo and adm groups")
#add users who need sudo to sudo group
print("")
print(not_sudoed_auth)
add_sudo_q = input("add these users to sudo group(y/n)? ")


if add_sudo_q in yes_list: 
	for i in not_sudoed_auth:
		sudo_start = os.popen('cat /etc/group | grep "^sudo:" | tr -d "\n"').read()
		os.system(f"sed -i 's/{sudo_start}/&,{i}/' /etc/group")

#add users who need adm to adm group
print("")
print(not_admed_auth)
add_adm_q = input("add these users to adm group(y/n)? ")

if add_adm_q in yes_list:
	for i in not_admed_auth:
		adm_start = os.popen('cat /etc/group | grep "^adm:" | tr -d "\n"').read()
		os.system(f"sed -i 's/{adm_start}/&,{i}/' /etc/group")

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"remove users in sudo and adm groups")
#remove not authroized sudo users
print("")
print(not_auth_sudoers)
rem_sudo_q = input("remove these users from sudo group(y/n)? ")

if rem_sudo_q in yes_list:
	for user in not_auth_sudoers:
		sudo_start = os.popen('cat /etc/group | grep "^sudo:" | tr -d "\n"').read()
		new_sudo = re.sub(user,'',sudo_start)
		new_sudo = re.sub(",,",",",new_sudo)
		new_sudo = re.sub(",$","",new_sudo)
		new_sudo = re.sub(":,",":",new_sudo)
		os.system(f'sed -i "s/{sudo_start}/{new_sudo}/" /etc/group')



#remove not authroized amd users
print("")
print(not_auth_admers)
rem_auth_q = input("remove these users from adm group(y/n)? ")

if rem_auth_q in yes_list:
	for user in not_auth_admers:
		adm_start = os.popen('cat /etc/group | grep "^adm:" | tr -d "\n"').read()
		new_adm = re.sub(user,'',adm_start)
		new_adm = re.sub(",,",",",new_adm)
		new_adm = re.sub(",$","",new_adm)
		new_adm = re.sub(":,",":",new_adm)
		os.system(f'sed -i "s/{adm_start}/{new_adm}/" /etc/group')


print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"remove unauthorized users")
#remove unauthorized users from the system
print("")

disallowed_users_on_sys = []
for user in users:
	if user not in allowed_users:
		disallowed_users_on_sys.append(user)
print(','.join(disallowed_users_on_sys))
if input("do you want to delete these users(y/n): ") == 'y':
	for user in disallowed_users_on_sys:
		os.system(f'deluser {user}')

"""
#disable unauthorized users from the system
for user in users:
	if user not in allowed_users:
		disable_user = os.popen(f'cat /etc/passwd | grep "^{user}" | tr -d "\n"').read()
		start_disable_user = os.popen(f'cat /etc/passwd | grep "^{user}" | sed "s/\/bin\/bash//" | sed "s/\/bin\/sh//" | tr -d "\n"').read()
		disable_user = re.sub("/","\/",disable_user)
		start_disable_user = re.sub("/","\/",start_disable_user)
		os.system(f'sed -i "s/{disable_user}/{start_disable_user}\/usr\/sbin\/nologin/" /etc/passwd')
"""


print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Add needed users to the system")
# add users that should be on system
print("")

add_users_blah = []
for i in allowed_users:
	if i not in users:
		add_users_blah.append(i)

print(','.join(add_users_blah))
add_users_q = input("add these users to the system(y/n)? ")

if add_users_q in yes_list:
	for i in allowed_users:
		if i not in users:
			os.system(f"groupdel {i} 2>/dev/null")
			os.system(f"useradd -s /bin/bash {i}")

users =  os.popen("cat /etc/passwd | awk -F: '$3 > 999 && $3 < 65534 {print $1}' | tr '\n' ','; echo 'root'").read().split(',')
users[-1] = re.sub("\n","",users[-1])
if users[-1] == '':
	users = users[:-1]

users.remove(f'{main_user}')

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Printing users with UID or GID of zero")
print("\n")
#print users with UID or GID 0
os.system("cat /etc/passwd |  awk -F':' '$4 == 0 ||  $3 == 0 {print $1\":\"$3\":\"$4}'")

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Changed all user passwords (Sup3rP@ssw0rd123!)")
# change all user passwords
password = "Sup3rP@ssw0rd123!"

with open("pased.sh","w") as file:
	file.write(f"#!/bin/bash\n")
for i in users:
	with open("pased.sh","a") as file:
		file.write(f'echo -e \"{password}\\n{password}\" | $(passwd {i})')
		file.write("\n")
os.system("chmod +x pased.sh")
os.system("./pased.sh")
os.system("rm pased.sh")

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Locked root account")
os.system("usermod -L root")
os.system("passwd -l root &>/dev/null")


#/etc/skel stuff

default_skel = ['/etc/skel/', '/etc/skel/.bash_logout', '/etc/skel/.profile', '/etc/skel/.bashrc','/etc/skel/.mozilla']

skel_files = os.popen("find /etc/skel/").read().split("\n")
if skel_files[-1] == '':
	skel_files = skel_files[:-1]

not_default_skel = []

for file in skel_files:
        if file not in default_skel:
                not_default_skel.append(file)

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Printing non default skel files")
print("\n")
#print non default skel files
for i in not_default_skel:
	print(i)

for file in not_default_skel:
	cur_file = os.popen(f'echo -n "{file}" | rev | cut -d"/" -f1 | rev | tr -d "\n"').read()
	#print non dfault skel files in home direcotry
	os.system(f'find /home/ -iname "{cur_file}"')


#non default groups
default_groups = ['root', 'mlocate', 'daemon', 'bin', 'sys', 'adm', 'tty', 'disk', 'lp', 'mail', 'news', 'uucp', 'man', 'proxy', 'kmem', 'dialout', 'fax', 'voice', 'cdrom', 'floppy', 'tape', 'sudo', 'audio', 'dip', 'www-data', 'backup', 'operator', 'list', 'irc', 'src', 'gnats', 'shadow', 'utmp', 'video', 'sasl', 'plugdev', 'staff', 'games', 'users', 'nogroup', 'systemd-journal', 'systemd-network', 'systemd-resolve', 'systemd-timesync', 'crontab', 'messagebus', 'input', 'kvm', 'render', 'syslog', 'tss', 'bluetooth', 'ssl-cert', 'uuidd', 'tcpdump', 'avahi-autoipd', 'rtkit', 'ssh', 'netdev', 'lpadmin', 'avahi', 'scanner', 'saned', 'nm-openvpn', 'whoopsie', 'colord', 'geoclue', 'pulse', 'pulse-access', 'gdm', 'sssd', 'lxd', 'student', 'sambashare', 'systemd-coredump']

cur_groups = os.popen('cat /etc/group | cut -d":" -f1').read().split("\n")
if cur_groups[-1] == '':
	cur_groups = cur_groups[:-1]

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Printing non default groups")
#printing non default groups
for group in cur_groups:
	if group not in default_groups:
		print(group)

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Printing non default sudoers stuff")
print("\n")
#print non default /etc/sudoers stuff
os.system("cat /etc/sudoers | grep -v '#\|%sudo[[:space:]]ALL=(ALL:ALL) ALL\|%admin ALL=(ALL) ALL\|root[[:space:]]ALL=(ALL:ALL) ALL\|Defaults[[:space:]]env_reset\|Defaults[[:space:]]mail_badpass\|Defaults[[:space:]]secure_path=\"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\"'")

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"remove all users from nopasswdlogin group")
#remove users from nopasswdlogin group

nopasswd_start = os.popen("cat /etc/group | grep '^nopasswdlogin' | awk -F':' '{print $1\":\"$2\":\"$3\":\"}' |tr -d '\n'").read()
nopasswd_long = os.popen("cat /etc/group | grep '^nopasswdlogin'| tr -d '\n'").read()
nopasswd_users = os.popen("cat /etc/group | grep '^nopasswdlogin' | cut -d':' -f4 | tr -d '\n'").read().split(',')

os.system(f"sed -i 's/{nopasswd_long}/{nopasswd_start}/' /etc/group")

"""
default_sources = 
deb http://us.archive.ubuntu.com/ubuntu/ jammy main restricted

deb http://us.archive.ubuntu.com/ubuntu/ jammy-updates main restricted

deb http://us.archive.ubuntu.com/ubuntu/ jammy universe
deb http://us.archive.ubuntu.com/ubuntu/ jammy-updates universe

deb http://us.archive.ubuntu.com/ubuntu/ jammy multiverse
deb http://us.archive.ubuntu.com/ubuntu/ jammy-updates multiverse

deb http://us.archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse

deb http://security.ubuntu.com/ubuntu jammy-security main restricted
deb http://security.ubuntu.com/ubuntu jammy-security universe
deb http://security.ubuntu.com/ubuntu jammy-security multiverse

with open("/etc/apt/sources.list","w") as file:
        file.write(default_sources)
print("\n\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"sources.list changed to default")
"""

#os.system("apt update 1>/dev/null 2>/dev/null")
#print("\n")
#print(Fore.RED + Back.WHITE + Style.BRIGHT +"apt updated")


#print("\n")
#print(Fore.BLUE + Style.BRIGHT +"apt upgrading...")

#os.system("echo 'printing line count: ';apt upgrade -y 2>/dev/null | pv --line-mode -b > /dev/null")
#print("\n")
#print(Fore.RED + Back.WHITE + Style.BRIGHT +"apt upgraded")
#print("\n\n")
#os.system("apt dist-upgrade -y &>/dev/null")

#os.system("update-manager –d & 1>/dev/null 2>/dev/null")

print(Fore.RED + Back.WHITE + Style.BRIGHT +"Held packages (apt-mark unhold <package_name>)")
print("\n")
os.system("apt-mark showhold")
print("\n\n")

default_packs = """accountsservice
acl
acpi-support
acpid
adduser
adwaita-icon-theme
alsa-base
alsa-topology-conf
alsa-ucm-conf
alsa-utils
amd64-microcode
anacron
apg
apparmor
apport
apport-gtk
apport-symptoms
appstream
apt
apt-config-icons
apt-config-icons-hidpi
apt-utils
aptdaemon
aptdaemon-data
apturl
apturl-common
aspell
aspell-en
at-spi2-core
avahi-autoipd
avahi-daemon
avahi-utils
base-files
base-passwd
bash
bash-completion
bc
bind9-dnsutils
bind9-host
bind9-libs:amd64
binutils
binutils-common:amd64
binutils-x86-64-linux-gnu
bluez
bluez-cups
bluez-obexd
bolt
brltty
bsd-mailx
bsdextrautils
bsdutils
bubblewrap
busybox-initramfs
busybox-static
bzip2
ca-certificates
cheese-common
chkrootkit
colord
colord-data
command-not-found
console-setup
console-setup-linux
coreutils
cpio
cpp
cpp-11
cracklib-runtime
cron
cups
cups-browsed
cups-bsd
cups-client
cups-common
cups-core-drivers
cups-daemon
cups-filters
cups-filters-core-drivers
cups-ipp-utils
cups-pk-helper
cups-ppdc
cups-server-common
dash
dbus
dbus-user-session
dc
dconf-cli
dconf-gsettings-backend:amd64
dconf-service
debconf
debconf-i18n
debianutils
desktop-file-utils
dictionaries-common
diffutils
dirmngr
distro-info
distro-info-data
dmidecode
dmsetup
dmz-cursor-theme
dns-root-data
dnsmasq-base
docbook-xml
dosfstools
dpkg
e2fsprogs
ed
efibootmgr
eject
emacsen-common
enchant-2
eog
espeak-ng-data:amd64
ethtool
evince
evince-common
evolution-data-server
evolution-data-server-common
fdisk
file
file-roller
findutils
firmware-sof-signed
fontconfig
fontconfig-config
fonts-beng
fonts-beng-extra
fonts-dejavu-core
fonts-deva
fonts-deva-extra
fonts-droid-fallback
fonts-freefont-ttf
fonts-gargi
fonts-gubbi
fonts-gujr
fonts-gujr-extra
fonts-guru
fonts-guru-extra
fonts-indic
fonts-kacst
fonts-kacst-one
fonts-kalapi
fonts-khmeros-core
fonts-knda
fonts-lao
fonts-lato
fonts-liberation
fonts-liberation2
fonts-lklug-sinhala
fonts-lohit-beng-assamese
fonts-lohit-beng-bengali
fonts-lohit-deva
fonts-lohit-gujr
fonts-lohit-guru
fonts-lohit-knda
fonts-lohit-mlym
fonts-lohit-orya
fonts-lohit-taml
fonts-lohit-taml-classical
fonts-lohit-telu
fonts-mlym
fonts-nakula
fonts-navilu
fonts-noto-cjk
fonts-noto-color-emoji
fonts-noto-mono
fonts-opensymbol
fonts-orya
fonts-orya-extra
fonts-pagul
fonts-sahadeva
fonts-samyak-deva
fonts-samyak-gujr
fonts-samyak-mlym
fonts-samyak-taml
fonts-sarai
fonts-sil-abyssinica
fonts-sil-padauk
fonts-smc
fonts-smc-anjalioldlipi
fonts-smc-chilanka
fonts-smc-dyuthi
fonts-smc-gayathri
fonts-smc-karumbi
fonts-smc-keraleeyam
fonts-smc-manjari
fonts-smc-meera
fonts-smc-rachana
fonts-smc-raghumalayalamsans
fonts-smc-suruma
fonts-smc-uroob
fonts-taml
fonts-telu
fonts-telu-extra
fonts-teluguvijayam
fonts-thai-tlwg
fonts-tibetan-machine
fonts-tlwg-garuda
fonts-tlwg-garuda-ttf
fonts-tlwg-kinnari
fonts-tlwg-kinnari-ttf
fonts-tlwg-laksaman
fonts-tlwg-laksaman-ttf
fonts-tlwg-loma
fonts-tlwg-loma-ttf
fonts-tlwg-mono
fonts-tlwg-mono-ttf
fonts-tlwg-norasi
fonts-tlwg-norasi-ttf
fonts-tlwg-purisa
fonts-tlwg-purisa-ttf
fonts-tlwg-sawasdee
fonts-tlwg-sawasdee-ttf
fonts-tlwg-typewriter
fonts-tlwg-typewriter-ttf
fonts-tlwg-typist
fonts-tlwg-typist-ttf
fonts-tlwg-typo
fonts-tlwg-typo-ttf
fonts-tlwg-umpush
fonts-tlwg-umpush-ttf
fonts-tlwg-waree
fonts-tlwg-waree-ttf
fonts-ubuntu
fonts-urw-base35
fonts-yrsa-rasa
foomatic-db-compressed-ppds
fprintd
friendly-recovery
ftp
fuse3
fwupd
fwupd-signed
gamemode
gamemode-daemon
gcc-11-base:amd64
gcc-12-base:amd64
gcr
gdb
gdisk
gdm3
gedit
gedit-common
geoclue-2.0
gettext-base
ghostscript
ghostscript-x
gir1.2-accountsservice-1.0:amd64
gir1.2-adw-1:amd64
gir1.2-atk-1.0:amd64
gir1.2-atspi-2.0:amd64
gir1.2-dbusmenu-glib-0.4:amd64
gir1.2-dee-1.0
gir1.2-freedesktop:amd64
gir1.2-gck-1:amd64
gir1.2-gcr-3:amd64
gir1.2-gdesktopenums-3.0:amd64
gir1.2-gdkpixbuf-2.0:amd64
gir1.2-gdm-1.0:amd64
gir1.2-geoclue-2.0:amd64
gir1.2-glib-2.0:amd64
gir1.2-gmenu-3.0:amd64
gir1.2-gnomebluetooth-3.0:amd64
gir1.2-gnomedesktop-3.0:amd64
gir1.2-goa-1.0:amd64
gir1.2-graphene-1.0:amd64
gir1.2-gstreamer-1.0:amd64
gir1.2-gtk-3.0:amd64
gir1.2-gtk-4.0:amd64
gir1.2-gtksource-4:amd64
gir1.2-gweather-3.0:amd64
gir1.2-handy-1:amd64
gir1.2-harfbuzz-0.0:amd64
gir1.2-ibus-1.0:amd64
gir1.2-javascriptcoregtk-4.0:amd64
gir1.2-json-1.0:amd64
gir1.2-mutter-10:amd64
gir1.2-nm-1.0:amd64
gir1.2-nma-1.0:amd64
gir1.2-notify-0.7:amd64
gir1.2-packagekitglib-1.0
gir1.2-pango-1.0:amd64
gir1.2-peas-1.0:amd64
gir1.2-polkit-1.0
gir1.2-rsvg-2.0:amd64
gir1.2-secret-1:amd64
gir1.2-snapd-1:amd64
gir1.2-soup-2.4:amd64
gir1.2-unity-7.0:amd64
gir1.2-upowerglib-1.0:amd64
gir1.2-vte-2.91:amd64
gir1.2-webkit2-4.0:amd64
gir1.2-wnck-3.0:amd64
gjs
gkbd-capplet
glib-networking:amd64
glib-networking-common
glib-networking-services
gnome-accessibility-themes
gnome-bluetooth
gnome-bluetooth-3-common
gnome-bluetooth-common
gnome-calculator
gnome-characters
gnome-control-center
gnome-control-center-data
gnome-control-center-faces
gnome-desktop3-data
gnome-disk-utility
gnome-font-viewer
gnome-initial-setup
gnome-keyring
gnome-keyring-pkcs11:amd64
gnome-logs
gnome-menus
gnome-online-accounts
gnome-power-manager
gnome-remote-desktop
gnome-session-bin
gnome-session-canberra
gnome-session-common
gnome-settings-daemon
gnome-settings-daemon-common
gnome-shell
gnome-shell-common
gnome-shell-extension-appindicator
gnome-shell-extension-desktop-icons-ng
gnome-shell-extension-ubuntu-dock
gnome-startup-applications
gnome-system-monitor
gnome-terminal
gnome-terminal-data
gnome-themes-extra:amd64
gnome-themes-extra-data
gnome-user-docs
gnupg
gnupg-l10n
gnupg-utils
gpg
gpg-agent
gpg-wks-client
gpg-wks-server
gpgconf
gpgsm
gpgv
grep
groff-base
grub-common
grub-efi-amd64-bin
grub-efi-amd64-signed
grub-gfxpayload-lists
grub-pc
grub-pc-bin
grub2-common
gsettings-desktop-schemas
gsettings-ubuntu-schemas
gstreamer1.0-alsa:amd64
gstreamer1.0-clutter-3.0:amd64
gstreamer1.0-gl:amd64
gstreamer1.0-packagekit
gstreamer1.0-pipewire:amd64
gstreamer1.0-plugins-base:amd64
gstreamer1.0-plugins-base-apps
gstreamer1.0-plugins-good:amd64
gstreamer1.0-pulseaudio:amd64
gstreamer1.0-tools
gstreamer1.0-x:amd64
gtk-update-icon-cache
gtk2-engines-murrine:amd64
gtk2-engines-pixbuf:amd64
gvfs:amd64
gvfs-backends
gvfs-common
gvfs-daemons
gvfs-fuse
gvfs-libs:amd64
gzip
hdparm
hicolor-icon-theme
hostname
hplip
hplip-data
htop
humanity-icon-theme
hunspell-en-us
ibus
ibus-data
ibus-gtk:amd64
ibus-gtk3:amd64
ibus-gtk4:amd64
ibus-table
iio-sensor-proxy
im-config
info
init
init-system-helpers
initramfs-tools
initramfs-tools-bin
initramfs-tools-core
inputattach
install-info
intel-microcode
ipp-usb
iproute2
iptables
iputils-ping
iputils-tracepath
irqbalance
isc-dhcp-client
isc-dhcp-common
iso-codes
iucode-tool
javascript-common
john
john-data
kbd
kerneloops
keyboard-configuration
klibc-utils
kmod
language-pack-en
language-pack-en-base
language-pack-gnome-en
language-pack-gnome-en-base
language-selector-common
language-selector-gnome
laptop-detect
less
libaa1:amd64
libabsl20210324:amd64
libaccountsservice0:amd64
libacl1:amd64
libadwaita-1-0:amd64
libao-common
libao4:amd64
libapparmor1:amd64
libappstream4:amd64
libapt-pkg6.0:amd64
libarchive13:amd64
libargon2-1:amd64
libasound2:amd64
libasound2-data
libasound2-plugins:amd64
libaspell15:amd64
libassuan0:amd64
libasyncns0:amd64
libatasmart4:amd64
libatk-adaptor:amd64
libatk-bridge2.0-0:amd64
libatk1.0-0:amd64
libatk1.0-data
libatkmm-1.6-1v5:amd64
libatm1:amd64
libatopology2:amd64
libatspi2.0-0:amd64
libattr1:amd64
libaudit-common
libaudit1:amd64
libauthen-sasl-perl
libavahi-client3:amd64
libavahi-common-data:amd64
libavahi-common3:amd64
libavahi-core7:amd64
libavahi-glib1:amd64
libavc1394-0:amd64
libayatana-appindicator3-1
libayatana-ido3-0.4-0:amd64
libayatana-indicator3-7:amd64
libbabeltrace1:amd64
libbinutils:amd64
libblkid1:amd64
libblockdev-crypto2:amd64
libblockdev-fs2:amd64
libblockdev-loop2:amd64
libblockdev-part-err2:amd64
libblockdev-part2:amd64
libblockdev-swap2:amd64
libblockdev-utils2:amd64
libblockdev2:amd64
libbluetooth3:amd64
libboost-regex1.74.0:amd64
libbpf0:amd64
libbrlapi0.8:amd64
libbrotli1:amd64
libbsd0:amd64
libbz2-1.0:amd64
libc-bin
libc6:amd64
libc6-dbg:amd64
libcaca0:amd64
libcairo-gobject-perl:amd64
libcairo-gobject2:amd64
libcairo-perl:amd64
libcairo-script-interpreter2:amd64
libcairo2:amd64
libcairomm-1.0-1v5:amd64
libcamel-1.2-63:amd64
libcanberra-gtk3-0:amd64
libcanberra-gtk3-module:amd64
libcanberra-pulse:amd64
libcanberra0:amd64
libcap-ng0:amd64
libcap2:amd64
libcap2-bin
libcbor0.8:amd64
libcdio-cdda2:amd64
libcdio-paranoia2:amd64
libcdio19:amd64
libcdparanoia0:amd64
libcheese-gtk25:amd64
libcheese8:amd64
libclone-perl
libclutter-1.0-0:amd64
libclutter-1.0-common
libclutter-gst-3.0-0:amd64
libclutter-gtk-1.0-0:amd64
libcogl-common
libcogl-pango20:amd64
libcogl-path20:amd64
libcogl20:amd64
libcolord-gtk1:amd64
libcolord2:amd64
libcolorhug2:amd64
libcom-err2:amd64
libcrack2:amd64
libcrypt1:amd64
libcryptsetup12:amd64
libctf-nobfd0:amd64
libctf0:amd64
libcue2:amd64
libcups2:amd64
libcupsfilters1:amd64
libcupsimage2:amd64
libcurl3-gnutls:amd64
libcurl4:amd64
libdaemon0:amd64
libdata-dump-perl
libdatrie1:amd64
libdb5.3:amd64
libdbus-1-3:amd64
libdbus-glib-1-2:amd64
libdbusmenu-glib4:amd64
libdbusmenu-gtk3-4:amd64
libdconf1:amd64
libdebconfclient0:amd64
libdebuginfod-common
libdebuginfod1:amd64
libdee-1.0-4:amd64
libdeflate0:amd64
libdevmapper1.02.1:amd64
libdjvulibre-text
libdjvulibre21:amd64
libdns-export1110
libdotconf0:amd64
libdrm-amdgpu1:amd64
libdrm-common
libdrm-intel1:amd64
libdrm-nouveau2:amd64
libdrm-radeon1:amd64
libdrm2:amd64
libdv4:amd64
libdw1:amd64
libebackend-1.2-10:amd64
libebook-1.2-20:amd64
libebook-contacts-1.2-3:amd64
libecal-2.0-1:amd64
libedata-book-1.2-26:amd64
libedata-cal-2.0-1:amd64
libedataserver-1.2-26:amd64
libedataserverui-1.2-3:amd64
libedit2:amd64
libefiboot1:amd64
libefivar1:amd64
libegl-mesa0:amd64
libegl1:amd64
libelf1:amd64
libenchant-2-2:amd64
libencode-locale-perl
libepoxy0:amd64
libespeak-ng1:amd64
libestr0:amd64
libevdev2:amd64
libevdocument3-4:amd64
libevview3-3:amd64
libexempi8:amd64
libexif12:amd64
libexiv2-27:amd64
libexpat1:amd64
libext2fs2:amd64
libextutils-depends-perl
libfastjson4:amd64
libfdisk1:amd64
libffi8:amd64
libfftw3-single3:amd64
libfido2-1:amd64
libfile-basedir-perl
libfile-desktopentry-perl
libfile-listing-perl
libfile-mimeinfo-perl
libflac8:amd64
libflashrom1:amd64
libfont-afm-perl
libfontconfig1:amd64
libfontembed1:amd64
libfontenc1:amd64
libfprint-2-2:amd64
libfreerdp-client2-2:amd64
libfreerdp-server2-2:amd64
libfreerdp2-2:amd64
libfreetype6:amd64
libfribidi0:amd64
libftdi1-2:amd64
libfuse3-3:amd64
libfwupd2:amd64
libfwupdplugin5:amd64
libgail-common:amd64
libgail18:amd64
libgamemode0:amd64
libgamemodeauto0:amd64
libgbm1:amd64
libgcab-1.0-0:amd64
libgcc-s1:amd64
libgck-1-0:amd64
libgcr-base-3-1:amd64
libgcr-ui-3-1:amd64
libgcrypt20:amd64
libgd3:amd64
libgdata-common
libgdata22:amd64
libgdbm-compat4:amd64
libgdbm6:amd64
libgdk-pixbuf-2.0-0:amd64
libgdk-pixbuf2.0-bin
libgdk-pixbuf2.0-common
libgdm1
libgee-0.8-2:amd64
libgeoclue-2-0:amd64
libgeocode-glib0:amd64
libgexiv2-2:amd64
libgif7:amd64
libgirepository-1.0-1:amd64
libgjs0g:amd64
libgl1:amd64
libgl1-amber-dri:amd64
libgl1-mesa-dri:amd64
libglapi-mesa:amd64
libgles2:amd64
libglib-object-introspection-perl
libglib-perl:amd64
libglib2.0-0:amd64
libglib2.0-bin
libglib2.0-data
libglibmm-2.4-1v5:amd64
libglu1-mesa:amd64
libglvnd0:amd64
libglx-mesa0:amd64
libglx0:amd64
libgmp10:amd64
libgnome-autoar-0-0:amd64
libgnome-bg-4-1:amd64
libgnome-bluetooth-3.0-13:amd64
libgnome-bluetooth13:amd64
libgnome-desktop-3-19:amd64
libgnome-desktop-4-1:amd64
libgnome-menu-3-0:amd64
libgnomekbd-common
libgnomekbd8:amd64
libgnutls30:amd64
libgoa-1.0-0b:amd64
libgoa-1.0-common
libgoa-backend-1.0-1:amd64
libgomp1:amd64
libgpg-error0:amd64
libgpgme11:amd64
libgphoto2-6:amd64
libgphoto2-l10n
libgphoto2-port12:amd64
libgpm2:amd64
libgraphene-1.0-0:amd64
libgraphite2-3:amd64
libgs9:amd64
libgs9-common
libgsf-1-114:amd64
libgsf-1-common
libgsound0:amd64
libgspell-1-2:amd64
libgspell-1-common
libgssapi-krb5-2:amd64
libgssdp-1.2-0:amd64
libgstreamer-gl1.0-0:amd64
libgstreamer-plugins-base1.0-0:amd64
libgstreamer-plugins-good1.0-0:amd64
libgstreamer1.0-0:amd64
libgtk-3-0:amd64
libgtk-3-bin
libgtk-3-common
libgtk-4-1:amd64
libgtk-4-bin
libgtk-4-common
libgtk2.0-0:amd64
libgtk2.0-bin
libgtk2.0-common
libgtk3-perl
libgtkmm-3.0-1v5:amd64
libgtksourceview-4-0:amd64
libgtksourceview-4-common
libgtop-2.0-11:amd64
libgtop2-common
libgudev-1.0-0:amd64
libgupnp-1.2-1:amd64
libgupnp-av-1.0-3
libgupnp-dlna-2.0-4
libgusb2:amd64
libgweather-3-16:amd64
libgweather-common
libgxps2:amd64
libhandy-1-0:amd64
libharfbuzz-icu0:amd64
libharfbuzz0b:amd64
libhogweed6:amd64
libhpmud0:amd64
libhtml-form-perl
libhtml-format-perl
libhtml-parser-perl:amd64
libhtml-tagset-perl
libhtml-tree-perl
libhttp-cookies-perl
libhttp-daemon-perl
libhttp-date-perl
libhttp-message-perl
libhttp-negotiate-perl
libhunspell-1.7-0:amd64
libhyphen0:amd64
libibus-1.0-5:amd64
libical3:amd64
libice6:amd64
libicu70:amd64
libidn12:amd64
libidn2-0:amd64
libiec61883-0:amd64
libieee1284-3:amd64
libijs-0.35:amd64
libimagequant0:amd64
libimobiledevice6:amd64
libinih1:amd64
libinput-bin
libinput10:amd64
libio-html-perl
libio-socket-ssl-perl
libio-stringy-perl
libip4tc2:amd64
libip6tc2:amd64
libipc-system-simple-perl
libipt2
libisc-export1105:amd64
libisl23:amd64
libiw30:amd64
libjack-jackd2-0:amd64
libjansson4:amd64
libjavascriptcoregtk-4.0-18:amd64
libjbig0:amd64
libjbig2dec0:amd64
libjcat1:amd64
libjpeg-turbo8:amd64
libjpeg8:amd64
libjs-jquery
libjson-c5:amd64
libjson-glib-1.0-0:amd64
libjson-glib-1.0-common
libk5crypto3:amd64
libkeyutils1:amd64
libklibc:amd64
libkmod2:amd64
libkpathsea6:amd64
libkrb5-3:amd64
libkrb5support0:amd64
libksba8:amd64
liblcms2-2:amd64
liblcms2-utils
libldap-2.5-0:amd64
libldap-common
libldb2:amd64
libllvm13:amd64
liblmdb0:amd64
liblocale-gettext-perl
liblockfile-bin
liblockfile1:amd64
liblouis-data
liblouis20:amd64
liblouisutdml-bin
liblouisutdml-data
liblouisutdml9:amd64
libltdl7:amd64
liblwp-mediatypes-perl
liblwp-protocol-https-perl
liblz4-1:amd64
liblzma5:amd64
liblzo2-2:amd64
libmagic-mgc
libmagic1:amd64
libmailtools-perl
libmanette-0.2-0:amd64
libmaxminddb0:amd64
libmbim-glib4:amd64
libmbim-proxy
libmd0:amd64
libmediaart-2.0-0:amd64
libmm-glib0:amd64
libmnl0:amd64
libmount1:amd64
libmozjs-91-0:amd64
libmp3lame0:amd64
libmpc3:amd64
libmpdec3:amd64
libmpfr6:amd64
libmpg123-0:amd64
libmspack0:amd64
libmtdev1:amd64
libmtp-common
libmtp-runtime
libmtp9:amd64
libmutter-10-0:amd64
libnautilus-extension1a:amd64
libncurses6:amd64
libncursesw6:amd64
libndp0:amd64
libnet-dbus-perl
libnet-http-perl
libnet-smtp-ssl-perl
libnet-ssleay-perl:amd64
libnetfilter-conntrack3:amd64
libnetplan0:amd64
libnettle8:amd64
libnewt0.52:amd64
libnfnetlink0:amd64
libnfs13:amd64
libnftables1:amd64
libnftnl11:amd64
libnghttp2-14:amd64
libnl-3-200:amd64
libnl-genl-3-200:amd64
libnl-route-3-200:amd64
libnm0:amd64
libnma-common
libnma0:amd64
libnotify-bin
libnotify4:amd64
libnpth0:amd64
libnsl2:amd64
libnspr4:amd64
libnss-mdns:amd64
libnss-systemd:amd64
libnss3:amd64
libntfs-3g89
libnuma1:amd64
libogg0:amd64
libopengl0:amd64
libopenjp2-7:amd64
libopus0:amd64
liborc-0.4-0:amd64
libp11-kit0:amd64
libpackagekit-glib2-18:amd64
libpam-cap:amd64
libpam-fprintd:amd64
libpam-gnome-keyring:amd64
libpam-modules:amd64
libpam-modules-bin
libpam-pwquality:amd64
libpam-runtime
libpam-sss:amd64
libpam-systemd:amd64
libpam0g:amd64
libpango-1.0-0:amd64
libpangocairo-1.0-0:amd64
libpangoft2-1.0-0:amd64
libpangomm-1.4-1v5:amd64
libpangoxft-1.0-0:amd64
libpaper-utils
libpaper1:amd64
libparted-fs-resize0:amd64
libparted2:amd64
libpcap0.8:amd64
libpcaudio0:amd64
libpci3:amd64
libpciaccess0:amd64
libpcre2-32-0:amd64
libpcre2-8-0:amd64
libpcre3:amd64
libpcsclite1:amd64
libpeas-1.0-0:amd64
libpeas-common
libperl5.34:amd64
libphonenumber8:amd64
libpipeline1:amd64
libpipewire-0.3-0:amd64
libpipewire-0.3-common
libpipewire-0.3-modules:amd64
libpixman-1-0:amd64
libpkcs11-helper1:amd64
libplist3:amd64
libplymouth5:amd64
libpng16-16:amd64
libpolkit-agent-1-0:amd64
libpolkit-gobject-1-0:amd64
libpoppler-cpp0v5:amd64
libpoppler-glib8:amd64
libpoppler118:amd64
libpopt0:amd64
libprocps8:amd64
libprotobuf23:amd64
libproxy1-plugin-gsettings:amd64
libproxy1-plugin-networkmanager:amd64
libproxy1v5:amd64
libpsl5:amd64
libpulse-mainloop-glib0:amd64
libpulse0:amd64
libpulsedsp:amd64
libpwquality-common
libpwquality1:amd64
libpython3-stdlib:amd64
libpython3.10:amd64
libpython3.10-minimal:amd64
libpython3.10-stdlib:amd64
libqmi-glib5:amd64
libqmi-proxy
libqpdf28:amd64
libraqm0:amd64
libraw1394-11:amd64
libreadline8:amd64
librest-0.7-0:amd64
librsvg2-2:amd64
librsvg2-common:amd64
librtmp1:amd64
libruby3.0:amd64
librygel-core-2.6-2:amd64
librygel-db-2.6-2:amd64
librygel-renderer-2.6-2:amd64
librygel-server-2.6-2:amd64
libsamplerate0:amd64
libsane-common
libsane-hpaio:amd64
libsane1:amd64
libsasl2-2:amd64
libsasl2-modules:amd64
libsasl2-modules-db:amd64
libsasl2-modules-gssapi-mit:amd64
libsbc1:amd64
libseccomp2:amd64
libsecret-1-0:amd64
libsecret-common
libselinux1:amd64
libsemanage-common
libsemanage2:amd64
libsensors-config
libsensors5:amd64
libsepol2:amd64
libshout3:amd64
libsigc++-2.0-0v5:amd64
libslang2:amd64
libsm6:amd64
libsmartcols1:amd64
libsmbclient:amd64
libsmbios-c2
libsnapd-glib1:amd64
libsndfile1:amd64
libsnmp-base
libsnmp40:amd64
libsodium23:amd64
libsonic0:amd64
libsoup-gnome2.4-1:amd64
libsoup2.4-1:amd64
libsoup2.4-common
libsource-highlight-common
libsource-highlight4v5
libsoxr0:amd64
libspa-0.2-modules:amd64
libspectre1:amd64
libspeechd2:amd64
libspeex1:amd64
libspeexdsp1:amd64
libsqlite3-0:amd64
libss2:amd64
libssh-4:amd64
libssl3:amd64
libstartup-notification0:amd64
libstdc++6:amd64
libstemmer0d:amd64
libsynctex2:amd64
libsysmetrics1:amd64
libsystemd0:amd64
libtag1v5:amd64
libtag1v5-vanilla:amd64
libtalloc2:amd64
libtasn1-6:amd64
libtcl8.6:amd64
libtdb1:amd64
libteamdctl0:amd64
libtevent0:amd64
libtext-charwidth-perl
libtext-iconv-perl
libtext-wrapi18n-perl
libthai-data
libthai0:amd64
libtheora0:amd64
libtie-ixhash-perl
libtiff5:amd64
libtimedate-perl
libtinfo6:amd64
libtirpc-common
libtirpc3:amd64
libtotem-plparser-common
libtotem-plparser18:amd64
libtracker-sparql-3.0-0:amd64
libtry-tiny-perl
libtss2-esys-3.0.2-0:amd64
libtss2-mu0:amd64
libtss2-sys1:amd64
libtss2-tcti-cmd0:amd64
libtss2-tcti-device0:amd64
libtss2-tcti-mssim0:amd64
libtss2-tcti-swtpm0:amd64
libtwolame0:amd64
libu2f-udev
libuchardet0:amd64
libudev1:amd64
libudisks2-0:amd64
libunistring2:amd64
libunity-protocol-private0:amd64
libunity-scopes-json-def-desktop
libunity9:amd64
libunwind8:amd64
libupower-glib3:amd64
liburi-perl
liburing2:amd64
libusb-1.0-0:amd64
libusbmuxd6:amd64
libuuid1:amd64
libuv1:amd64
libv4l-0:amd64
libv4lconvert0:amd64
libvisual-0.4-0:amd64
libvncserver1:amd64
libvolume-key1
libvorbis0a:amd64
libvorbisenc2:amd64
libvorbisfile3:amd64
libvpx7:amd64
libvte-2.91-0:amd64
libvte-2.91-common
libvulkan1:amd64
libwacom-bin
libwacom-common
libwacom9:amd64
libwavpack1:amd64
libwayland-client0:amd64
libwayland-cursor0:amd64
libwayland-egl1:amd64
libwayland-server0:amd64
libwbclient0:amd64
libwebkit2gtk-4.0-37:amd64
libwebp7:amd64
libwebpdemux2:amd64
libwebpmux3:amd64
libwebrtc-audio-processing1:amd64
libwhoopsie-preferences0
libwhoopsie0:amd64
libwinpr2-2:amd64
libwmf-0.2-7:amd64
libwmf-0.2-7-gtk
libwmf0.2-7-gtk:amd64
libwmflite-0.2-7:amd64
libwnck-3-0:amd64
libwnck-3-common
libwoff1:amd64
libwrap0:amd64
libwww-perl
libwww-robotrules-perl
libx11-6:amd64
libx11-data
libx11-protocol-perl
libx11-xcb1:amd64
libxatracker2:amd64
libxau6:amd64
libxaw7:amd64
libxcb-dri2-0:amd64
libxcb-dri3-0:amd64
libxcb-glx0:amd64
libxcb-icccm4:amd64
libxcb-image0:amd64
libxcb-keysyms1:amd64
libxcb-present0:amd64
libxcb-randr0:amd64
libxcb-render-util0:amd64
libxcb-render0:amd64
libxcb-res0:amd64
libxcb-shape0:amd64
libxcb-shm0:amd64
libxcb-sync1:amd64
libxcb-util1:amd64
libxcb-xfixes0:amd64
libxcb-xkb1:amd64
libxcb-xv0:amd64
libxcb1:amd64
libxcomposite1:amd64
libxcursor1:amd64
libxcvt0:amd64
libxdamage1:amd64
libxdmcp6:amd64
libxext6:amd64
libxfixes3:amd64
libxfont2:amd64
libxft2:amd64
libxi6:amd64
libxinerama1:amd64
libxkbcommon-x11-0:amd64
libxkbcommon0:amd64
libxkbfile1:amd64
libxkbregistry0:amd64
libxklavier16:amd64
libxml-parser-perl:amd64
libxml-twig-perl
libxml-xpathengine-perl
libxml2:amd64
libxmlb2:amd64
libxmlsec1:amd64
libxmlsec1-openssl:amd64
libxmu6:amd64
libxmuu1:amd64
libxpm4:amd64
libxrandr2:amd64
libxrender1:amd64
libxres1:amd64
libxshmfence1:amd64
libxslt1.1:amd64
libxss1:amd64
libxt6:amd64
libxtables12:amd64
libxtst6:amd64
libxv1:amd64
libxvmc1:amd64
libxxf86dga1:amd64
libxxf86vm1:amd64
libxxhash0:amd64
libyaml-0-2:amd64
libyelp0:amd64
libzstd1:amd64
linux-base
linux-firmware
linux-generic-hwe-22.04
linux-headers-5.15.0-43
linux-headers-5.15.0-43-generic
linux-headers-5.15.0-56
linux-headers-5.15.0-56-generic
linux-headers-generic-hwe-22.04
linux-image-5.15.0-43-generic
linux-image-5.15.0-56-generic
linux-image-generic-hwe-22.04
linux-modules-5.15.0-43-generic
linux-modules-5.15.0-56-generic
linux-modules-extra-5.15.0-43-generic
linux-modules-extra-5.15.0-56-generic
linux-sound-base
locales
login
logrotate
logsave
lsb-base
lsb-release
lshw
lsof
mailcap
man-db
manpages
mawk
media-types
memtest86+
mesa-vulkan-drivers:amd64
mime-support
mlocate
mobile-broadband-provider-info
modemmanager
mokutil
mount
mousetweaks
mscompress
mtr-tiny
mutter-common
nano
nautilus
nautilus-data
nautilus-extension-gnome-terminal
nautilus-sendto
nautilus-share
ncurses-base
ncurses-bin
net-tools
netbase
netcat-openbsd
netplan.io
network-manager
network-manager-config-connectivity-ubuntu
network-manager-gnome
network-manager-openvpn
network-manager-openvpn-gnome
network-manager-pptp
network-manager-pptp-gnome
networkd-dispatcher
nftables
ntfs-3g
open-vm-tools
open-vm-tools-desktop
openprinting-ppds
openssh-client
openssl
openvpn
orca
os-prober
p11-kit
p11-kit-modules:amd64
packagekit
packagekit-tools
parted
passwd
patch
pci.ids
pciutils
pcmciautils
perl
perl-base
perl-modules-5.34
perl-openssl-defaults:amd64
pinentry-curses
pinentry-gnome3
pipewire:amd64
pipewire-bin
pipewire-media-session
pkexec
plocate
plymouth
plymouth-label
plymouth-theme-spinner
plymouth-theme-ubuntu-text
policycoreutils
policykit-1
policykit-desktop-privileges
polkitd
poppler-data
poppler-utils
postfix
power-profiles-daemon
powermgmt-base
ppp
pptp-linux
printer-driver-brlaser
printer-driver-c2esp
printer-driver-foo2zjs
printer-driver-foo2zjs-common
printer-driver-hpcups
printer-driver-m2300w
printer-driver-min12xxw
printer-driver-pnm2ppa
printer-driver-postscript-hp
printer-driver-ptouch
printer-driver-pxljr
printer-driver-sag-gdi
printer-driver-splix
procps
psmisc
publicsuffix
pulseaudio
pulseaudio-module-bluetooth
pulseaudio-utils
pv
python-apt-common
python3
python3-apport
python3-apt
python3-aptdaemon
python3-aptdaemon.gtk3widgets
python3-blinker
python3-brlapi:amd64
python3-cairo:amd64
python3-certifi
python3-cffi-backend:amd64
python3-chardet
python3-click
python3-colorama
python3-commandnotfound
python3-cryptography
python3-cups:amd64
python3-cupshelpers
python3-dateutil
python3-dbus
python3-debconf
python3-debian
python3-defer
python3-distro
python3-distro-info
python3-distupgrade
python3-gdbm:amd64
python3-gi
python3-gi-cairo
python3-httplib2
python3-ibus-1.0
python3-idna
python3-importlib-metadata
python3-jeepney
python3-jwt
python3-keyring
python3-launchpadlib
python3-lazr.restfulclient
python3-lazr.uri
python3-ldb
python3-louis
python3-macaroonbakery
python3-minimal
python3-more-itertools
python3-nacl
python3-netifaces:amd64
python3-oauthlib
python3-olefile
python3-pexpect
python3-pil:amd64
python3-pkg-resources
python3-problem-report
python3-protobuf
python3-ptyprocess
python3-pyatspi
python3-pymacaroons
python3-pyparsing
python3-renderpm:amd64
python3-reportlab
python3-reportlab-accel:amd64
python3-requests
python3-rfc3339
python3-secretstorage
python3-six
python3-software-properties
python3-speechd
python3-systemd
python3-talloc:amd64
python3-tz
python3-update-manager
python3-urllib3
python3-wadllib
python3-xdg
python3-xkit
python3-yaml
python3-zipp
python3.10
python3.10-minimal
rake
readline-common
rfkill
rkhunter
rsync
rsyslog
rtkit
ruby
ruby-net-telnet
ruby-rubygems
ruby-webrick
ruby-xmlrpc
ruby3.0
rubygems-integration
rygel
samba-libs:amd64
sane-airscan
sane-utils
sbsigntool
seahorse
secureboot-db
sed
selinux-utils
sensible-utils
session-migration
sgml-base
sgml-data
shared-mime-info
shim-signed
snapd
software-properties-common
software-properties-gtk
sound-icons
sound-theme-freedesktop
speech-dispatcher
speech-dispatcher-audio-plugins:amd64
speech-dispatcher-espeak-ng
spice-vdagent
squashfs-tools
ssl-cert
strace
sudo
switcheroo-control
system-config-printer
system-config-printer-common
system-config-printer-udev
systemd
systemd-hwe-hwdb
systemd-oomd
systemd-sysv
systemd-timesyncd
sysvinit-utils
tar
tcl
tcl8.6
tcpdump
telnet
thermald
tiger
time
tnftp
tpm-udev
tracker
tracker-extract
tracker-miner-fs
tripwire
tzdata
ubuntu-advantage-desktop-daemon
ubuntu-advantage-tools
ubuntu-desktop
ubuntu-desktop-minimal
ubuntu-docs
ubuntu-drivers-common
ubuntu-keyring
ubuntu-minimal
ubuntu-mono
ubuntu-release-upgrader-core
ubuntu-release-upgrader-gtk
ubuntu-report
ubuntu-session
ubuntu-settings
ubuntu-standard
ubuntu-wallpapers
ubuntu-wallpapers-jammy
ucf
udev
udisks2
ufw
unattended-upgrades
unhide
unhide.rb
unzip
update-inetd
update-manager
update-manager-core
update-notifier
update-notifier-common
upower
usb-modeswitch
usb-modeswitch-data
usb.ids
usbmuxd
usbutils
usrmerge
util-linux
uuid-runtime
vim-common
vim-tiny
wamerican
wbritish
wget
whiptail
whoopsie
whoopsie-preferences
wireless-regdb
wireless-tools
wpasupplicant
x11-apps
x11-common
x11-session-utils
x11-utils
x11-xkb-utils
x11-xserver-utils
xauth
xbitmaps
xbrlapi
xclip
xcursor-themes
xcvt
xdg-dbus-proxy
xdg-desktop-portal
xdg-desktop-portal-gnome
xdg-desktop-portal-gtk
xdg-user-dirs
xdg-user-dirs-gtk
xdg-utils
xfonts-base
xfonts-encodings
xfonts-scalable
xfonts-utils
xinit
xinput
xkb-data
xml-core
xorg
xorg-docs-core
xserver-common
xserver-xephyr
xserver-xorg
xserver-xorg-core
xserver-xorg-input-all
xserver-xorg-input-libinput
xserver-xorg-input-wacom
xserver-xorg-legacy
xserver-xorg-video-all
xserver-xorg-video-amdgpu
xserver-xorg-video-ati
xserver-xorg-video-fbdev
xserver-xorg-video-intel
xserver-xorg-video-nouveau
xserver-xorg-video-qxl
xserver-xorg-video-radeon
xserver-xorg-video-vesa
xserver-xorg-video-vmware
xwayland
xxd
xz-utils
yaru-theme-gnome-shell
yaru-theme-gtk
yaru-theme-icon
yaru-theme-sound
yelp
yelp-xsl
zenity
zenity-common
zerofree
zip
zlib1g:amd64
zstd"""
current_packs = os.popen("dpkg --get-selections | awk '{print $1}'").read()

default_list = default_packs.split("\n")
current_list = current_packs.split("\n")

if current_list[-1] == '':
	current_list = current_list[:-1]


print(Fore.RED + Back.WHITE + Style.BRIGHT +"LISTING NON-DEFAULT PACKAGES")
print("\n\n")
for pack in current_list:
	if pack not in default_list:
		print(pack)

print("\n\n\n\n")
os.system("ufw enable 1>/dev/null")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"UFW enabled")


print("\n\n")

os.system("apt install auditd audispd-plugins -y 0>/dev/null 1>/dev/null 2>/dev/null")
os.system("sed -i \'s/\\bGRUB_CMDLINE_LINUX=\"\\b/&audit=1 /\' /etc/default/grub")
os.system("sed -i \'s/\\bGRUB_CMDLINE_LINUX=\"\\b/&audit_backlog_limit=8192 /\' /etc/default/grub")
os.system("update-grub 2>/dev/null")

with open("/etc/audit/rules.d/auditd.conf","w") as file:
	file.write("""
#
# This file controls the configuration of the audit daemon
#
local_events = yes
write_logs = yes
log_file = /var/log/audit/audit.log
log_group = adm
log_format = RAW
flush = INCREMENTAL_ASYNC
freq = 50
max_log_file = 8
num_logs = 5
priority_boost = 4
disp_qos = lossy
dispatcher = /sbin/audispd
name_format = NONE
##name = mydomain
max_log_file_action = keep_logs
space_left = 75
space_left_action = email
verify_email = yes
action_mail_acct = root
admin_space_left = 50
admin_space_left_action = halt
disk_full_action = SUSPEND
disk_error_action = SUSPEND
use_libwrap = yes
##tcp_listen_port = 60
tcp_listen_queue = 5
tcp_max_per_addr = 1
##tcp_client_ports = 1024-65535
tcp_client_max_idle = 0
enable_krb5 = no
krb5_principal = auditd
##krb5_key_file = /etc/audit/audit.key
distribute_network = no
""")


with open("/etc/audit/rules.d/50-access.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access 
-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access 
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access 
-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access 
""")

with open("/etc/audit/rules.d/50-delete.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
""")
with open("/etc/audit/rules.d/50-logins.rules","w") as file:
	file.write("""
-w /var/log/faillog -p wa -k logins
-w /var/log/lastlog -p wa -k logins
-w /var/log/tallylog -p wa -k logins
""")
with open("/etc/audit/rules.d/50-modules.rules","w") as file:
	file.write("""
-w /sbin/insmod -p x -k modules
-w /sbin/rmmod -p x -k modules
-w /sbin/modprobe -p x -k modules
-a always,exit -F arch=b64 -S init_module -S delete_module -k modules
""")
with open("/etc/audit/rules.d/50-perm_mod.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -Slremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -Slremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
""")
with open("/etc/audit/rules.d/50-session.rules","w") as file:
	file.write("""
-w /var/run/utmp -p wa -k session
-w /var/log/wtmp -p wa -k logins
-w /var/log/btmp -p wa -k logins
""")
with open("/etc/audit/rules.d/50-time-change.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change
-a always,exit -F arch=b64 -S clock_settime -k time-change
-a always,exit -F arch=b32 -S clock_settime -k time-change
-w /etc/localtime -p wa -k time-change
""")
with open("/etc/audit/rules.d/50-actions.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -C euid!=uid -F euid=0 -Fauid>=1000 -F auid!=4294967295 -S execve -k actions
-a always,exit -F arch=b32 -C euid!=uid -F euid=0 -Fauid>=1000 -F auid!=4294967295 -S execve -k actions
""")
with open("/etc/audit/rules.d/50-identity.rules","w") as file:
	file.write("""
-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/security/opasswd -p wa -k identity
""")
with open("/etc/audit/rules.d/50-MAC-policy.rules","w") as file:
	file.write("""
-w /etc/apparmor/ -p wa -k MAC-policy
-w /etc/apparmor.d/ -p wa -k MAC-policy
""")
with open("/etc/audit/rules.d/50-mounts.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts
-a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts
""")
with open("/etc/audit/rules.d/50-privileged.rules","w") as file:
	file.write("""
-a always,exit -F path=/usr/lib/snapd/snap-confine -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/lib/openssh/ssh-keysign -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/lib/dbus-1.0/dbus-daemon-launch-helper -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/lib/eject/dmcrypt-get-device -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/lib/policykit-1/polkit-agent-helper-1 -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/lib/xorg/Xorg.wrap -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/passwd -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/su -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/expiry -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/chsh -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/ssh-agent -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/fusermount -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/gpasswd -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/newgrp -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/sudo -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/mount -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/wall -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/vmware-user-suid-wrapper -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/crontab -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/umount -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/bsd-write -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/chage -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/pkexec -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/bin/chfn -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/sbin/unix_chkpwd -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/sbin/pppd -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/sbin/pam_extrausers_chkpwd -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
-a always,exit -F path=/usr/libexec/camel-lock-helper-1.2 -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged
""")
with open("/etc/audit/rules.d/50-system-locale.rules","w") as file:
	file.write("""
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale
-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale
-w /etc/issue -p wa -k system-locale
-w /etc/issue.net -p wa -k system-locale
-w /etc/hosts -p wa -k system-locale
-w /etc/network -p wa -k system-locale
""")
with open("/etc/audit/rules.d/99-finalize.rules","w") as file:
	file.write("""
-e 2
""")

os.system("systemctl restart auditd")

print(Fore.RED + Back.WHITE + Style.BRIGHT +"auditd configured")

print("\n\n")
sysctl = """kernel.randomize_va_space = 2
fs.suid_dumpable = 0
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.ip_forward=0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.tcp_syncookies = 1
kernel.perf_event_paranoid = 2
kernel.sysrq=0
kernel.unprivileged_userns_clone=0
kernel.dmesg_restrict = 1
"""

with open("/etc/sysctl.conf","w") as file:
	file.write(sysctl)
os.system("sysctl --system 1>/dev/null 2>/dev/null")

sshd = """AllowUsers CHANGE_TO_AUTHORIZED_USERS
LogLevel INFO
X11Forwarding no
MaxAuthTries 4
IgnoreRhosts yes
HostbasedAuthentication no
PermitRootLogin no
PermitEmptyPasswords no
PermitUserEnvironment no
Ciphers aes128-ctr,aes192-ctr,aes256-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256
ClientAliveInterval 300
ClientAliveCountMax 3
LoginGraceTime 60
Banner /etc/issue.net
UsePAM yes
AllowTcpForwarding no
MaxStartups 10:30:60
MaxSessions 10
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
SyslogFacility AUTH
ChallengeResponseAuthentication no
### Unless CyberPatriot asks for passwordless authentication, this is set to no
PubkeyAuthentication no
# Port Number
Port 22
AllowAgentForwarding no
"""

with open("/etc/ssh/sshd_config","w") as file:
	file.write(sshd)

print(Fore.RED + Back.WHITE + Style.BRIGHT +"sshd configured")
print("\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"sysctl configured")

print("\n\n")
os.system("apt purge firefox -y 1>/dev/null 2>/dev/null")
os.system("apt install firefox -y 1>/dev/null 2>/dev/null")

print(Fore.RED + Back.WHITE + Style.BRIGHT +"firefox updated")
print("\n\n")

with open("/etc/modprobe.d/cramfs.conf","w") as file:
	file.write("install cramfs /bin/true")
with open("/etc/modprobe.d/freevxfs.conf","w") as file:
	file.write("install freevxfs /bin/true")
with open("/etc/modprobe.d/hfs.conf","w") as file:
	file.write("install hfs /bin/true")
with open("/etc/modprobe.d/hfsplus.conf","w") as file:
	file.write("install hfsplus /bin/true")
with open("/etc/modprobe.d/jffs2.conf","w") as file:
	file.write("install jffs2 /bin/true")
with open("/etc/modprobe.d/squashfs.conf","w") as file:
	file.write("install squashfs /bin/true")
with open("/etc/modprobe.d/udf.conf","w") as file:
	file.write("install udf /bin/true")
with open("/etc/modprobe.d/usb_storage.conf","w") as file:
	file.write("install usb-storage /bin/true")
os.system("rmmod cramfs 1>/dev/null 2>/dev/null")
os.system("rmmod freevxfs 1>/dev/null 2>/dev/null")
os.system("rmmod jffs2 1>/dev/null 2>/dev/null")
os.system("rmmod hfs 1>/dev/null 2>/dev/null")
os.system("rmmod hfsplus 1>/dev/null 2>/dev/null")
os.system("rmmod squashfs 1>/dev/null 2>/dev/null")
os.system("rmmod udf 1>/dev/null 2>/dev/null")
os.system("rmmod usb-storage 1>/dev/null 2>/dev/null")

os.system("echo '\ntmpfs /tmp tmpfs defaults,rw,nosuid,nodev,noexec,relatime 0 0\ntmpfs /dev/shm tmpfs defaults,noexec,nodev,nosuid,seclabel 0 0' >> /etc/fstab")
os.system("mount -a 1>/dev/null 2>/dev/null")

os.system("systemctl --now disable autofs 1>/dev/null 2>/dev/null")
os.system("apt purge autofs -y 1>/dev/null 2>/dev/null")

print(Fore.RED + Back.WHITE + Style.BRIGHT +"filesystems modified")
print("\n\n\n")

print(Fore.RED + Back.WHITE + Style.BRIGHT +"files with SUID or SGID bits")

normal = ['/snap/snapd/16292/usr/lib/snapd/snap-confine', '/snap/core18/1988/bin/mount', '/snap/core18/1988/bin/ping', '/snap/core18/1988/bin/su', '/snap/core18/1988/bin/umount', '/snap/core18/1988/usr/bin/chfn', '/snap/core18/1988/usr/bin/chsh', '/snap/core18/1988/usr/bin/gpasswd', '/snap/core18/1988/usr/bin/newgrp', '/snap/core18/1988/usr/bin/passwd', '/snap/core18/1988/usr/bin/sudo', '/snap/core18/1988/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core18/1988/usr/lib/openssh/ssh-keysign', '/snap/core18/2538/bin/mount', '/snap/core18/2538/bin/ping', '/snap/core18/2538/bin/su', '/snap/core18/2538/bin/umount', '/snap/core18/2538/usr/bin/chfn', '/snap/core18/2538/usr/bin/chsh', '/snap/core18/2538/usr/bin/gpasswd', '/snap/core18/2538/usr/bin/newgrp', '/snap/core18/2538/usr/bin/passwd', '/snap/core18/2538/usr/bin/sudo', '/snap/core18/2538/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core18/2538/usr/lib/openssh/ssh-keysign', '/snap/core20/1587/usr/bin/chfn', '/snap/core20/1587/usr/bin/chsh', '/snap/core20/1587/usr/bin/gpasswd', '/snap/core20/1587/usr/bin/mount', '/snap/core20/1587/usr/bin/newgrp', '/snap/core20/1587/usr/bin/passwd', '/snap/core20/1587/usr/bin/su', '/snap/core20/1587/usr/bin/sudo', '/snap/core20/1587/usr/bin/umount', '/snap/core20/1587/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core20/1587/usr/lib/openssh/ssh-keysign', '/usr/lib/snapd/snap-confine', '/usr/lib/openssh/ssh-keysign', '/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/usr/lib/eject/dmcrypt-get-device', '/usr/lib/policykit-1/polkit-agent-helper-1', '/usr/lib/xorg/Xorg.wrap', '/usr/bin/passwd', '/usr/bin/su', '/usr/bin/chsh', '/usr/bin/fusermount', '/usr/bin/gpasswd', '/usr/bin/newgrp', '/usr/bin/sudo', '/usr/bin/mount', '/usr/bin/vmware-user-suid-wrapper', '/usr/bin/umount', '/usr/bin/pkexec', '/usr/bin/chfn', '/usr/sbin/pppd','/usr/lib/openssh/ssh-keysign', '/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/usr/lib/eject/dmcrypt-get-device', '/usr/lib/policykit-1/polkit-agent-helper-1', '/usr/lib/xorg/Xorg.wrap', '/usr/bin/passwd', '/usr/bin/su', '/usr/bin/chsh', '/usr/bin/fusermount', '/usr/bin/gpasswd', '/usr/bin/newgrp', '/usr/bin/sudo', '/usr/bin/mount', '/usr/bin/vmware-user-suid-wrapper', '/usr/bin/umount', '/usr/bin/pkexec', '/usr/bin/chfn', '/usr/sbin/pppd', 'root@ubuntu:/home/student/script# find / -perm /4000 2>/dev/null', '/snap/snapd/15904/usr/lib/snapd/snap-confine', '/snap/snapd/16292/usr/lib/snapd/snap-confine', '/snap/core18/2409/bin/mount', '/snap/core18/2409/bin/ping', '/snap/core18/2409/bin/su', '/snap/core18/2409/bin/umount', '/snap/core18/2409/usr/bin/chfn', '/snap/core18/2409/usr/bin/chsh', '/snap/core18/2409/usr/bin/gpasswd', '/snap/core18/2409/usr/bin/newgrp', '/snap/core18/2409/usr/bin/passwd', '/snap/core18/2409/usr/bin/sudo', '/snap/core18/2409/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core18/2409/usr/lib/openssh/ssh-keysign', '/snap/core18/2538/bin/mount', '/snap/core18/2538/bin/ping', '/snap/core18/2538/bin/su', '/snap/core18/2538/bin/umount', '/snap/core18/2538/usr/bin/chfn', '/snap/core18/2538/usr/bin/chsh', '/snap/core18/2538/usr/bin/gpasswd', '/snap/core18/2538/usr/bin/newgrp', '/snap/core18/2538/usr/bin/passwd', '/snap/core18/2538/usr/bin/sudo', '/snap/core18/2538/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core18/2538/usr/lib/openssh/ssh-keysign', '/snap/core20/1587/usr/bin/chfn', '/snap/core20/1587/usr/bin/chsh', '/snap/core20/1587/usr/bin/gpasswd', '/snap/core20/1587/usr/bin/mount', '/snap/core20/1587/usr/bin/newgrp', '/snap/core20/1587/usr/bin/passwd', '/snap/core20/1587/usr/bin/su', '/snap/core20/1587/usr/bin/sudo', '/snap/core20/1587/usr/bin/umount', '/snap/core20/1587/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core20/1587/usr/lib/openssh/ssh-keysign', '/snap/core20/1494/usr/bin/chfn', '/snap/core20/1494/usr/bin/chsh', '/snap/core20/1494/usr/bin/gpasswd', '/snap/core20/1494/usr/bin/mount', '/snap/core20/1494/usr/bin/newgrp', '/snap/core20/1494/usr/bin/passwd', '/snap/core20/1494/usr/bin/su', '/snap/core20/1494/usr/bin/sudo', '/snap/core20/1494/usr/bin/umount', '/snap/core20/1494/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/snap/core20/1494/usr/lib/openssh/ssh-keysign', '/usr/lib/snapd/snap-confine', '/usr/lib/openssh/ssh-keysign', '/usr/lib/dbus-1.0/dbus-daemon-launch-helper', '/usr/lib/eject/dmcrypt-get-device', '/usr/lib/policykit-1/polkit-agent-helper-1', '/usr/lib/xorg/Xorg.wrap', '/usr/bin/passwd', '/usr/bin/su', '/usr/bin/chsh', '/usr/bin/fusermount', '/usr/bin/gpasswd', '/usr/bin/newgrp', '/usr/bin/sudo', '/usr/bin/mount', '/usr/bin/vmware-user-suid-wrapper', '/usr/bin/umount', '/usr/bin/pkexec', '/usr/bin/chfn', '/usr/sbin/pppd']

sbit = os.popen("find / -perm /4000 2>/dev/null | grep -v snap").read()
sbit = sbit.rstrip("\n")
sbit = sbit.split("\n")

print("suid bits")
print("--------------------------------------------------------------------------------------------------------------------")
for i in sbit:
	if i not in normal:
		print(i)

normal_gid = ['/run/log/journal','/var/log/journal/969b0afa964e47f7ae341416a3fe739f', '/etc/ppp/peers', '/etc/chatscripts', '/snap/core18/2409/sbin/pam_extrausers_chkpwd', '/snap/core18/2409/sbin/unix_chkpwd', '/snap/core18/2409/usr/bin/chage', '/snap/core18/2409/usr/bin/expiry', '/snap/core18/2409/usr/bin/ssh-agent', '/snap/core18/2409/usr/bin/wall', '/snap/core18/2409/var/mail', '/snap/core18/2538/sbin/pam_extrausers_chkpwd', '/snap/core18/2538/sbin/unix_chkpwd', '/snap/core18/2538/usr/bin/chage', '/snap/core18/2538/usr/bin/expiry', '/snap/core18/2538/usr/bin/ssh-agent', '/snap/core18/2538/usr/bin/wall', '/snap/core18/2538/var/mail', '/snap/core20/1587/usr/bin/chage', '/snap/core20/1587/usr/bin/expiry', '/snap/core20/1587/usr/bin/ssh-agent', '/snap/core20/1587/usr/bin/wall', '/snap/core20/1587/usr/sbin/pam_extrausers_chkpwd', '/snap/core20/1587/usr/sbin/unix_chkpwd', '/snap/core20/1587/var/mail', '/snap/core20/1611/usr/bin/chage', '/snap/core20/1611/usr/bin/expiry', '/snap/core20/1611/usr/bin/ssh-agent', '/snap/core20/1611/usr/bin/wall', '/snap/core20/1611/usr/sbin/pam_extrausers_chkpwd', '/snap/core20/1611/usr/sbin/unix_chkpwd', '/snap/core20/1611/var/mail', '/usr/local/lib/python3.8', '/usr/local/lib/python3.8/dist-packages', '/usr/local/lib/python3.8/dist-packages/readchar-3.1.0.dist-info', '/usr/local/lib/python3.8/dist-packages/tests', '/usr/local/lib/python3.8/dist-packages/tests/acceptance', '/usr/local/lib/python3.8/dist-packages/tests/acceptance/__pycache__', '/usr/local/lib/python3.8/dist-packages/tests/unit', '/usr/local/lib/python3.8/dist-packages/tests/unit/__pycache__', '/usr/local/lib/python3.8/dist-packages/python_editor-1.0.4.dist-info', '/usr/local/lib/python3.8/dist-packages/blessed-1.19.1.dist-info', '/usr/local/lib/python3.8/dist-packages/blessed', '/usr/local/lib/python3.8/dist-packages/blessed/__pycache__', '/usr/local/lib/python3.8/dist-packages/inquirer-2.10.0.dist-info', '/usr/local/lib/python3.8/dist-packages/wcwidth-0.2.5.dist-info', '/usr/local/lib/python3.8/dist-packages/readchar', '/usr/local/lib/python3.8/dist-packages/readchar/__pycache__', '/usr/local/lib/python3.8/dist-packages/inquirer', '/usr/local/lib/python3.8/dist-packages/inquirer/render', '/usr/local/lib/python3.8/dist-packages/inquirer/render/console', '/usr/local/lib/python3.8/dist-packages/inquirer/render/console/__pycache__', '/usr/local/lib/python3.8/dist-packages/inquirer/render/__pycache__', '/usr/local/lib/python3.8/dist-packages/inquirer/__pycache__', '/usr/local/lib/python3.8/dist-packages/__pycache__', '/usr/local/lib/python3.8/dist-packages/wcwidth', '/usr/local/lib/python3.8/dist-packages/wcwidth/tests', '/usr/local/lib/python3.8/dist-packages/wcwidth/tests/__pycache__', '/usr/local/lib/python3.8/dist-packages/wcwidth/__pycache__', '/usr/local/share/fonts', '/usr/lib/xorg/Xorg.wrap', '/usr/bin/expiry', '/usr/bin/ssh-agent', '/usr/bin/mlocate', '/usr/bin/wall', '/usr/bin/crontab', '/usr/bin/cat', '/usr/bin/bsd-write', '/usr/bin/chage', '/usr/share/ppd/custom', '/usr/sbin/unix_chkpwd', '/usr/sbin/pam_extrausers_chkpwd', '/usr/libexec/camel-lock-helper-1.2', '/var/local', '/var/mail', '/var/crash', '/var/metrics', '/var/log/journal', '/var/log/journal/91a274617804438db83444984b752ff9']

sgid = os.popen("find / -perm /2000 2>/dev/null | grep -v snap").read()
sgid = sgid.rstrip("\n")
sgid = sgid.split("\n")
print("\n\n")
print("sgid bits")
print("--------------------------------------------------------------------------------------------------------------------")
for i in sgid:
	if i not in normal_gid:
		print(i)

os.system("chmod -R a+t /tmp")
print("\n\n\n")

os.system("systemctl start apparmor 1>/dev/null 2>/dev/null")

print(Fore.RED + Back.WHITE + Style.BRIGHT +"Apparmor started")
print("\n\n")

grub_file = f"""#!/bin/sh
exec tail -n +3 $0
# This file provides an easy way to add custom menu entries.  Simply type the
# menu entries you want to add after this comment.  Be careful not to change
# the 'exec tail' line above.
set superusers="{main_user}"
password_pbkdf2 {main_user} grub.pbkdf2.sha512.10000.A21D097643AB5C6C46D1F3DAC51DAD3E19B68A7712EB8F0936F093D58CD53A0FA7E7B081EF2A7E96C27AB3C3C44F92CA552458B3E34E25423AF5F117DC95F390.767AB5C5900393E70279EE9084DDC5BADEB93387119AC59624B01CE219A990AFAB549194147CC8908A401B64431DBC0781BB7073EF2828BD77CA0018901696F0
"""

with open("/etc/grub.d/40_custom","w") as file:
	file.write(grub_file)

os.system("update-grub 1>/dev/null 2>/dev/null")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"grub password set")
print("\n\n")

yes_list = ["y","yes","ya","ye","yas","t","u","i","h","g","j"]



if vsftpd_ask in yes_list:
	with open("/etc/vsftpd.conf","w") as file:
		file.write("""listen=NO
listen_ipv6=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
chroot_local_user=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
rsa_cert_file=/etc/ssl/certs/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.key
ssl_enable=Yes
allow_anon_ssl=YES
force_anon_data_ssl=YES
force_anon_logins_ssl=YES
force_local_data_ssl=YES
force_local_logins_ssl=YES
pasv_enable=Yes
pasv_min_port=10000
pasv_max_port=10100
allow_writeable_chroot=YES
ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO
pasv_promiscuous=NO
write_enable=NO
""")

	os.system("openssl genrsa -out /etc/ssl/private/vsftpd.key 1>/dev/null 2>/dev/null")
	os.system('openssl req -new -key /etc/ssl/private/vsftpd.key -out /etc/ssl/certs/vsftpd.csr -subj "/C=US/ST=Oregon/L=Portland/O=Company Name/OU=Org/CN=www.example.com" 1>/dev/null 2>/dev/null')
	os.system("openssl x509 -req -days 365 -in /etc/ssl/certs/vsftpd.csr -signkey /etc/ssl/private/vsftpd.key -out /etc/ssl/certs/vsftpd.pem 1>/dev/null 2>/dev/null")
	os.system("systemctl restart vsftpd 1>/dev/null 2>/dev/null")
	print(Fore.RED + Back.WHITE + Style.BRIGHT +"Vsftpd secured")
	print("\n\n")


if apache2_ask in yes_list:
	os.system("chown -R root:root /etc/apache2")
	os.system("chown -R www-data:www-data /var/www")
	print(Fore.RED + Back.WHITE + Style.BRIGHT +"Apache root secured")
	print("\n\n")
	#evil php stuff
	"""
	print(Fore.RED + Back.WHITE + Style.BRIGHT +"Evil PHP stuff")
	os.system("grep -R 'phpinfo()' /var/www/html/*;grep -R 'shell_exec(' /var/www/html/*;grep -R 'eval(base64_decode(' /var/www/html/*;grep -R 'exec(' /var/www/html/*;grep -R 'passthru(' /var/www/html/*;grep -R 'eval(' /var/www/html/*;")

	print("\n\n\n")
	"""

print(Fore.RED + Back.WHITE + Style.BRIGHT +"Checking crontabs")
print(Fore.BLUE + Style.BRIGHT +"user crontabs")
os.system('for i in $(ls /var/spool/cron/crontabs/);do echo "---$i---" && cat /var/spool/cron/crontabs/$i | grep -v "#";done')

print("\n")

print(Fore.BLUE + Style.BRIGHT +"non standard cron files in /etc")
default_crons = ['/etc/anacrontab', 'anacron', 'e2scrub_all', 'popularity-contest', '0anacron', 'apache2', 'apport', 'apt-compat', 'bsdmainutils', 'cracklib-runtime', 'dpkg', 'logrotate', 'man-db', 'mlocate', 'popularity-contest', 'update-notifier-common', '0anacron', '/etc/crontab', '0anacron', 'man-db', 'update-notifier-common']

cur_cron = os.popen("for i in $(ls /etc | grep cron);do ls /etc/$i;done | tr -d ' '").read().split("\n")
if cur_cron[-1] == '':
        cur_cron = cur_cron[:-1]


for cron in cur_cron:
	if cron not in default_crons:
		print(cron)
print("\n\n")


print(Fore.RED + Back.WHITE + Style.BRIGHT +"non standard /etc/hosts entries")
print("\n")
os.system('cat /etc/hosts | grep -ve "^127.0.0.1[[:space:]]localhost$\|^127.0.1.1[[:space:]]ubuntu$\|^::1     ip6-localhost ip6-loopback$\|^#\|^fe00::0 ip6-localnet$\|^ff00::0 ip6-mcastprefix$\|^ff02::1 ip6-allnodes$\|^ff02::2 ip6-allrouters$"')


print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Non Standard files in home folder")
print("\n")
os.system(f'find /home/ -print | grep -v ".bash_history\|.bash_logout\|.bashrc\|.cache\|.config\|.gnupg\|.local\|.mozilla\|.profile\|.sudo_as_admin_successful\|Desktop$\|Downloads$\|Public$\|Videos$\|Templates$\|Documents$\|Music$\|Pictures$\|/home/$\|/home/{main_user}" | grep -E "^/home/[a-zA-Z]+/"')
print("\n\n")

#print(Fore.RED + Back.WHITE + Style.BRIGHT +"Password Policy Configured")
os.system("apt install libpam-pwquality -y 1>/dev/null 0>/dev/null")

print("\n\n")
print(Fore.RED + Back.WHITE + Style.BRIGHT +"Non Standard file perms in /etc (and non standard files)")
print("\n")

default_etc_perms = [' . drwxr-xr-x', '.. drwxr-xr-x', 'acpi drwxr-xr-x', 'adduser.conf -rw-r--r--', 'alsa drwxr-xr-x', 'alternatives drwxr-xr-x', 'anacrontab -rw-r--r--', 'apache2 drwxr-xr-x', 'apg.conf -rw-r--r--', 'apm drwxr-xr-x', 'apparmor drwxr-xr-x', 'apparmor.d drwxr-xr-x', 'apport drwxr-xr-x', 'appstream.conf -rw-r--r--', 'apt drwxr-xr-x', 'avahi drwxr-xr-x', 'bash.bashrc -rw-r--r--', 'bash_completion -rw-r--r--', 'bash_completion.d drwxr-xr-x', 'bindresvport.blacklist -rw-r--r--', 'binfmt.d drwxr-xr-x', 'bluetooth drwxr-xr-x', 'brlapi.key -rw-r-----', 'brltty drwxr-xr-x', 'brltty.conf -rw-r--r--', 'ca-certificates drwxr-xr-x', 'ca-certificates.conf -rw-r--r--', 'ca-certificates.conf.dpkg-old -rw-r--r--', 'calendar drwxr-xr-x', 'chatscripts drwxr-s---', 'console-setup drwxr-xr-x', 'cracklib drwxr-xr-x', 'cron.d drwxr-xr-x', 'cron.daily drwxr-xr-x', 'cron.hourly drwxr-xr-x', 'cron.monthly drwxr-xr-x', 'crontab -rw-r--r--', 'cron.weekly drwxr-xr-x', 'cups drwxr-xr-x', 'cupshelpers drwxr-xr-x', 'dbus-1 drwxr-xr-x', 'dconf drwxr-xr-x', 'debconf.conf -rw-r--r--', 'debian_version -rw-r--r--', 'default drwxr-xr-x', 'deluser.conf -rw-r--r--', 'depmod.d drwxr-xr-x', 'dhcp drwxr-xr-x', 'dictionaries-common drwxr-xr-x', 'dpkg drwxr-xr-x', 'e2scrub.conf -rw-r--r--', 'emacs drwxr-xr-x', 'environment -rw-r--r--', 'environment.d drwxr-xr-x', 'ethertypes -rw-r--r--', 'firefox drwxr-xr-x', 'fonts drwxr-xr-x', 'fprintd.conf -rw-r--r--', 'fstab -rw-rw-r--', 'ftpchroot -rw-r--r--', 'ftpusers -rw-r--r--', 'fuse.conf -rw-r--r--', 'fwupd drwxr-xr-x', 'gai.conf -rw-r--r--', 'gamemode.ini -rw-r--r--', 'gdb drwxr-xr-x', 'gdm3 drwxr-xr-x', 'geoclue drwxr-xr-x', 'ghostscript drwxr-xr-x', 'glvnd drwxr-xr-x', 'gnome drwxr-xr-x', 'groff drwxr-xr-x', 'group -rw-r--r--', 'group- -rw-r--r--', 'grub.d drwxr-xr-x', 'gshadow -rw-r-----', 'gshadow- -rw-r-----', 'gss drwxr-xr-x', 'gtk-2.0 drwxr-xr-x', 'gtk-3.0 drwxr-xr-x', 'hdparm.conf -rw-r--r--', 'host.conf -rw-r--r--', 'hostid -rw-r--r--', 'hostname -rw-r--r--', 'hosts -rw-r--r--', 'hosts.allow -rw-r--r--', 'hosts.deny -rw-r--r--', 'hp drwxr-xr-x', 'ifplugd drwxr-xr-x', 'inetd.conf -rw-r--r--', 'init drwxr-xr-x', 'init.d drwxr-xr-x', 'initramfs-tools drwxr-xr-x', 'inputrc -rw-r--r--', 'insserv.conf.d drwxr-xr-x', 'iproute2 drwxr-xr-x', 'issue -rw-r--r--', 'issue.net -rw-r--r--', 'kernel drwxr-xr-x', 'kernel-img.conf -rw-r--r--', 'kerneloops.conf -rw-r--r--', 'ldap drwxr-xr-x', 'ld.so.cache -rw-r--r--', 'ld.so.conf -rw-r--r--', 'ld.so.conf.d drwxr-xr-x', 'legal -rw-r--r--', 'libao.conf -rw-r--r--', 'libaudit.conf -rw-r--r--', 'libblockdev drwxr-xr-x', 'libibverbs.d drwxr-xr-x', 'libnl-3 drwxr-xr-x', 'libpaper.d drwxr-xr-x', 'locale.alias -rw-r--r--', 'locale.gen -rw-r--r--', 'localtime lrwxrwxrwx', 'logcheck drwxr-xr-x', 'login.defs -rw-r--r--', 'logrotate.conf -rw-r--r--', 'logrotate.d drwxr-xr-x', 'lsb-release -rw-r--r--', 'ltrace.conf -rw-r--r--', 'machine-id -r--r--r--', 'magic -rw-r--r--', 'magic.mime -rw-r--r--', 'mailcap -rw-r--r--', 'mailcap.order -rw-r--r--', 'manpath.config -rw-r--r--', 'mime.types -rw-r--r--', 'mke2fs.conf -rw-r--r--', 'ModemManager drwxr-xr-x', 'modprobe.d drwxr-xr-x', 'modules -rw-r--r--', 'modules-load.d drwxr-xr-x', 'mtab lrwxrwxrwx', 'mtools.conf -rw-r--r--', 'mysql drwxr-xr-x', 'nanorc -rw-r--r--', 'netplan drwxr-xr-x', 'network drwxr-xr-x', 'networkd-dispatcher drwxr-xr-x', 'NetworkManager drwxr-xr-x', 'networks -rw-r--r--', 'newt drwxr-xr-x', 'nginx drwxr-xr-x', 'nsswitch.conf -rw-r--r--', 'openvpn drwxr-xr-x', 'opt drwxr-xr-x', 'os-release lrwxrwxrwx', 'PackageKit drwxr-xr-x', 'pam.conf -rw-r--r--', 'pam.d drwxr-xr-x', 'papersize -rw-rw-r--', 'passwd -rw-r--r--', 'passwd- -rw-r--r--', 'pcmcia drwxr-xr-x', 'perl drwxr-xr-x', 'php drwxr-xr-x', 'pki drwxr-xr-x', 'pm drwxr-xr-x', 'pnm2ppa.conf -rw-r--r--', 'polkit-1 drwxr-xr-x', 'popularity-contest.conf -rw-rw-r--', 'postgresql drwxr-xr-x', 'postgresql-common drwxr-xr-x', 'ppp drwxr-xr-x', 'profile -rw-r--r--', 'profile.d drwxr-xr-x', 'protocols -rw-r--r--', 'pulse drwxr-xr-x', '.pwd.lock -rw-------', 'python3 drwxr-xr-x', 'python3.8 drwxr-xr-x', 'rc0.d drwxr-xr-x', 'rc1.d drwxr-xr-x', 'rc2.d drwxr-xr-x', 'rc3.d drwxr-xr-x', 'rc4.d drwxr-xr-x', 'rc5.d drwxr-xr-x', 'rc6.d drwxr-xr-x', 'rc.local -rw-rw-r--', 'rcS.d drwxr-xr-x', 'resolv.conf lrwxrwxrwx', 'rmt lrwxrwxrwx', 'rpc -rw-r--r--', 'rsyslog.conf -rw-r--r--', 'rsyslog.d drwxr-xr-x', 'rygel.conf -rw-r--r--', 'samba drwxr-xr-x', 'sane.d drwxr-xr-x', 'security drwxr-xr-x', 'selinux drwxr-xr-x', 'sensors3.conf -rw-r--r--', 'sensors.d drwxr-xr-x', 'services -rw-r--r--', 'sgml drwxr-xr-x', 'shadow -rw-r-----', 'shadow- -rw-r-----', 'shells -rw-r--r--', 'skel drwxr-xr-x', 'snmp drwxr-xr-x', 'speech-dispatcher drwxr-xr-x', 'ssh drwxr-xr-x', 'ssl drwxr-xr-x', 'subgid -rw-r--r--', 'subgid- -rw-r--r--', 'subuid -rw-r--r--', 'subuid- -rw-r--r--', 'sudoers -r--r-----', 'sudoers.d drwxr-xr-x', 'sysctl.conf -rw-r--r--', 'sysctl.d drwxr-xr-x', 'sysstat drwxr-xr-x', 'systemd drwxr-xr-x', 'terminfo drwxr-xr-x', 'thermald drwxr-xr-x', 'timezone -rw-r--r--', 'tmpfiles.d drwxr-xr-x', 'ubuntu-advantage drwxr-xr-x', 'ucf.conf -rw-r--r--', 'udev drwxr-xr-x', 'udisks2 drwxr-xr-x', 'ufw drwxr-xr-x', 'update-manager drwxr-xr-x', 'update-motd.d drwxr-xr-x', 'update-notifier drwxr-xr-x', 'UPower drwxr-xr-x', 'usb_modeswitch.conf -rw-r--r--', 'usb_modeswitch.d drwxr-xr-x', 'vim drwxr-xr-x', 'vmware-tools drwxr-xr-x', 'vsftpd.conf -rw-r--r--', 'vtrgb lrwxrwxrwx', 'vulkan drwxr-xr-x', 'wgetrc -rw-r--r--', 'wpa_supplicant drwxr-xr-x', 'X11 drwxr-xr-x', 'xattr.conf -rw-r--r--', 'xdg drwxr-xr-x', 'xml drwxr-xr-x', 'zsh_command_not_found -rw-r--r--']
etc_perms = os.popen("ls -ahl /etc/ | awk '{print $9,$1}' | tr '\n' ',' | sed 's/total,//' | sed 's/,$//'").read().split(",")

for i in etc_perms:
	if i not in default_etc_perms:
		print(i)


print("\n\n\n")
print("printing service things")
print("\n")
running_services = os.popen("service --status-all | grep '\[ + \]' | cut -d' ' -f6").read().split()

default_running_services = ['acpid', 'apparmor', 'apport', 'avahi-daemon', 'cron', 'cups', 'cups-browsed', 'dbus', 'gdm3', 'irqbalance', 'kerneloops', 'kmod', 'network-manager', 'open-vm-tools', 'openvpn', 'procps', 'rsyslog', 'udev', 'ufw', 'unattended-upgrades', 'whoopsie']

for service in running_services:
	if service not in default_running_services:
		print("non default running service: " + service)
print("\n")
for service in default_running_services:
	if service not in running_services:
		print("Non running default service: " + service)



default_files_in_etc = ['/etc/', '/etc/newt', '/etc/newt/palette', '/etc/newt/palette.original', '/etc/newt/palette.ubuntu', '/etc/hostname', '/etc/pulse', '/etc/pulse/client.conf', '/etc/pulse/default.pa', '/etc/pulse/daemon.conf', '/etc/pulse/client.conf.d', '/etc/pulse/client.conf.d/01-enable-autospawn.conf', '/etc/pulse/system.pa', '/etc/profile', '/etc/dbus-1', '/etc/dbus-1/system.d', '/etc/dbus-1/system.d/org.opensuse.CupsPkHelper.Mechanism.conf', '/etc/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf', '/etc/dbus-1/system.d/wpa_supplicant.conf', '/etc/dbus-1/system.d/com.ubuntu.WhoopsiePreferences.conf', '/etc/dbus-1/system.d/org.freedesktop.ModemManager1.conf', '/etc/dbus-1/system.d/com.redhat.PrinterDriversInstaller.conf', '/etc/dbus-1/system.d/com.ubuntu.LanguageSelector.conf', '/etc/dbus-1/system.d/net.hadess.SensorProxy.conf', '/etc/dbus-1/system.d/gdm.conf', '/etc/dbus-1/system.d/com.hp.hplip.conf', '/etc/dbus-1/system.d/net.hadess.SwitcherooControl.conf', '/etc/dbus-1/system.d/dnsmasq.conf', '/etc/dbus-1/system.d/org.freedesktop.Accounts.conf', '/etc/dbus-1/system.d/org.freedesktop.GeoClue2.conf', '/etc/dbus-1/system.d/pulseaudio-system.conf', '/etc/dbus-1/system.d/com.ubuntu.SoftwareProperties.conf', '/etc/dbus-1/system.d/kerneloops.conf', '/etc/dbus-1/system.d/org.freedesktop.thermald.conf', '/etc/dbus-1/system.d/bluetooth.conf', '/etc/dbus-1/system.d/com.redhat.NewPrinterNotification.conf', '/etc/dbus-1/system.d/org.freedesktop.PackageKit.conf', '/etc/dbus-1/system.d/org.debian.apt.conf', '/etc/dbus-1/system.d/avahi-dbus.conf', '/etc/dbus-1/session.d', '/etc/deluser.conf', '/etc/rc6.d', '/etc/rc6.d/K01irqbalance', '/etc/rc6.d/K01cups-browsed', '/etc/rc6.d/K01gdm3', '/etc/rc6.d/K01speech-dispatcher', '/etc/rc6.d/K01open-vm-tools', '/etc/rc6.d/K01openvpn', '/etc/rc6.d/K01rsyslog', '/etc/rc6.d/K01plymouth', '/etc/rc6.d/K01kerneloops', '/etc/rc6.d/K01avahi-daemon', '/etc/rc6.d/K01spice-vdagent', '/etc/rc6.d/K01bluetooth', '/etc/rc6.d/K01pulseaudio-enable-autospawn', '/etc/rc6.d/K01saned', '/etc/rc6.d/K01udev', '/etc/rc6.d/K01unattended-upgrades', '/etc/rc6.d/K01uuidd', '/etc/rc6.d/K01alsa-utils', '/etc/gshadow-', '/etc/cron.monthly', '/etc/cron.monthly/.placeholder', '/etc/cron.monthly/0anacron', '/etc/snmp', '/etc/snmp/snmp.conf', '/etc/depmod.d', '/etc/depmod.d/ubuntu.conf', '/etc/magic', '/etc/perl', '/etc/perl/Net', '/etc/perl/Net/libnet.cfg', '/etc/ld.so.cache', '/etc/usb_modeswitch.conf', '/etc/libblockdev', '/etc/libblockdev/conf.d', '/etc/libblockdev/conf.d/00-default.cfg', '/etc/ppp', '/etc/ppp/ipv6-up.d', '/etc/ppp/chap-secrets', '/etc/ppp/options.pptp', '/etc/ppp/peers', '/etc/ppp/peers/provider', '/etc/ppp/ip-up', '/etc/ppp/ip-down', '/etc/ppp/ipv6-down.d', '/etc/ppp/options', '/etc/ppp/ipv6-down', '/etc/ppp/ip-down.d', '/etc/ppp/ip-down.d/0000usepeerdns', '/etc/ppp/pap-secrets', '/etc/ppp/ip-up.d', '/etc/ppp/ip-up.d/0000usepeerdns', '/etc/ppp/ipv6-up', '/etc/pnm2ppa.conf', '/etc/ld.so.conf.d', '/etc/ld.so.conf.d/x86_64-linux-gnu.conf', '/etc/ld.so.conf.d/libc.conf', '/etc/cron.d', '/etc/cron.d/anacron', '/etc/cron.d/popularity-contest', '/etc/cron.d/.placeholder', '/etc/cron.d/e2scrub_all', '/etc/ld.so.conf', '/etc/mailcap.order', '/etc/ufw', '/etc/ufw/after.init', '/etc/ufw/after6.rules', '/etc/ufw/after.rules', '/etc/ufw/applications.d', '/etc/ufw/applications.d/cups', '/etc/ufw/user6.rules', '/etc/ufw/sysctl.conf', '/etc/ufw/ufw.conf', '/etc/ufw/before.init', '/etc/ufw/user.rules', '/etc/ufw/before.rules', '/etc/ufw/before6.rules', '/etc/groff', '/etc/groff/man.local', '/etc/groff/mdoc.local', '/etc/hosts.deny', '/etc/bash_completion.d', '/etc/bash_completion.d/apport_completion', '/etc/mtab', '/etc/rc5.d', '/etc/rc5.d/S01console-setup.sh', '/etc/rc5.d/S01plymouth', '/etc/rc5.d/S01rsyslog', '/etc/rc5.d/S01irqbalance', '/etc/rc5.d/S01cups', '/etc/rc5.d/K01speech-dispatcher', '/etc/rc5.d/S01cron', '/etc/rc5.d/S01spice-vdagent', '/etc/rc5.d/S01anacron', '/etc/rc5.d/S01openvpn', '/etc/rc5.d/S01unattended-upgrades', '/etc/rc5.d/S01rsync', '/etc/rc5.d/S01cups-browsed', '/etc/rc5.d/S01acpid', '/etc/rc5.d/S01apport', '/etc/rc5.d/S01kerneloops', '/etc/rc5.d/S01pulseaudio-enable-autospawn', '/etc/rc5.d/S01dbus', '/etc/rc5.d/S01grub-common', '/etc/rc5.d/S01avahi-daemon', '/etc/rc5.d/S01open-vm-tools', '/etc/rc5.d/S01uuidd', '/etc/rc5.d/S01gdm3', '/etc/rc5.d/S01bluetooth', '/etc/rc5.d/S01whoopsie', '/etc/rc5.d/S01saned', '/etc/calendar', '/etc/calendar/default', '/etc/popularity-contest.conf', '/etc/e2scrub.conf', '/etc/ca-certificates.conf.dpkg-old', '/etc/locale.alias', '/etc/appstream.conf', '/etc/pam.conf', '/etc/NetworkManager', '/etc/NetworkManager/conf.d', '/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf', '/etc/NetworkManager/system-connections', '/etc/NetworkManager/dnsmasq.d', '/etc/NetworkManager/NetworkManager.conf', '/etc/NetworkManager/dispatcher.d', '/etc/NetworkManager/dispatcher.d/pre-down.d', '/etc/NetworkManager/dispatcher.d/01-ifupdown', '/etc/NetworkManager/dispatcher.d/pre-up.d', '/etc/NetworkManager/dispatcher.d/no-wait.d', '/etc/NetworkManager/dnsmasq-shared.d', '/etc/cron.hourly', '/etc/cron.hourly/.placeholder', '/etc/console-setup', '/etc/console-setup/compose.CP1255.inc', '/etc/console-setup/ISO-8859-1.acm', '/etc/console-setup/compose.IBM1133.inc', '/etc/console-setup/compose.GEORGIAN-PS.inc', '/etc/console-setup/cached_Uni2-Fixed16.psf.gz', '/etc/console-setup/vtrgb.vga', '/etc/console-setup/compose.ISO-8859-1.inc', '/etc/console-setup/compose.CP1256.inc', '/etc/console-setup/compose.ISO-8859-2.inc', '/etc/console-setup/cached_ISO-8859-1.acm.gz', '/etc/console-setup/cached_setup_font.sh', '/etc/console-setup/compose.ISO-8859-7.inc', '/etc/console-setup/compose.CP1251.inc', '/etc/console-setup/compose.ISO-8859-4.inc', '/etc/console-setup/compose.VISCII.inc', '/etc/console-setup/remap.inc', '/etc/console-setup/compose.KOI8-R.inc', '/etc/console-setup/compose.KOI8-U.inc', '/etc/console-setup/cached_setup_terminal.sh', '/etc/console-setup/cached_setup_keyboard.sh', '/etc/console-setup/compose.ISO-8859-15.inc', '/etc/console-setup/compose.ISO-8859-3.inc', '/etc/console-setup/compose.GEORGIAN-ACADEMY.inc', '/etc/console-setup/vtrgb', '/etc/console-setup/compose.ARMSCII-8.inc', '/etc/console-setup/compose.ISO-8859-5.inc', '/etc/console-setup/compose.ISO-8859-9.inc', '/etc/console-setup/compose.ISO-8859-11.inc', '/etc/console-setup/compose.ISO-8859-13.inc', '/etc/console-setup/compose.ISO-8859-16.inc', '/etc/console-setup/cached_ISO-8859-1_del.kmap.gz', '/etc/console-setup/compose.TIS-620.inc', '/etc/console-setup/cached_UTF-8_del.kmap.gz', '/etc/console-setup/compose.ISO-8859-10.inc', '/etc/console-setup/compose.ISO-8859-8.inc', '/etc/console-setup/Uni2-Fixed16.psf.gz', '/etc/console-setup/compose.ISIRI-3342.inc', '/etc/console-setup/compose.ISO-8859-14.inc', '/etc/console-setup/compose.ISO-8859-6.inc', '/etc/avahi', '/etc/avahi/avahi-daemon.conf', '/etc/avahi/avahi-autoipd.action', '/etc/avahi/services', '/etc/avahi/hosts', '/etc/gshadow', '/etc/rygel.conf', '/etc/security', '/etc/security/limits.d', '/etc/security/pwquality.conf', '/etc/security/sepermit.conf', '/etc/security/access.conf', '/etc/security/namespace.init', '/etc/security/pam_env.conf', '/etc/security/namespace.d', '/etc/security/time.conf', '/etc/security/group.conf', '/etc/security/faillock.conf', '/etc/security/capability.conf', '/etc/security/namespace.conf', '/etc/security/opasswd', '/etc/security/limits.conf', '/etc/grub.d', '/etc/grub.d/40_custom', '/etc/grub.d/30_uefi-firmware', '/etc/grub.d/30_os-prober', '/etc/grub.d/20_memtest86+', '/etc/grub.d/05_debian_theme', '/etc/grub.d/20_linux_xen', '/etc/grub.d/README', '/etc/grub.d/35_fwupd', '/etc/grub.d/00_header', '/etc/grub.d/10_linux', '/etc/grub.d/41_custom', '/etc/grub.d/10_linux_zfs', '/etc/services', '/etc/sensors3.conf', '/etc/ldap', '/etc/ldap/ldap.conf', '/etc/geoclue', '/etc/geoclue/geoclue.conf', '/etc/inputrc', '/etc/xdg', '/etc/xdg/user-dirs.conf', '/etc/xdg/Xwayland-session.d', '/etc/xdg/Xwayland-session.d/00-xrdb', '/etc/xdg/user-dirs.defaults', '/etc/xdg/autostart', '/etc/xdg/autostart/org.gnome.SettingsDaemon.UsbProtection.desktop', '/etc/xdg/autostart/gnome-initial-setup-first-login.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Wacom.desktop', '/etc/xdg/autostart/update-notifier.desktop', '/etc/xdg/autostart/ubuntu-report-on-upgrade.desktop', '/etc/xdg/autostart/geoclue-demo-agent.desktop', '/etc/xdg/autostart/gnome-keyring-ssh.desktop', '/etc/xdg/autostart/at-spi-dbus-bus.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Color.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.MediaKeys.desktop', '/etc/xdg/autostart/orca-autostart.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.PrintNotifications.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Housekeeping.desktop', '/etc/xdg/autostart/gnome-welcome-tour.desktop', '/etc/xdg/autostart/print-applet.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.DiskUtilityNotify.desktop', '/etc/xdg/autostart/user-dirs-update-gtk.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Datetime.desktop', '/etc/xdg/autostart/spice-vdagent.desktop', '/etc/xdg/autostart/gnome-keyring-pkcs11.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.A11ySettings.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Wwan.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.ScreensaverProxy.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Keyboard.desktop', '/etc/xdg/autostart/im-launch.desktop', '/etc/xdg/autostart/tracker-extract.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Smartcard.desktop', '/etc/xdg/autostart/gnome-initial-setup-copy-worker.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Sharing.desktop', '/etc/xdg/autostart/vmware-user.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Sound.desktop', '/etc/xdg/autostart/org.gnome.Evolution-alarm-notify.desktop', '/etc/xdg/autostart/xdg-user-dirs.desktop', '/etc/xdg/autostart/gnome-keyring-secrets.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.XSettings.desktop', '/etc/xdg/autostart/gnome-shell-overrides-migration.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Power.desktop', '/etc/xdg/autostart/pulseaudio.desktop', '/etc/xdg/autostart/tracker-miner-fs.desktop', '/etc/xdg/autostart/nm-applet.desktop', '/etc/xdg/autostart/org.gnome.SettingsDaemon.Rfkill.desktop', '/etc/xdg/autostart/snap-userd-autostart.desktop', '/etc/xdg/systemd', '/etc/xdg/systemd/user', '/etc/xdg/menus', '/etc/xdg/menus/gnome-applications.menu', '/etc/hdparm.conf', '/etc/ifplugd', '/etc/ifplugd/action.d', '/etc/ifplugd/action.d/action_wpa', '/etc/init.d', '/etc/init.d/hwclock.sh', '/etc/init.d/network-manager', '/etc/init.d/anacron', '/etc/init.d/ufw', '/etc/init.d/kmod', '/etc/init.d/kerneloops', '/etc/init.d/plymouth-log', '/etc/init.d/plymouth', '/etc/init.d/unattended-upgrades', '/etc/init.d/rsync', '/etc/init.d/pulseaudio-enable-autospawn', '/etc/init.d/pppd-dns', '/etc/init.d/dbus', '/etc/init.d/open-vm-tools', '/etc/init.d/gdm3', '/etc/init.d/speech-dispatcher', '/etc/init.d/spice-vdagent', '/etc/init.d/avahi-daemon', '/etc/init.d/rsyslog', '/etc/init.d/x11-common', '/etc/init.d/udev', '/etc/init.d/acpid', '/etc/init.d/cups-browsed', '/etc/init.d/irqbalance', '/etc/init.d/openvpn', '/etc/init.d/cups', '/etc/init.d/console-setup.sh', '/etc/init.d/saned', '/etc/init.d/apparmor', '/etc/init.d/alsa-utils', '/etc/init.d/keyboard-setup.sh', '/etc/init.d/procps', '/etc/init.d/grub-common', '/etc/init.d/uuidd', '/etc/init.d/apport', '/etc/init.d/whoopsie', '/etc/init.d/cron', '/etc/init.d/bluetooth', '/etc/rc3.d', '/etc/rc3.d/S01console-setup.sh', '/etc/rc3.d/S01plymouth', '/etc/rc3.d/S01rsyslog', '/etc/rc3.d/S01irqbalance', '/etc/rc3.d/S01cups', '/etc/rc3.d/K01speech-dispatcher', '/etc/rc3.d/S01cron', '/etc/rc3.d/S01spice-vdagent', '/etc/rc3.d/S01anacron', '/etc/rc3.d/S01openvpn', '/etc/rc3.d/S01unattended-upgrades', '/etc/rc3.d/S01rsync', '/etc/rc3.d/S01cups-browsed', '/etc/rc3.d/S01acpid', '/etc/rc3.d/S01apport', '/etc/rc3.d/S01kerneloops', '/etc/rc3.d/S01pulseaudio-enable-autospawn', '/etc/rc3.d/S01dbus', '/etc/rc3.d/S01grub-common', '/etc/rc3.d/S01avahi-daemon', '/etc/rc3.d/S01open-vm-tools', '/etc/rc3.d/S01uuidd', '/etc/rc3.d/S01gdm3', '/etc/rc3.d/S01bluetooth', '/etc/rc3.d/S01whoopsie', '/etc/rc3.d/S01saned', '/etc/mtools.conf', '/etc/os-release', '/etc/apg.conf', '/etc/vulkan', '/etc/vulkan/implicit_layer.d', '/etc/vulkan/icd.d', '/etc/vulkan/explicit_layer.d', '/etc/insserv.conf.d', '/etc/insserv.conf.d/gdm3', '/etc/python3', '/etc/python3/debian_config', '/etc/acpi', '/etc/acpi/tosh-wireless.sh', '/etc/acpi/asus-keyboard-backlight.sh', '/etc/acpi/undock.sh', '/etc/acpi/asus-wireless.sh', '/etc/acpi/ibm-wireless.sh', '/etc/acpi/events', '/etc/acpi/events/lenovo-undock', '/etc/acpi/events/asus-wireless-on', '/etc/acpi/events/ibm-wireless', '/etc/acpi/events/asus-wireless-off', '/etc/acpi/events/asus-keyboard-backlight-down', '/etc/acpi/events/thinkpad-cmos', '/etc/acpi/events/tosh-wireless', '/etc/acpi/events/asus-keyboard-backlight-up', '/etc/libpaper.d', '/etc/PackageKit', '/etc/PackageKit/PackageKit.conf', '/etc/PackageKit/Vendor.conf', '/etc/logrotate.conf', '/etc/modules', '/etc/firefox', '/etc/firefox/syspref.js', '/etc/firefox/pref', '/etc/firefox/pref/apturl.js', '/etc/magic.mime', '/etc/sensors.d', '/etc/sensors.d/.placeholder', '/etc/libao.conf', '/etc/xml', '/etc/xml/sgml-data.xml.old', '/etc/xml/xml-core.xml', '/etc/xml/docbook-xml.xml.old', '/etc/xml/catalog.old', '/etc/xml/catalog', '/etc/xml/xml-core.xml.old', '/etc/xml/docbook-xml.xml', '/etc/xml/sgml-data.xml', '/etc/xattr.conf', '/etc/login.defs', '/etc/apparmor.d', '/etc/apparmor.d/usr.sbin.cups-browsed', '/etc/apparmor.d/usr.sbin.rsyslogd', '/etc/apparmor.d/lsb_release', '/etc/apparmor.d/usr.sbin.ippusbxd', '/etc/apparmor.d/nvidia_modprobe', '/etc/apparmor.d/local', '/etc/apparmor.d/local/usr.sbin.cups-browsed', '/etc/apparmor.d/local/usr.sbin.rsyslogd', '/etc/apparmor.d/local/lsb_release', '/etc/apparmor.d/local/usr.sbin.ippusbxd', '/etc/apparmor.d/local/nvidia_modprobe', '/etc/apparmor.d/local/usr.sbin.cupsd', '/etc/apparmor.d/local/usr.bin.evince', '/etc/apparmor.d/local/usr.bin.man', '/etc/apparmor.d/local/usr.bin.firefox', '/etc/apparmor.d/local/README', '/etc/apparmor.d/local/sbin.dhclient', '/etc/apparmor.d/local/usr.lib.snapd.snap-confine.real', '/etc/apparmor.d/local/usr.sbin.tcpdump', '/etc/apparmor.d/abstractions', '/etc/apparmor.d/abstractions/opencl-intel', '/etc/apparmor.d/abstractions/gnupg', '/etc/apparmor.d/abstractions/evince', '/etc/apparmor.d/abstractions/user-manpages', '/etc/apparmor.d/abstractions/libpam-systemd', '/etc/apparmor.d/abstractions/wutmp', '/etc/apparmor.d/abstractions/perl', '/etc/apparmor.d/abstractions/samba', '/etc/apparmor.d/abstractions/video', '/etc/apparmor.d/abstractions/enchant', '/etc/apparmor.d/abstractions/X', '/etc/apparmor.d/abstractions/ruby', '/etc/apparmor.d/abstractions/dbus-accessibility-strict', '/etc/apparmor.d/abstractions/ubuntu-konsole', '/etc/apparmor.d/abstractions/php', '/etc/apparmor.d/abstractions/nameservice', '/etc/apparmor.d/abstractions/opencl', '/etc/apparmor.d/abstractions/dbus-session', '/etc/apparmor.d/abstractions/apache2-common', '/etc/apparmor.d/abstractions/php5', '/etc/apparmor.d/abstractions/audio', '/etc/apparmor.d/abstractions/wayland', '/etc/apparmor.d/abstractions/opencl-common', '/etc/apparmor.d/abstractions/postfix-common', '/etc/apparmor.d/abstractions/ubuntu-unity7-launcher', '/etc/apparmor.d/abstractions/nvidia', '/etc/apparmor.d/abstractions/qt5-settings-write', '/etc/apparmor.d/abstractions/vulkan', '/etc/apparmor.d/abstractions/qt5', '/etc/apparmor.d/abstractions/kde', '/etc/apparmor.d/abstractions/xad', '/etc/apparmor.d/abstractions/freedesktop.org', '/etc/apparmor.d/abstractions/dbus-session-strict', '/etc/apparmor.d/abstractions/dbus', '/etc/apparmor.d/abstractions/nis', '/etc/apparmor.d/abstractions/svn-repositories', '/etc/apparmor.d/abstractions/mdns', '/etc/apparmor.d/abstractions/smbpass', '/etc/apparmor.d/abstractions/kde-language-write', '/etc/apparmor.d/abstractions/opencl-mesa', '/etc/apparmor.d/abstractions/p11-kit', '/etc/apparmor.d/abstractions/ubuntu-helpers', '/etc/apparmor.d/abstractions/mesa', '/etc/apparmor.d/abstractions/ubuntu-feed-readers', '/etc/apparmor.d/abstractions/aspell', '/etc/apparmor.d/abstractions/likewise', '/etc/apparmor.d/abstractions/web-data', '/etc/apparmor.d/abstractions/qt5-compose-cache-write', '/etc/apparmor.d/abstractions/fonts', '/etc/apparmor.d/abstractions/python', '/etc/apparmor.d/abstractions/user-mail', '/etc/apparmor.d/abstractions/dovecot-common', '/etc/apparmor.d/abstractions/user-write', '/etc/apparmor.d/abstractions/ubuntu-media-players', '/etc/apparmor.d/abstractions/ubuntu-gnome-terminal', '/etc/apparmor.d/abstractions/kerberosclient', '/etc/apparmor.d/abstractions/ubuntu-browsers.d', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/ubuntu-integration', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/kde', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/firefox', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/plugins-common', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/text-editors', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/mailto', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/user-files', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/multimedia', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/productivity', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/ubuntu-integration-xul', '/etc/apparmor.d/abstractions/ubuntu-browsers.d/java', '/etc/apparmor.d/abstractions/xdg-desktop', '/etc/apparmor.d/abstractions/dri-enumerate', '/etc/apparmor.d/abstractions/gnome', '/etc/apparmor.d/abstractions/ssl_certs', '/etc/apparmor.d/abstractions/ubuntu-xterm', '/etc/apparmor.d/abstractions/kde-globals-write', '/etc/apparmor.d/abstractions/ubuntu-unity7-base', '/etc/apparmor.d/abstractions/opencl-pocl', '/etc/apparmor.d/abstractions/base', '/etc/apparmor.d/abstractions/ibus', '/etc/apparmor.d/abstractions/ubuntu-unity7-messaging', '/etc/apparmor.d/abstractions/fcitx-strict', '/etc/apparmor.d/abstractions/user-download', '/etc/apparmor.d/abstractions/user-tmp', '/etc/apparmor.d/abstractions/mysql', '/etc/apparmor.d/abstractions/opencl-nvidia', '/etc/apparmor.d/abstractions/bash', '/etc/apparmor.d/abstractions/ubuntu-bittorrent-clients', '/etc/apparmor.d/abstractions/ubuntu-console-email', '/etc/apparmor.d/abstractions/consoles', '/etc/apparmor.d/abstractions/ubuntu-console-browsers', '/etc/apparmor.d/abstractions/dri-common', '/etc/apparmor.d/abstractions/apparmor_api', '/etc/apparmor.d/abstractions/apparmor_api/change_profile', '/etc/apparmor.d/abstractions/apparmor_api/is_enabled', '/etc/apparmor.d/abstractions/apparmor_api/find_mountpoint', '/etc/apparmor.d/abstractions/apparmor_api/examine', '/etc/apparmor.d/abstractions/apparmor_api/introspect', '/etc/apparmor.d/abstractions/cups-client', '/etc/apparmor.d/abstractions/winbind', '/etc/apparmor.d/abstractions/orbit2', '/etc/apparmor.d/abstractions/mozc', '/etc/apparmor.d/abstractions/recent-documents-write', '/etc/apparmor.d/abstractions/ubuntu-email', '/etc/apparmor.d/abstractions/ubuntu-browsers', '/etc/apparmor.d/abstractions/dconf', '/etc/apparmor.d/abstractions/dbus-accessibility', '/etc/apparmor.d/abstractions/dbus-strict', '/etc/apparmor.d/abstractions/ldapclient', '/etc/apparmor.d/abstractions/private-files', '/etc/apparmor.d/abstractions/authentication', '/etc/apparmor.d/abstractions/kde-icon-cache-write', '/etc/apparmor.d/abstractions/mir', '/etc/apparmor.d/abstractions/openssl', '/etc/apparmor.d/abstractions/private-files-strict', '/etc/apparmor.d/abstractions/ssl_keys', '/etc/apparmor.d/abstractions/fcitx', '/etc/apparmor.d/usr.sbin.cupsd', '/etc/apparmor.d/disable', '/etc/apparmor.d/disable/usr.sbin.rsyslogd', '/etc/apparmor.d/disable/usr.bin.firefox', '/etc/apparmor.d/usr.bin.evince', '/etc/apparmor.d/usr.bin.man', '/etc/apparmor.d/usr.bin.firefox', '/etc/apparmor.d/sbin.dhclient', '/etc/apparmor.d/usr.lib.snapd.snap-confine.real', '/etc/apparmor.d/usr.sbin.tcpdump', '/etc/apparmor.d/tunables', '/etc/apparmor.d/tunables/sys', '/etc/apparmor.d/tunables/xdg-user-dirs', '/etc/apparmor.d/tunables/home', '/etc/apparmor.d/tunables/alias', '/etc/apparmor.d/tunables/share', '/etc/apparmor.d/tunables/multiarch.d', '/etc/apparmor.d/tunables/multiarch.d/site.local', '/etc/apparmor.d/tunables/proc', '/etc/apparmor.d/tunables/dovecot', '/etc/apparmor.d/tunables/securityfs', '/etc/apparmor.d/tunables/apparmorfs', '/etc/apparmor.d/tunables/xdg-user-dirs.d', '/etc/apparmor.d/tunables/xdg-user-dirs.d/site.local', '/etc/apparmor.d/tunables/multiarch', '/etc/apparmor.d/tunables/global', '/etc/apparmor.d/tunables/home.d', '/etc/apparmor.d/tunables/home.d/site.local', '/etc/apparmor.d/tunables/home.d/ubuntu', '/etc/apparmor.d/tunables/kernelvars', '/etc/hostid', '/etc/tmpfiles.d', '/etc/mke2fs.conf', '/etc/cupshelpers', '/etc/cupshelpers/preferreddrivers.xml', '/etc/hp', '/etc/hp/hplip.conf', '/etc/bash_completion', '/etc/nsswitch.conf', '/etc/update-manager', '/etc/update-manager/meta-release', '/etc/update-manager/release-upgrades', '/etc/update-manager/release-upgrades.d', '/etc/update-manager/release-upgrades.d/ubuntu-advantage-upgrades.cfg', '/etc/iproute2', '/etc/iproute2/rt_protos.d', '/etc/iproute2/rt_protos.d/README', '/etc/iproute2/rt_scopes', '/etc/iproute2/rt_protos', '/etc/iproute2/rt_tables.d', '/etc/iproute2/rt_tables.d/README', '/etc/iproute2/nl_protos', '/etc/iproute2/ematch_map', '/etc/iproute2/rt_tables', '/etc/iproute2/rt_dsfield', '/etc/iproute2/rt_realms', '/etc/iproute2/group', '/etc/iproute2/bpf_pinning', '/etc/gdm3', '/etc/gdm3/Prime', '/etc/gdm3/Prime/Default', '/etc/gdm3/PreSession', '/etc/gdm3/PreSession/Default', '/etc/gdm3/custom.conf', '/etc/gdm3/Xsession', '/etc/gdm3/greeter.dconf-defaults', '/etc/gdm3/PostSession', '/etc/gdm3/PostSession/Default', '/etc/gdm3/config-error-dialog.sh', '/etc/gdm3/Init', '/etc/gdm3/Init/Default', '/etc/gdm3/PostLogin', '/etc/gdm3/PostLogin/Default.sample', '/etc/gdm3/PrimeOff', '/etc/gdm3/PrimeOff/Default', '/etc/terminfo', '/etc/terminfo/README', '/etc/ethertypes', '/etc/issue.net', '/etc/thermald', '/etc/thermald/thermal-cpu-cdev-order.xml', '/etc/sysctl.d', '/etc/sysctl.d/10-link-restrictions.conf', '/etc/sysctl.d/10-ipv6-privacy.conf', '/etc/sysctl.d/10-magic-sysrq.conf', '/etc/sysctl.d/10-console-messages.conf', '/etc/sysctl.d/10-kernel-hardening.conf', '/etc/sysctl.d/99-sysctl.conf', '/etc/sysctl.d/10-network-security.conf', '/etc/sysctl.d/10-zeropage.conf', '/etc/sysctl.d/README.sysctl', '/etc/sysctl.d/10-ptrace.conf', '/etc/gai.conf', '/etc/bash.bashrc', '/etc/resolv.conf', '/etc/apm', '/etc/apm/resume.d', '/etc/apm/resume.d/20alsa', '/etc/apm/suspend.d', '/etc/apm/suspend.d/80alsa', '/etc/apm/scripts.d', '/etc/apm/scripts.d/alsa', '/etc/rc4.d', '/etc/rc4.d/S01console-setup.sh', '/etc/rc4.d/S01plymouth', '/etc/rc4.d/S01rsyslog', '/etc/rc4.d/S01irqbalance', '/etc/rc4.d/S01cups', '/etc/rc4.d/K01speech-dispatcher', '/etc/rc4.d/S01cron', '/etc/rc4.d/S01spice-vdagent', '/etc/rc4.d/S01anacron', '/etc/rc4.d/S01openvpn', '/etc/rc4.d/S01unattended-upgrades', '/etc/rc4.d/S01rsync', '/etc/rc4.d/S01cups-browsed', '/etc/rc4.d/S01acpid', '/etc/rc4.d/S01apport', '/etc/rc4.d/S01kerneloops', '/etc/rc4.d/S01pulseaudio-enable-autospawn', '/etc/rc4.d/S01dbus', '/etc/rc4.d/S01grub-common', '/etc/rc4.d/S01avahi-daemon', '/etc/rc4.d/S01open-vm-tools', '/etc/rc4.d/S01uuidd', '/etc/rc4.d/S01gdm3', '/etc/rc4.d/S01bluetooth', '/etc/rc4.d/S01whoopsie', '/etc/rc4.d/S01saned', '/etc/subuid-', '/etc/brlapi.key', '/etc/cron.weekly', '/etc/cron.weekly/.placeholder', '/etc/cron.weekly/update-notifier-common', '/etc/cron.weekly/man-db', '/etc/cron.weekly/0anacron', '/etc/subgid', '/etc/nanorc', '/etc/timezone', '/etc/alsa', '/etc/alsa/conf.d', '/etc/alsa/conf.d/50-arcam-av-ctl.conf', '/etc/alsa/conf.d/50-pulseaudio.conf', '/etc/alsa/conf.d/98-usb-stream.conf', '/etc/alsa/conf.d/99-pulseaudio-default.conf.example', '/etc/alsa/conf.d/60-upmix.conf', '/etc/alsa/conf.d/99-pulse.conf', '/etc/alsa/conf.d/50-jack.conf', '/etc/alsa/conf.d/50-oss.conf', '/etc/alsa/conf.d/60-vdownmix.conf', '/etc/alsa/conf.d/10-speexrate.conf', '/etc/alsa/conf.d/10-samplerate.conf', '/etc/rc0.d', '/etc/rc0.d/K01irqbalance', '/etc/rc0.d/K01cups-browsed', '/etc/rc0.d/K01gdm3', '/etc/rc0.d/K01speech-dispatcher', '/etc/rc0.d/K01open-vm-tools', '/etc/rc0.d/K01openvpn', '/etc/rc0.d/K01rsyslog', '/etc/rc0.d/K01plymouth', '/etc/rc0.d/K01kerneloops', '/etc/rc0.d/K01avahi-daemon', '/etc/rc0.d/K01spice-vdagent', '/etc/rc0.d/K01bluetooth', '/etc/rc0.d/K01pulseaudio-enable-autospawn', '/etc/rc0.d/K01saned', '/etc/rc0.d/K01udev', '/etc/rc0.d/K01unattended-upgrades', '/etc/rc0.d/K01uuidd', '/etc/rc0.d/K01alsa-utils', '/etc/ltrace.conf', '/etc/speech-dispatcher', '/etc/speech-dispatcher/modules', '/etc/speech-dispatcher/modules/epos-generic.conf', '/etc/speech-dispatcher/modules/mary-generic.conf', '/etc/speech-dispatcher/modules/kali.conf', '/etc/speech-dispatcher/modules/espeak-ng-mbrola-generic.conf', '/etc/speech-dispatcher/modules/cicero.conf', '/etc/speech-dispatcher/modules/espeak-generic.conf', '/etc/speech-dispatcher/modules/ivona.conf', '/etc/speech-dispatcher/modules/espeak-mbrola-generic.conf', '/etc/speech-dispatcher/modules/espeak.conf', '/etc/speech-dispatcher/modules/dtk-generic.conf', '/etc/speech-dispatcher/modules/flite.conf', '/etc/speech-dispatcher/modules/espeak-ng.conf', '/etc/speech-dispatcher/modules/baratinoo.conf', '/etc/speech-dispatcher/modules/swift-generic.conf', '/etc/speech-dispatcher/modules/pico-generic.conf', '/etc/speech-dispatcher/modules/ibmtts.conf', '/etc/speech-dispatcher/modules/festival.conf', '/etc/speech-dispatcher/modules/llia_phon-generic.conf', '/etc/speech-dispatcher/speechd.conf', '/etc/speech-dispatcher/clients', '/etc/speech-dispatcher/clients/emacs.conf', '/etc/init', '/etc/init/whoopsie.conf', '/etc/cron.daily', '/etc/cron.daily/apt-compat', '/etc/cron.daily/logrotate', '/etc/cron.daily/bsdmainutils', '/etc/cron.daily/popularity-contest', '/etc/cron.daily/.placeholder', '/etc/cron.daily/update-notifier-common', '/etc/cron.daily/man-db', '/etc/cron.daily/0anacron', '/etc/cron.daily/dpkg', '/etc/cron.daily/apport', '/etc/cron.daily/cracklib-runtime', '/etc/shadow', '/etc/fonts', '/etc/fonts/conf.avail', '/etc/fonts/conf.avail/67-smc-suruma.conf', '/etc/fonts/conf.avail/40-nonlatin.conf', '/etc/fonts/conf.avail/99-language-selector-zh.conf', '/etc/fonts/conf.avail/65-0-fonts-pagul.conf', '/etc/fonts/conf.avail/67-lohit-malayalam.conf', '/etc/fonts/conf.avail/66-lohit-bengali.conf', '/etc/fonts/conf.avail/57-dejavu-serif.conf', '/etc/fonts/conf.avail/80-delicious.conf', '/etc/fonts/conf.avail/30-cjk-aliases.conf', '/etc/fonts/conf.avail/69-language-selector-zh-hk.conf', '/etc/fonts/conf.avail/20-unhint-small-dejavu-lgc-sans-mono.conf', '/etc/fonts/conf.avail/51-local.conf', '/etc/fonts/conf.avail/66-lohit-assamese.conf', '/etc/fonts/conf.avail/69-unifont.conf', '/etc/fonts/conf.avail/70-force-bitmaps.conf', '/etc/fonts/conf.avail/67-fonts-smc-manjari.conf', '/etc/fonts/conf.avail/10-hinting-full.conf', '/etc/fonts/conf.avail/10-antialias.conf', '/etc/fonts/conf.avail/10-autohint.conf', '/etc/fonts/conf.avail/10-hinting-none.conf', '/etc/fonts/conf.avail/65-nonlatin.conf', '/etc/fonts/conf.avail/58-dejavu-lgc-sans-mono.conf', '/etc/fonts/conf.avail/67-smc-anjalioldlipi.conf', '/etc/fonts/conf.avail/66-lohit-kannada.conf', '/etc/fonts/conf.avail/65-0-fonts-gujr-extra.conf', '/etc/fonts/conf.avail/53-monospace-lcd-filter.conf', '/etc/fonts/conf.avail/66-lohit-telugu.conf', '/etc/fonts/conf.avail/65-0-fonts-orya-extra.conf', '/etc/fonts/conf.avail/66-lohit-gujarati.conf', '/etc/fonts/conf.avail/57-dejavu-sans-mono.conf', '/etc/fonts/conf.avail/57-dejavu-sans.conf', '/etc/fonts/conf.avail/65-0-fonts-telu-extra.conf', '/etc/fonts/conf.avail/20-unhint-small-dejavu-lgc-serif.conf', '/etc/fonts/conf.avail/49-sansserif.conf', '/etc/fonts/conf.avail/20-unhint-small-dejavu-serif.conf', '/etc/fonts/conf.avail/10-sub-pixel-vbgr.conf', '/etc/fonts/conf.avail/45-latin.conf', '/etc/fonts/conf.avail/69-language-selector-ja.conf', '/etc/fonts/conf.avail/11-lcdfilter-default.conf', '/etc/fonts/conf.avail/65-0-fonts-beng-extra.conf', '/etc/fonts/conf.avail/67-smc-raghumalayalamsans.conf', '/etc/fonts/conf.avail/60-latin.conf', '/etc/fonts/conf.avail/45-generic.conf', '/etc/fonts/conf.avail/67-smc-karumbi.conf', '/etc/fonts/conf.avail/10-hinting-medium.conf', '/etc/fonts/conf.avail/65-fonts-persian.conf', '/etc/fonts/conf.avail/60-generic.conf', '/etc/fonts/conf.avail/65-0-fonts-deva-extra.conf', '/etc/fonts/conf.avail/30-metric-aliases.conf', '/etc/fonts/conf.avail/66-lohit-tamil.conf', '/etc/fonts/conf.avail/25-unhint-nonlatin.conf', '/etc/fonts/conf.avail/56-language-selector-ar.conf', '/etc/fonts/conf.avail/50-user.conf', '/etc/fonts/conf.avail/20-unhint-small-dejavu-sans-mono.conf', '/etc/fonts/conf.avail/67-smc-chilanka.conf', '/etc/fonts/conf.avail/11-lcdfilter-legacy.conf', '/etc/fonts/conf.avail/65-0-smc-meera.conf', '/etc/fonts/conf.avail/58-dejavu-lgc-serif.conf', '/etc/fonts/conf.avail/65-khmer.conf', '/etc/fonts/conf.avail/65-droid-sans-fallback.conf', '/etc/fonts/conf.avail/11-lcdfilter-light.conf', '/etc/fonts/conf.avail/70-yes-bitmaps.conf', '/etc/fonts/conf.avail/10-no-sub-pixel.conf', '/etc/fonts/conf.avail/67-smc-dyuthi.conf', '/etc/fonts/conf.avail/69-language-selector-zh-mo.conf', '/etc/fonts/conf.avail/10-sub-pixel-bgr.conf', '/etc/fonts/conf.avail/66-lohit-devanagari.conf', '/etc/fonts/conf.avail/67-smc-keraleeyam.conf', '/etc/fonts/conf.avail/10-unhinted.conf', '/etc/fonts/conf.avail/65-0-fonts-guru-extra.conf', '/etc/fonts/conf.avail/58-dejavu-lgc-sans.conf', '/etc/fonts/conf.avail/20-unhint-small-dejavu-lgc-sans.conf', '/etc/fonts/conf.avail/69-language-selector-zh-tw.conf', '/etc/fonts/conf.avail/69-language-selector-zh-cn.conf', '/etc/fonts/conf.avail/90-synthetic.conf', '/etc/fonts/conf.avail/30-droid-noto-mono.conf', '/etc/fonts/conf.avail/59-lohit-devanagari.conf', '/etc/fonts/conf.avail/69-language-selector-zh-sg.conf', '/etc/fonts/conf.avail/20-unhint-small-vera.conf', '/etc/fonts/conf.avail/64-language-selector-prefer.conf', '/etc/fonts/conf.avail/65-0-fonts-gubbi.conf', '/etc/fonts/conf.avail/10-hinting-slight.conf', '/etc/fonts/conf.avail/10-scale-bitmap-fonts.conf', '/etc/fonts/conf.avail/65-0-smc-rachana.conf', '/etc/fonts/conf.avail/10-sub-pixel-vrgb.conf', '/etc/fonts/conf.avail/66-lohit-tamil-classical.conf', '/etc/fonts/conf.avail/66-lohit-gurmukhi.conf', '/etc/fonts/conf.avail/70-no-bitmaps.conf', '/etc/fonts/conf.avail/67-smc-uroob.conf', '/etc/fonts/conf.avail/10-sub-pixel-rgb.conf', '/etc/fonts/conf.avail/66-lohit-odia.conf', '/etc/fonts/conf.avail/20-unhint-small-dejavu-sans.conf', '/etc/fonts/conf.d', '/etc/fonts/conf.d/61-urw-p052.conf', '/etc/fonts/conf.d/64-21-tlwg-typo.conf', '/etc/fonts/conf.d/61-urw-nimbus-mono-ps.conf', '/etc/fonts/conf.d/67-smc-suruma.conf', '/etc/fonts/conf.d/40-nonlatin.conf', '/etc/fonts/conf.d/99-language-selector-zh.conf', '/etc/fonts/conf.d/65-0-fonts-pagul.conf', '/etc/fonts/conf.d/61-urw-bookman.conf', '/etc/fonts/conf.d/66-lohit-bengali.conf', '/etc/fonts/conf.d/57-dejavu-serif.conf', '/etc/fonts/conf.d/80-delicious.conf', '/etc/fonts/conf.d/64-22-tlwg-typist.conf', '/etc/fonts/conf.d/30-cjk-aliases.conf', '/etc/fonts/conf.d/69-language-selector-zh-hk.conf', '/etc/fonts/conf.d/61-urw-fallback-backwards.conf', '/etc/fonts/conf.d/20-unhint-small-dejavu-lgc-sans-mono.conf', '/etc/fonts/conf.d/51-local.conf', '/etc/fonts/conf.d/61-urw-z003.conf', '/etc/fonts/conf.d/66-lohit-assamese.conf', '/etc/fonts/conf.d/64-13-tlwg-garuda.conf', '/etc/fonts/conf.d/69-unifont.conf', '/etc/fonts/conf.d/67-fonts-smc-manjari.conf', '/etc/fonts/conf.d/10-antialias.conf', '/etc/fonts/conf.d/64-14-tlwg-umpush.conf', '/etc/fonts/conf.d/65-nonlatin.conf', '/etc/fonts/conf.d/58-dejavu-lgc-sans-mono.conf', '/etc/fonts/conf.d/67-smc-anjalioldlipi.conf', '/etc/fonts/conf.d/66-lohit-kannada.conf', '/etc/fonts/conf.d/65-0-fonts-gujr-extra.conf', '/etc/fonts/conf.d/64-11-tlwg-waree.conf', '/etc/fonts/conf.d/66-lohit-telugu.conf', '/etc/fonts/conf.d/89-tlwg-garuda-synthetic.conf', '/etc/fonts/conf.d/65-0-fonts-orya-extra.conf', '/etc/fonts/conf.d/61-urw-standard-symbols-ps.conf', '/etc/fonts/conf.d/61-urw-nimbus-sans.conf', '/etc/fonts/conf.d/66-lohit-gujarati.conf', '/etc/fonts/conf.d/57-dejavu-sans-mono.conf', '/etc/fonts/conf.d/61-urw-d050000l.conf', '/etc/fonts/conf.d/57-dejavu-sans.conf', '/etc/fonts/conf.d/65-0-fonts-telu-extra.conf', '/etc/fonts/conf.d/89-tlwg-kinnari-synthetic.conf', '/etc/fonts/conf.d/20-unhint-small-dejavu-lgc-serif.conf', '/etc/fonts/conf.d/49-sansserif.conf', '/etc/fonts/conf.d/20-unhint-small-dejavu-serif.conf', '/etc/fonts/conf.d/45-latin.conf', '/etc/fonts/conf.d/69-language-selector-ja.conf', '/etc/fonts/conf.d/11-lcdfilter-default.conf', '/etc/fonts/conf.d/65-0-fonts-beng-extra.conf', '/etc/fonts/conf.d/70-fonts-noto-cjk.conf', '/etc/fonts/conf.d/64-15-laksaman.conf', '/etc/fonts/conf.d/67-smc-raghumalayalamsans.conf', '/etc/fonts/conf.d/60-latin.conf', '/etc/fonts/conf.d/45-generic.conf', '/etc/fonts/conf.d/67-smc-karumbi.conf', '/etc/fonts/conf.d/65-fonts-persian.conf', '/etc/fonts/conf.d/60-generic.conf', '/etc/fonts/conf.d/30-opensymbol.conf', '/etc/fonts/conf.d/65-0-fonts-deva-extra.conf', '/etc/fonts/conf.d/30-metric-aliases.conf', '/etc/fonts/conf.d/66-lohit-tamil.conf', '/etc/fonts/conf.d/64-23-tlwg-mono.conf', '/etc/fonts/conf.d/56-language-selector-ar.conf', '/etc/fonts/conf.d/50-user.conf', '/etc/fonts/conf.d/20-unhint-small-dejavu-sans-mono.conf', '/etc/fonts/conf.d/67-smc-chilanka.conf', '/etc/fonts/conf.d/61-urw-gothic.conf', '/etc/fonts/conf.d/65-0-smc-meera.conf', '/etc/fonts/conf.d/58-dejavu-lgc-serif.conf', '/etc/fonts/conf.d/64-02-tlwg-norasi.conf', '/etc/fonts/conf.d/65-khmer.conf', '/etc/fonts/conf.d/65-droid-sans-fallback.conf', '/etc/fonts/conf.d/89-tlwg-umpush-synthetic.conf', '/etc/fonts/conf.d/61-urw-fallback-generics.conf', '/etc/fonts/conf.d/67-smc-dyuthi.conf', '/etc/fonts/conf.d/64-01-tlwg-kinnari.conf', '/etc/fonts/conf.d/69-language-selector-zh-mo.conf', '/etc/fonts/conf.d/README', '/etc/fonts/conf.d/66-lohit-devanagari.conf', '/etc/fonts/conf.d/67-smc-keraleeyam.conf', '/etc/fonts/conf.d/65-0-fonts-guru-extra.conf', '/etc/fonts/conf.d/58-dejavu-lgc-sans.conf', '/etc/fonts/conf.d/20-unhint-small-dejavu-lgc-sans.conf', '/etc/fonts/conf.d/64-10-tlwg-loma.conf', '/etc/fonts/conf.d/69-language-selector-zh-tw.conf', '/etc/fonts/conf.d/69-language-selector-zh-cn.conf', '/etc/fonts/conf.d/61-urw-c059.conf', '/etc/fonts/conf.d/90-synthetic.conf', '/etc/fonts/conf.d/59-lohit-devanagari.conf', '/etc/fonts/conf.d/69-language-selector-zh-sg.conf', '/etc/fonts/conf.d/20-unhint-small-vera.conf', '/etc/fonts/conf.d/64-language-selector-prefer.conf', '/etc/fonts/conf.d/65-0-fonts-gubbi.conf', '/etc/fonts/conf.d/10-hinting-slight.conf', '/etc/fonts/conf.d/10-scale-bitmap-fonts.conf', '/etc/fonts/conf.d/65-0-smc-rachana.conf', '/etc/fonts/conf.d/66-lohit-tamil-classical.conf', '/etc/fonts/conf.d/61-urw-nimbus-roman.conf', '/etc/fonts/conf.d/66-lohit-gurmukhi.conf', '/etc/fonts/conf.d/70-no-bitmaps.conf', '/etc/fonts/conf.d/67-smc-uroob.conf', '/etc/fonts/conf.d/89-tlwg-laksaman-synthetic.conf', '/etc/fonts/conf.d/66-lohit-odia.conf', '/etc/fonts/conf.d/20-unhint-small-dejavu-sans.conf', '/etc/fonts/fonts.conf', '/etc/ucf.conf', '/etc/gtk-3.0', '/etc/gtk-3.0/im-multipress.conf', '/etc/gtk-3.0/settings.ini', '/etc/host.conf', '/etc/pki', '/etc/pki/fwupd-metadata', '/etc/pki/fwupd-metadata/GPG-KEY-Linux-Vendor-Firmware-Service', '/etc/pki/fwupd-metadata/GPG-KEY-Linux-Foundation-Metadata', '/etc/pki/fwupd-metadata/LVFS-CA.pem', '/etc/pki/fwupd', '/etc/pki/fwupd/GPG-KEY-Linux-Foundation-Firmware', '/etc/pki/fwupd/GPG-KEY-Linux-Vendor-Firmware-Service', '/etc/pki/fwupd/LVFS-CA.pem', '/etc/rsyslog.d', '/etc/rsyslog.d/50-default.conf', '/etc/rsyslog.d/20-ufw.conf', '/etc/ca-certificates.conf', '/etc/ModemManager', '/etc/ModemManager/fcc-unlock.d', '/etc/wpa_supplicant', '/etc/wpa_supplicant/functions.sh', '/etc/wpa_supplicant/ifupdown.sh', '/etc/wpa_supplicant/action_wpa.sh', '/etc/ubuntu-advantage', '/etc/ubuntu-advantage/uaclient.conf', '/etc/ubuntu-advantage/help_data.yaml', '/etc/modprobe.d', '/etc/modprobe.d/blacklist-firewire.conf', '/etc/modprobe.d/iwlwifi.conf', '/etc/modprobe.d/blacklist-framebuffer.conf', '/etc/modprobe.d/blacklist-oss.conf', '/etc/modprobe.d/blacklist-modem.conf', '/etc/modprobe.d/blacklist.conf', '/etc/modprobe.d/intel-microcode-blacklist.conf', '/etc/modprobe.d/blacklist-ath_pci.conf', '/etc/modprobe.d/blacklist-rare-network.conf', '/etc/modprobe.d/alsa-base.conf', '/etc/modprobe.d/amd64-microcode-blacklist.conf', '/etc/rmt', '/etc/machine-id', '/etc/X11', '/etc/X11/Xwrapper.config', '/etc/X11/XvMCConfig', '/etc/X11/xsm', '/etc/X11/xsm/system.xsm', '/etc/X11/xinit', '/etc/X11/xinit/xinputrc', '/etc/X11/xinit/xserverrc', '/etc/X11/xinit/xinitrc', '/etc/X11/cursors', '/etc/X11/cursors/redglass.theme', '/etc/X11/cursors/whiteglass.theme', '/etc/X11/cursors/core.theme', '/etc/X11/cursors/handhelds.theme', '/etc/X11/Xresources', '/etc/X11/Xresources/x11-common', '/etc/X11/Xsession', '/etc/X11/Xreset', '/etc/X11/Xsession.d', '/etc/X11/Xsession.d/35x11-common_xhost-local', '/etc/X11/Xsession.d/90x11-common_ssh-agent', '/etc/X11/Xsession.d/99x11-common_start', '/etc/X11/Xsession.d/90atk-adaptor', '/etc/X11/Xsession.d/90gpg-agent', '/etc/X11/Xsession.d/75dbus_dbus-launch', '/etc/X11/Xsession.d/40x11-common_xsessionrc', '/etc/X11/Xsession.d/60xbrlapi', '/etc/X11/Xsession.d/20x11-common_process-args', '/etc/X11/Xsession.d/60x11-common_localhost', '/etc/X11/Xsession.d/60x11-common_xdg_path', '/etc/X11/Xsession.d/90qt-a11y', '/etc/X11/Xsession.d/95dbus_update-activation-env', '/etc/X11/Xsession.d/20dbus_xdg-runtime', '/etc/X11/Xsession.d/70im-config_launch', '/etc/X11/Xsession.d/55gnome-session_gnomerc', '/etc/X11/Xsession.d/50x11-common_determine-startup', '/etc/X11/Xsession.d/30x11-common_xresources', '/etc/X11/Xsession.options', '/etc/X11/fonts', '/etc/X11/fonts/misc', '/etc/X11/fonts/misc/xfonts-base.alias', '/etc/X11/fonts/Type1', '/etc/X11/fonts/Type1/xfonts-scalable.scale', '/etc/X11/default-display-manager', '/etc/X11/Xreset.d', '/etc/X11/Xreset.d/README', '/etc/X11/rgb.txt', '/etc/X11/xkb', '/etc/X11/app-defaults', '/etc/X11/app-defaults/XLogo', '/etc/X11/app-defaults/Xditview', '/etc/X11/app-defaults/XClipboard', '/etc/X11/app-defaults/Xedit-color', '/etc/X11/app-defaults/XCalc-color', '/etc/X11/app-defaults/Viewres', '/etc/X11/app-defaults/Xman', '/etc/X11/app-defaults/Bitmap-color', '/etc/X11/app-defaults/Clock-color', '/etc/X11/app-defaults/XLogo-color', '/etc/X11/app-defaults/XSm', '/etc/X11/app-defaults/Xgc-color', '/etc/X11/app-defaults/XFontSel', '/etc/X11/app-defaults/XClock', '/etc/X11/app-defaults/Xmag', '/etc/X11/app-defaults/Xfd', '/etc/X11/app-defaults/Xvidtune', '/etc/X11/app-defaults/Xmessage', '/etc/X11/app-defaults/Xmessage-color', '/etc/X11/app-defaults/XCalc', '/etc/X11/app-defaults/XMore', '/etc/X11/app-defaults/XLoad', '/etc/X11/app-defaults/Xgc', '/etc/X11/app-defaults/Editres-color', '/etc/X11/app-defaults/Bitmap', '/etc/X11/app-defaults/Editres', '/etc/X11/app-defaults/XClock-color', '/etc/X11/app-defaults/Bitmap-nocase', '/etc/X11/app-defaults/Viewres-color', '/etc/X11/app-defaults/Xedit', '/etc/X11/app-defaults/XConsole', '/etc/X11/app-defaults/Xditview-chrtr', '/etc/manpath.config', '/etc/sysctl.conf', '/etc/.pwd.lock', '/etc/rpc', '/etc/environment.d', '/etc/environment.d/90qt-a11y.conf', '/etc/environment.d/90atk-adaptor.conf', '/etc/fwupd', '/etc/fwupd/uefi_capsule.conf', '/etc/fwupd/daemon.conf', '/etc/fwupd/thunderbolt.conf', '/etc/fwupd/redfish.conf', '/etc/fwupd/remotes.d', '/etc/fwupd/remotes.d/lvfs-testing.conf', '/etc/fwupd/remotes.d/vendor-directory.conf', '/etc/fwupd/remotes.d/dell-esrt.conf', '/etc/fwupd/remotes.d/vendor.conf', '/etc/fwupd/remotes.d/lvfs.conf', '/etc/gamemode.ini', '/etc/hosts.allow', '/etc/glvnd', '/etc/glvnd/egl_vendor.d', '/etc/gnome', '/etc/gnome/menus.blacklist', '/etc/gnome/defaults.list', '/etc/localtime', '/etc/network', '/etc/network/if-down.d', '/etc/network/if-down.d/wpasupplicant', '/etc/network/if-down.d/avahi-autoipd', '/etc/network/if-down.d/openvpn', '/etc/network/if-pre-up.d', '/etc/network/if-pre-up.d/wpasupplicant', '/etc/network/if-pre-up.d/wireless-tools', '/etc/network/if-up.d', '/etc/network/if-up.d/wpasupplicant', '/etc/network/if-up.d/avahi-autoipd', '/etc/network/if-up.d/openvpn', '/etc/network/if-post-down.d', '/etc/network/if-post-down.d/wpasupplicant', '/etc/network/if-post-down.d/wireless-tools', '/etc/network/if-post-down.d/avahi-daemon', '/etc/pam.d', '/etc/pam.d/common-account', '/etc/pam.d/ppp', '/etc/pam.d/gdm-launch-environment', '/etc/pam.d/su-l', '/etc/pam.d/chsh', '/etc/pam.d/runuser', '/etc/pam.d/gdm-autologin', '/etc/pam.d/sudo', '/etc/pam.d/common-session-noninteractive', '/etc/pam.d/vmtoolsd', '/etc/pam.d/other', '/etc/pam.d/common-auth', '/etc/pam.d/newusers', '/etc/pam.d/common-session', '/etc/pam.d/runuser-l', '/etc/pam.d/su', '/etc/pam.d/common-password', '/etc/pam.d/polkit-1', '/etc/pam.d/gdm-fingerprint', '/etc/pam.d/login', '/etc/pam.d/cups', '/etc/pam.d/chpasswd', '/etc/pam.d/systemd-user', '/etc/pam.d/passwd', '/etc/pam.d/chfn', '/etc/pam.d/gdm-password', '/etc/pam.d/cron', '/etc/udev', '/etc/udev/udev.conf', '/etc/udev/rules.d', '/etc/udev/rules.d/70-snap.snapd.rules', '/etc/udev/rules.d/70-snap.snap-store.rules', '/etc/udev/hwdb.d', '/etc/modules-load.d', '/etc/modules-load.d/modules.conf', '/etc/modules-load.d/cups-filters.conf', '/etc/alternatives', '/etc/alternatives/vi.ja.1.gz', '/etc/alternatives/lzcmp', '/etc/alternatives/pinentry', '/etc/alternatives/editor', '/etc/alternatives/nawk', '/etc/alternatives/unlzma.1.gz', '/etc/alternatives/telnet.1.gz', '/etc/alternatives/nawk.1.gz', '/etc/alternatives/awk', '/etc/alternatives/view.1.gz', '/etc/alternatives/from', '/etc/alternatives/default.plymouth', '/etc/alternatives/pager', '/etc/alternatives/arptables-restore', '/etc/alternatives/pinentry-x11.1.gz', '/etc/alternatives/ex.1.gz', '/etc/alternatives/infobrowser', '/etc/alternatives/view.pl.1.gz', '/etc/alternatives/lzegrep.1.gz', '/etc/alternatives/rcp.1.gz', '/etc/alternatives/rmt.8.gz', '/etc/alternatives/ip6tables', '/etc/alternatives/ftp.1.gz', '/etc/alternatives/w.1.gz', '/etc/alternatives/pftp', '/etc/alternatives/lzfgrep.1.gz', '/etc/alternatives/rlogin', '/etc/alternatives/x-window-manager.1.gz', '/etc/alternatives/ip6tables-restore', '/etc/alternatives/lzgrep.1.gz', '/etc/alternatives/view.ja.1.gz', '/etc/alternatives/lzgrep', '/etc/alternatives/ex.da.1.gz', '/etc/alternatives/rcp', '/etc/alternatives/ex.ja.1.gz', '/etc/alternatives/ex', '/etc/alternatives/cpp', '/etc/alternatives/netcat', '/etc/alternatives/vi.ru.1.gz', '/etc/alternatives/view.de.1.gz', '/etc/alternatives/rsh.1.gz', '/etc/alternatives/lzcat', '/etc/alternatives/vi.it.1.gz', '/etc/alternatives/lzdiff.1.gz', '/etc/alternatives/vi.pl.1.gz', '/etc/alternatives/ip6tables-save', '/etc/alternatives/infobrowser.1.gz', '/etc/alternatives/ftp', '/etc/alternatives/text.plymouth', '/etc/alternatives/view.ru.1.gz', '/etc/alternatives/rmt', '/etc/alternatives/iptables-save', '/etc/alternatives/iptables', '/etc/alternatives/rview', '/etc/alternatives/write.1.gz', '/etc/alternatives/lzma', '/etc/alternatives/gnome-www-browser', '/etc/alternatives/editor.1.gz', '/etc/alternatives/view.fr.1.gz', '/etc/alternatives/traceroute6.8.gz', '/etc/alternatives/lzfgrep', '/etc/alternatives/mt.1.gz', '/etc/alternatives/vi.da.1.gz', '/etc/alternatives/pinentry-x11', '/etc/alternatives/lzcat.1.gz', '/etc/alternatives/my.cnf', '/etc/alternatives/view.da.1.gz', '/etc/alternatives/pico', '/etc/alternatives/vi', '/etc/alternatives/from.1.gz', '/etc/alternatives/w', '/etc/alternatives/lzcmp.1.gz', '/etc/alternatives/lzma.1.gz', '/etc/alternatives/traceroute6', '/etc/alternatives/vtrgb', '/etc/alternatives/pftp.1.gz', '/etc/alternatives/lzdiff', '/etc/alternatives/lzless', '/etc/alternatives/arptables', '/etc/alternatives/pico.1.gz', '/etc/alternatives/gstreamer-codec-install', '/etc/alternatives/rsh', '/etc/alternatives/README', '/etc/alternatives/ex.de.1.gz', '/etc/alternatives/lzmore', '/etc/alternatives/ex.ru.1.gz', '/etc/alternatives/nc', '/etc/alternatives/builtins.7.gz', '/etc/alternatives/unlzma', '/etc/alternatives/view', '/etc/alternatives/x-session-manager.1.gz', '/etc/alternatives/lzegrep', '/etc/alternatives/x-session-manager', '/etc/alternatives/ex.it.1.gz', '/etc/alternatives/iptables-restore', '/etc/alternatives/ex.fr.1.gz', '/etc/alternatives/ex.pl.1.gz', '/etc/alternatives/telnet', '/etc/alternatives/awk.1.gz', '/etc/alternatives/rlogin.1.gz', '/etc/alternatives/vi.de.1.gz', '/etc/alternatives/vi.1.gz', '/etc/alternatives/write', '/etc/alternatives/mt', '/etc/alternatives/x-cursor-theme', '/etc/alternatives/vi.fr.1.gz', '/etc/alternatives/x-terminal-emulator.1.gz', '/etc/alternatives/gdm3-theme.gresource', '/etc/alternatives/x-window-manager', '/etc/alternatives/ebtables-restore', '/etc/alternatives/x-www-browser', '/etc/alternatives/ebtables-save', '/etc/alternatives/nc.1.gz', '/etc/alternatives/lzmore.1.gz', '/etc/alternatives/gnome-text-editor.1.gz', '/etc/alternatives/netrc.5.gz', '/etc/alternatives/netcat.1.gz', '/etc/alternatives/gnome-text-editor', '/etc/alternatives/x-terminal-emulator', '/etc/alternatives/ebtables', '/etc/alternatives/lzless.1.gz', '/etc/alternatives/pinentry.1.gz', '/etc/alternatives/pager.1.gz', '/etc/alternatives/newt-palette', '/etc/alternatives/view.it.1.gz', '/etc/alternatives/arptables-save', '/etc/passwd-', '/etc/pcmcia', '/etc/pcmcia/config.opts', '/etc/brltty', '/etc/brltty/Attributes', '/etc/brltty/Attributes/upper_lower.atb', '/etc/brltty/Attributes/left_right.atb', '/etc/brltty/Attributes/invleft_right.atb', '/etc/brltty/Text', '/etc/brltty/Text/se.ttb', '/etc/brltty/Text/brf.ttb', '/etc/brltty/Text/bn.ttb', '/etc/brltty/Text/kok.ttb', '/etc/brltty/Text/sd.ttb', '/etc/brltty/Text/ltr-dot8.tti', '/etc/brltty/Text/no-generic.ttb', '/etc/brltty/Text/pi.ttb', '/etc/brltty/Text/ascii-basic.tti', '/etc/brltty/Text/sa.ttb', '/etc/brltty/Text/et.ttb', '/etc/brltty/Text/gd.ttb', '/etc/brltty/Text/new.ttb', '/etc/brltty/Text/kannada.tti', '/etc/brltty/Text/is.ttb', '/etc/brltty/Text/en-nabcc.ttb', '/etc/brltty/Text/nl_BE.ttb', '/etc/brltty/Text/eo.ttb', '/etc/brltty/Text/ne.ttb', '/etc/brltty/Text/it.ttb', '/etc/brltty/Text/bra.ttb', '/etc/brltty/Text/awa.ttb', '/etc/brltty/Text/sv-1989.ttb', '/etc/brltty/Text/sat.ttb', '/etc/brltty/Text/sk.ttb', '/etc/brltty/Text/en_GB.ttb', '/etc/brltty/Text/ltr-alias.tti', '/etc/brltty/Text/fr.ttb', '/etc/brltty/Text/tamil.tti', '/etc/brltty/Text/dra.ttb', '/etc/brltty/Text/common.tti', '/etc/brltty/Text/punc-alternate.tti', '/etc/brltty/Text/en_US.ttb', '/etc/brltty/Text/ltr-tibetan.tti', '/etc/brltty/Text/cs.ttb', '/etc/brltty/Text/en.ttb', '/etc/brltty/Text/num-nemd8.tti', '/etc/brltty/Text/nl_NL.ttb', '/etc/brltty/Text/or.ttb', '/etc/brltty/Text/da-lt.ttb', '/etc/brltty/Text/nl.ttb', '/etc/brltty/Text/he.ttb', '/etc/brltty/Text/mt.ttb', '/etc/brltty/Text/mni.ttb', '/etc/brltty/Text/te.ttb', '/etc/brltty/Text/en-na-ascii.tti', '/etc/brltty/Text/kn.ttb', '/etc/brltty/Text/bh.ttb', '/etc/brltty/Text/cy.ttb', '/etc/brltty/Text/hi.ttb', '/etc/brltty/Text/num-nemeth.tti', '/etc/brltty/Text/greek.tti', '/etc/brltty/Text/fr-cbifs.ttb', '/etc/brltty/Text/ta.ttb', '/etc/brltty/Text/ctl-latin.tti', '/etc/brltty/Text/gurmukhi.tti', '/etc/brltty/Text/oriya.tti', '/etc/brltty/Text/da.ttb', '/etc/brltty/Text/de-chess.tti', '/etc/brltty/Text/ml.ttb', '/etc/brltty/Text/malayalam.tti', '/etc/brltty/Text/fr-2007.ttb', '/etc/brltty/Text/el.ttb', '/etc/brltty/Text/punc-tibetan.tti', '/etc/brltty/Text/fi.ttb', '/etc/brltty/Text/bg.ttb', '/etc/brltty/Text/devanagari.tti', '/etc/brltty/Text/gu.ttb', '/etc/brltty/Text/win-1252.tti', '/etc/brltty/Text/bengali.tti', '/etc/brltty/Text/punc-basic.tti', '/etc/brltty/Text/as.ttb', '/etc/brltty/Text/hy.ttb', '/etc/brltty/Text/nwc.ttb', '/etc/brltty/Text/no-oup.ttb', '/etc/brltty/Text/gujarati.tti', '/etc/brltty/Text/mi.ttb', '/etc/brltty/Text/sv.ttb', '/etc/brltty/Text/mwr.ttb', '/etc/brltty/Text/gon.ttb', '/etc/brltty/Text/pa.ttb', '/etc/brltty/Text/sv-1996.ttb', '/etc/brltty/Text/es.ttb', '/etc/brltty/Text/ltr-latin.tti', '/etc/brltty/Text/pl.ttb', '/etc/brltty/Text/kru.ttb', '/etc/brltty/Text/tr.ttb', '/etc/brltty/Text/ru.ttb', '/etc/brltty/Text/fr_FR.ttb', '/etc/brltty/Text/num-alias.tti', '/etc/brltty/Text/lt.ttb', '/etc/brltty/Text/en_CA.ttb', '/etc/brltty/Text/ar.ttb', '/etc/brltty/Text/lv.ttb', '/etc/brltty/Text/mun.ttb', '/etc/brltty/Text/mg.ttb', '/etc/brltty/Text/hr.ttb', '/etc/brltty/Text/hu.ttb', '/etc/brltty/Text/bo.ttb', '/etc/brltty/Text/en-chess.tti', '/etc/brltty/Text/sl.ttb', '/etc/brltty/Text/da-1252.ttb', '/etc/brltty/Text/alias.tti', '/etc/brltty/Text/no.ttb', '/etc/brltty/Text/num-dot8.tti', '/etc/brltty/Text/vi.ttb', '/etc/brltty/Text/pt.ttb', '/etc/brltty/Text/ltr-cyrillic.tti', '/etc/brltty/Text/uk.ttb', '/etc/brltty/Text/mr.ttb', '/etc/brltty/Text/sw.ttb', '/etc/brltty/Text/num-french.tti', '/etc/brltty/Text/ro.ttb', '/etc/brltty/Text/boxes.tti', '/etc/brltty/Text/fr-vs.ttb', '/etc/brltty/Text/fr_CA.ttb', '/etc/brltty/Text/telugu.tti', '/etc/brltty/Text/blocks.tti', '/etc/brltty/Text/kha.ttb', '/etc/brltty/Text/num-dot6.tti', '/etc/brltty/Text/ga.ttb', '/etc/brltty/Text/de.ttb', '/etc/brltty/Keyboard', '/etc/brltty/Keyboard/braille.ktb', '/etc/brltty/Keyboard/laptop.ktb', '/etc/brltty/Keyboard/desktop.ktb', '/etc/brltty/Keyboard/braille.kti', '/etc/brltty/Keyboard/desktop.kti', '/etc/brltty/Keyboard/kp_say.kti', '/etc/brltty/Keyboard/kp_speak.kti', '/etc/brltty/Keyboard/keypad.ktb', '/etc/brltty/Keyboard/sun_type6.ktb', '/etc/brltty/Contraction', '/etc/brltty/Contraction/zh-tw.ctb', '/etc/brltty/Contraction/mun.ctb', '/etc/brltty/Contraction/th.ctb', '/etc/brltty/Contraction/fr-abrege.ctb', '/etc/brltty/Contraction/ko-g1.ctb', '/etc/brltty/Contraction/id.ctb', '/etc/brltty/Contraction/spaces.cti', '/etc/brltty/Contraction/de-kurzschrift.ctb', '/etc/brltty/Contraction/de-basis.ctb', '/etc/brltty/Contraction/de-kurzschrift-2015.ctb', '/etc/brltty/Contraction/mg.ctb', '/etc/brltty/Contraction/de-kurzschrift-1998.ctb', '/etc/brltty/Contraction/letters-latin.cti', '/etc/brltty/Contraction/ny.ctb', '/etc/brltty/Contraction/af.ctb', '/etc/brltty/Contraction/es.ctb', '/etc/brltty/Contraction/ipa.ctb', '/etc/brltty/Contraction/en-us-g2.ctb', '/etc/brltty/Contraction/de-kurzschrift-wort.cti', '/etc/brltty/Contraction/nl.ctb', '/etc/brltty/Contraction/lt.ctb', '/etc/brltty/Contraction/am.ctb', '/etc/brltty/Contraction/ha.ctb', '/etc/brltty/Contraction/fr-integral.ctb', '/etc/brltty/Contraction/zh-tw-ucb.ctb', '/etc/brltty/Contraction/ko-g2.ctb', '/etc/brltty/Contraction/latex-access.ctb', '/etc/brltty/Contraction/en-ueb-g2.ctb', '/etc/brltty/Contraction/si.ctb', '/etc/brltty/Contraction/sw.ctb', '/etc/brltty/Contraction/zu.ctb', '/etc/brltty/Contraction/ko.ctb', '/etc/brltty/Contraction/ja.ctb', '/etc/brltty/Contraction/pt.ctb', '/etc/brltty/Contraction/nabcc.cti', '/etc/brltty/Contraction/de-vollschrift.ctb', '/etc/brltty/Contraction/countries.cti', '/etc/brltty/Input', '/etc/brltty/Input/vr', '/etc/brltty/Input/vr/all.txt', '/etc/brltty/Input/vo', '/etc/brltty/Input/vo/bp.ktb', '/etc/brltty/Input/vo/all.ktb', '/etc/brltty/Input/vo/all.kti', '/etc/brltty/Input/bp', '/etc/brltty/Input/bp/all.kti', '/etc/brltty/Input/eu', '/etc/brltty/Input/eu/clio.ktb', '/etc/brltty/Input/eu/iris.ktb', '/etc/brltty/Input/eu/esys_large.ktb', '/etc/brltty/Input/eu/esys_medium.ktb', '/etc/brltty/Input/eu/common.kti', '/etc/brltty/Input/eu/all.txt', '/etc/brltty/Input/eu/sw56.kti', '/etc/brltty/Input/eu/routing.kti', '/etc/brltty/Input/eu/esys_small.ktb', '/etc/brltty/Input/eu/braille.kti', '/etc/brltty/Input/eu/esytime.ktb', '/etc/brltty/Input/eu/joysticks.kti', '/etc/brltty/Input/eu/sw34.kti', '/etc/brltty/Input/eu/sw12.kti', '/etc/brltty/Input/bd', '/etc/brltty/Input/bd/all.txt', '/etc/brltty/Input/lt', '/etc/brltty/Input/lt/all.txt', '/etc/brltty/Input/hd', '/etc/brltty/Input/hd/mbl.ktb', '/etc/brltty/Input/hd/pfl.ktb', '/etc/brltty/Input/ce', '/etc/brltty/Input/ce/novem.ktb', '/etc/brltty/Input/ce/all.ktb', '/etc/brltty/Input/menu.kti', '/etc/brltty/Input/lb', '/etc/brltty/Input/lb/all.txt', '/etc/brltty/Input/ba', '/etc/brltty/Input/ba/all.txt', '/etc/brltty/Input/sk', '/etc/brltty/Input/sk/bdp.ktb', '/etc/brltty/Input/sk/ntk.ktb', '/etc/brltty/Input/ir', '/etc/brltty/Input/ir/pc.ktb', '/etc/brltty/Input/ir/all.kti', '/etc/brltty/Input/ir/brl.ktb', '/etc/brltty/Input/vd', '/etc/brltty/Input/vd/all.txt', '/etc/brltty/Input/hw', '/etc/brltty/Input/hw/BI32.ktb', '/etc/brltty/Input/hw/joystick.kti', '/etc/brltty/Input/hw/touch.ktb', '/etc/brltty/Input/hw/BI14.ktb', '/etc/brltty/Input/hw/BI40.ktb', '/etc/brltty/Input/hw/braille.kti', '/etc/brltty/Input/hw/B80.ktb', '/etc/brltty/Input/hw/command.kti', '/etc/brltty/Input/hw/thumb.kti', '/etc/brltty/Input/fs', '/etc/brltty/Input/fs/common.kti', '/etc/brltty/Input/fs/focus_basic.kti', '/etc/brltty/Input/fs/pacmate.ktb', '/etc/brltty/Input/fs/focus_large.ktb', '/etc/brltty/Input/fs/focus_small.ktb', '/etc/brltty/Input/fs/bumpers.kti', '/etc/brltty/Input/fs/rockers.kti', '/etc/brltty/Input/fs/focus_basic.ktb', '/etc/brltty/Input/cb', '/etc/brltty/Input/cb/all.ktb', '/etc/brltty/Input/chords.kti', '/etc/brltty/Input/tt', '/etc/brltty/Input/tt/all.txt', '/etc/brltty/Input/xw', '/etc/brltty/Input/bn', '/etc/brltty/Input/bn/input.kti', '/etc/brltty/Input/bn/all.ktb', '/etc/brltty/Input/ec', '/etc/brltty/Input/ec/spanish.txt', '/etc/brltty/Input/ec/all.txt', '/etc/brltty/Input/ts', '/etc/brltty/Input/ts/nav40.ktb', '/etc/brltty/Input/ts/nav20.ktb', '/etc/brltty/Input/ts/pb_large.kti', '/etc/brltty/Input/ts/nav_small.kti', '/etc/brltty/Input/ts/pb40.ktb', '/etc/brltty/Input/ts/routing.kti', '/etc/brltty/Input/ts/pb80.ktb', '/etc/brltty/Input/ts/pb_small.kti', '/etc/brltty/Input/ts/nav_large.kti', '/etc/brltty/Input/ts/pb65.ktb', '/etc/brltty/Input/ts/pb.kti', '/etc/brltty/Input/ts/nav.kti', '/etc/brltty/Input/ts/nav80.ktb', '/etc/brltty/Input/mn', '/etc/brltty/Input/mn/all.txt', '/etc/brltty/Input/mb', '/etc/brltty/Input/mb/all.txt', '/etc/brltty/Input/bl', '/etc/brltty/Input/bl/40_m20_m40.txt', '/etc/brltty/Input/bl/18.txt', '/etc/brltty/Input/ic', '/etc/brltty/Input/ic/all.ktb', '/etc/brltty/Input/ht', '/etc/brltty/Input/ht/bs80.ktb', '/etc/brltty/Input/ht/mdlr.ktb', '/etc/brltty/Input/ht/alo.ktb', '/etc/brltty/Input/ht/dots.kti', '/etc/brltty/Input/ht/bs.kti', '/etc/brltty/Input/ht/joystick.kti', '/etc/brltty/Input/ht/me.kti', '/etc/brltty/Input/ht/ac4.ktb', '/etc/brltty/Input/ht/cb40.ktb', '/etc/brltty/Input/ht/easy.ktb', '/etc/brltty/Input/ht/rockers.kti', '/etc/brltty/Input/ht/input.kti', '/etc/brltty/Input/ht/bs40.ktb', '/etc/brltty/Input/ht/bb.ktb', '/etc/brltty/Input/ht/me88.ktb', '/etc/brltty/Input/ht/brln.ktb', '/etc/brltty/Input/ht/ab40.ktb', '/etc/brltty/Input/ht/mc88.ktb', '/etc/brltty/Input/ht/me64.ktb', '/etc/brltty/Input/ht/keypad.kti', '/etc/brltty/Input/ht/wave.ktb', '/etc/brltty/Input/ht/as40.ktb', '/etc/brltty/Input/ht/bkwm.ktb', '/etc/brltty/Input/al', '/etc/brltty/Input/al/el.ktb', '/etc/brltty/Input/al/abt_large.ktb', '/etc/brltty/Input/al/bc680.ktb', '/etc/brltty/Input/al/sat_large.ktb', '/etc/brltty/Input/al/abt_basic.kti', '/etc/brltty/Input/al/bc-smartpad.kti', '/etc/brltty/Input/al/bc-etouch.kti', '/etc/brltty/Input/al/sat_extra.kti', '/etc/brltty/Input/al/sat_small.ktb', '/etc/brltty/Input/al/sat_basic.kti', '/etc/brltty/Input/al/bc-thumb.kti', '/etc/brltty/Input/al/bc.kti', '/etc/brltty/Input/al/abt_extra.kti', '/etc/brltty/Input/al/bc640.ktb', '/etc/brltty/Input/al/voyager.ktb', '/etc/brltty/Input/al/abt_small.ktb', '/etc/brltty/Input/vs', '/etc/brltty/Input/vs/all.txt', '/etc/brltty/Input/pg', '/etc/brltty/Input/pg/all.ktb', '/etc/brltty/Input/md', '/etc/brltty/Input/md/common.kti', '/etc/brltty/Input/md/kbd.ktb', '/etc/brltty/Input/md/default.ktb', '/etc/brltty/Input/md/keyboard.kti', '/etc/brltty/Input/md/fkeys.kti', '/etc/brltty/Input/md/status.kti', '/etc/brltty/Input/md/fk.ktb', '/etc/brltty/Input/md/fk_s.ktb', '/etc/brltty/Input/toggle.kti', '/etc/brltty/Input/tn', '/etc/brltty/Input/tn/all.txt', '/etc/brltty/Input/mt', '/etc/brltty/Input/mt/bd1_3s.ktb', '/etc/brltty/Input/mt/bd1_6.ktb', '/etc/brltty/Input/mt/bd1_6.kti', '/etc/brltty/Input/mt/bd1_3.ktb', '/etc/brltty/Input/mt/status.kti', '/etc/brltty/Input/mt/bd1_6s.ktb', '/etc/brltty/Input/mt/bd1_3.kti', '/etc/brltty/Input/mt/bd2.ktb', '/etc/brltty/Input/bm', '/etc/brltty/Input/bm/vertical.kti', '/etc/brltty/Input/bm/vk.ktb', '/etc/brltty/Input/bm/pro.ktb', '/etc/brltty/Input/bm/routing6.kti', '/etc/brltty/Input/bm/default.ktb', '/etc/brltty/Input/bm/dm80p.ktb', '/etc/brltty/Input/bm/b2g.ktb', '/etc/brltty/Input/bm/d6.kti', '/etc/brltty/Input/bm/ultra.ktb', '/etc/brltty/Input/bm/inka.ktb', '/etc/brltty/Input/bm/connect.ktb', '/etc/brltty/Input/bm/front6.kti', '/etc/brltty/Input/bm/conny.ktb', '/etc/brltty/Input/bm/routing.kti', '/etc/brltty/Input/bm/b9b10.kti', '/etc/brltty/Input/bm/b9b11b10.kti', '/etc/brltty/Input/bm/keyboard.kti', '/etc/brltty/Input/bm/v40.ktb', '/etc/brltty/Input/bm/display6.kti', '/etc/brltty/Input/bm/horizontal.kti', '/etc/brltty/Input/bm/pronto.ktb', '/etc/brltty/Input/bm/command.kti', '/etc/brltty/Input/bm/status.kti', '/etc/brltty/Input/bm/front10.kti', '/etc/brltty/Input/bm/sv.ktb', '/etc/brltty/Input/bm/pv.ktb', '/etc/brltty/Input/bm/wheels.kti', '/etc/brltty/Input/bm/orbit.ktb', '/etc/brltty/Input/bm/routing7.kti', '/etc/brltty/Input/bm/rb.ktb', '/etc/brltty/Input/bm/display7.kti', '/etc/brltty/Input/bm/v80.ktb', '/etc/brltty/Input/pm', '/etc/brltty/Input/pm/front9.kti', '/etc/brltty/Input/pm/elba_20.ktb', '/etc/brltty/Input/pm/el70s.ktb', '/etc/brltty/Input/pm/el40c.ktb', '/etc/brltty/Input/pm/status4.kti', '/etc/brltty/Input/pm/el80_ii.ktb', '/etc/brltty/Input/pm/status20.kti', '/etc/brltty/Input/pm/status13.kti', '/etc/brltty/Input/pm/el_2d_66.ktb', '/etc/brltty/Input/pm/el66s.ktb', '/etc/brltty/Input/pm/trio.ktb', '/etc/brltty/Input/pm/el_40_p.ktb', '/etc/brltty/Input/pm/el40s.ktb', '/etc/brltty/Input/pm/status0.kti', '/etc/brltty/Input/pm/elb_tr_20.ktb', '/etc/brltty/Input/pm/switches.kti', '/etc/brltty/Input/pm/status22.kti', '/etc/brltty/Input/pm/routing.kti', '/etc/brltty/Input/pm/keys.kti', '/etc/brltty/Input/pm/elb_tr_32.ktb', '/etc/brltty/Input/pm/keyboard.kti', '/etc/brltty/Input/pm/2d_s.ktb', '/etc/brltty/Input/pm/c_486.ktb', '/etc/brltty/Input/pm/el60c.ktb', '/etc/brltty/Input/pm/front13.kti', '/etc/brltty/Input/pm/el_2d_80.ktb', '/etc/brltty/Input/pm/el80c.ktb', '/etc/brltty/Input/pm/elba_32.ktb', '/etc/brltty/Input/pm/bar.kti', '/etc/brltty/Input/pm/c.ktb', '/etc/brltty/Input/pm/status2.kti', '/etc/brltty/Input/pm/el_80.ktb', '/etc/brltty/Input/pm/ib_80.ktb', '/etc/brltty/Input/pm/el80s.ktb', '/etc/brltty/Input/pm/el_2d_40.ktb', '/etc/brltty/Input/pm/el2d_80s.ktb', '/etc/brltty/Input/pm/2d_l.ktb', '/etc/brltty/Input/pm/live.ktb', '/etc/brltty/Input/np', '/etc/brltty/Input/np/all.ktb', '/etc/brltty/Input/hm', '/etc/brltty/Input/hm/contexts.kti', '/etc/brltty/Input/hm/edge.ktb', '/etc/brltty/Input/hm/common.kti', '/etc/brltty/Input/hm/pan.ktb', '/etc/brltty/Input/hm/f14.kti', '/etc/brltty/Input/hm/scroll.ktb', '/etc/brltty/Input/hm/scroll.kti', '/etc/brltty/Input/hm/qwerty.ktb', '/etc/brltty/Input/hm/f18.kti', '/etc/brltty/Input/hm/braille.kti', '/etc/brltty/Input/hm/fnkey.kti', '/etc/brltty/Input/hm/letters.kti', '/etc/brltty/Input/hm/beetle.ktb', '/etc/brltty/Input/hm/sync.ktb', '/etc/brltty/Input/hm/pan.kti', '/etc/brltty/Input/hm/right.kti', '/etc/brltty/Input/hm/qwerty.kti', '/etc/brltty/Input/hm/left.kti', '/etc/brltty/Input/bg', '/etc/brltty/Input/bg/all.ktb', '/etc/brltty/Input/mm', '/etc/brltty/Input/mm/common.kti', '/etc/brltty/Input/mm/pocket.ktb', '/etc/brltty/Input/mm/smart.ktb', '/etc/brltty/Input/at', '/etc/brltty/Input/at/all.ktb', '/etc/mime.types', '/etc/kerneloops.conf', '/etc/mysql', '/etc/mysql/conf.d', '/etc/mysql/conf.d/mysql.cnf', '/etc/mysql/conf.d/mysqldump.cnf', '/etc/mysql/my.cnf', '/etc/mysql/my.cnf.fallback', '/etc/vtrgb', '/etc/sane.d', '/etc/sane.d/hp.conf', '/etc/sane.d/pie.conf', '/etc/sane.d/snapscan.conf', '/etc/sane.d/epson2.conf', '/etc/sane.d/canon.conf', '/etc/sane.d/gphoto2.conf', '/etc/sane.d/dmc.conf', '/etc/sane.d/abaton.conf', '/etc/sane.d/p5.conf', '/etc/sane.d/genesys.conf', '/etc/sane.d/dc240.conf', '/etc/sane.d/epjitsu.conf', '/etc/sane.d/fujitsu.conf', '/etc/sane.d/s9036.conf', '/etc/sane.d/lexmark.conf', '/etc/sane.d/bh.conf', '/etc/sane.d/matsushita.conf', '/etc/sane.d/ricoh.conf', '/etc/sane.d/leo.conf', '/etc/sane.d/plustek_pp.conf', '/etc/sane.d/dll.d', '/etc/sane.d/dll.d/hplip', '/etc/sane.d/saned.conf', '/etc/sane.d/ibm.conf', '/etc/sane.d/umax_pp.conf', '/etc/sane.d/sceptre.conf', '/etc/sane.d/hpsj5s.conf', '/etc/sane.d/qcam.conf', '/etc/sane.d/cardscan.conf', '/etc/sane.d/epson.conf', '/etc/sane.d/gt68xx.conf', '/etc/sane.d/avision.conf', '/etc/sane.d/teco3.conf', '/etc/sane.d/net.conf', '/etc/sane.d/canon_dr.conf', '/etc/sane.d/apple.conf', '/etc/sane.d/coolscan.conf', '/etc/sane.d/hp4200.conf', '/etc/sane.d/sm3840.conf', '/etc/sane.d/agfafocus.conf', '/etc/sane.d/kvs1025.conf', '/etc/sane.d/escl.conf', '/etc/sane.d/dell1600n_net.conf', '/etc/sane.d/hp3900.conf', '/etc/sane.d/hs2p.conf', '/etc/sane.d/stv680.conf', '/etc/sane.d/nec.conf', '/etc/sane.d/canon_pp.conf', '/etc/sane.d/pixma.conf', '/etc/sane.d/dll.conf', '/etc/sane.d/ma1509.conf', '/etc/sane.d/kodakaio.conf', '/etc/sane.d/dc25.conf', '/etc/sane.d/magicolor.conf', '/etc/sane.d/microtek2.conf', '/etc/sane.d/sharp.conf', '/etc/sane.d/microtek.conf', '/etc/sane.d/umax.conf', '/etc/sane.d/mustek_usb.conf', '/etc/sane.d/mustek.conf', '/etc/sane.d/teco2.conf', '/etc/sane.d/canon630u.conf', '/etc/sane.d/coolscan2.conf', '/etc/sane.d/epsonds.conf', '/etc/sane.d/artec.conf', '/etc/sane.d/xerox_mfp.conf', '/etc/sane.d/pieusb.conf', '/etc/sane.d/sp15c.conf', '/etc/sane.d/test.conf', '/etc/sane.d/rts8891.conf', '/etc/sane.d/st400.conf', '/etc/sane.d/dc210.conf', '/etc/sane.d/umax1220u.conf', '/etc/sane.d/artec_eplus48u.conf', '/etc/sane.d/u12.conf', '/etc/sane.d/tamarack.conf', '/etc/sane.d/kodak.conf', '/etc/sane.d/coolscan3.conf', '/etc/sane.d/mustek_pp.conf', '/etc/sane.d/hp5400.conf', '/etc/sane.d/teco1.conf', '/etc/sane.d/plustek.conf', '/etc/environment', '/etc/polkit-1', '/etc/polkit-1/localauthority.conf.d', '/etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf', '/etc/polkit-1/localauthority.conf.d/50-localauthority.conf', '/etc/polkit-1/localauthority', '/etc/polkit-1/localauthority/90-mandatory.d', '/etc/polkit-1/localauthority/20-org.d', '/etc/polkit-1/localauthority/30-site.d', '/etc/polkit-1/localauthority/10-vendor.d', '/etc/polkit-1/localauthority/50-local.d', '/etc/crontab', '/etc/gss', '/etc/gss/mech.d', '/etc/debconf.conf', '/etc/openvpn', '/etc/openvpn/server', '/etc/openvpn/client', '/etc/openvpn/update-resolv-conf', '/etc/group', '/etc/fprintd.conf', '/etc/cracklib', '/etc/cracklib/cracklib.conf', '/etc/kernel', '/etc/kernel/postrm.d', '/etc/kernel/postrm.d/initramfs-tools', '/etc/kernel/postrm.d/zz-update-grub', '/etc/kernel/preinst.d', '/etc/kernel/preinst.d/intel-microcode', '/etc/kernel/postinst.d', '/etc/kernel/postinst.d/unattended-upgrades', '/etc/kernel/postinst.d/xx-update-initrd-links', '/etc/kernel/postinst.d/update-notifier', '/etc/kernel/postinst.d/initramfs-tools', '/etc/kernel/postinst.d/zz-update-grub', '/etc/kernel/install.d', '/etc/wgetrc', '/etc/ca-certificates', '/etc/ca-certificates/update.d', '/etc/python3.8', '/etc/python3.8/sitecustomize.py', '/etc/cups', '/etc/cups/cupsd.conf', '/etc/cups/subscriptions.conf.O', '/etc/cups/raw.types', '/etc/cups/cups-browsed.conf', '/etc/cups/ppd', '/etc/cups/snmp.conf', '/etc/cups/interfaces', '/etc/cups/subscriptions.conf', '/etc/cups/raw.convs', '/etc/cups/cups-files.conf', '/etc/cups/ssl', '/etc/protocols', '/etc/emacs', '/etc/emacs/site-start.d', '/etc/emacs/site-start.d/50dictionaries-common.el', '/etc/gdb', '/etc/gdb/gdbinit', '/etc/fstab', '/etc/group-', '/etc/brltty.conf', '/etc/lsb-release', '/etc/papersize', '/etc/anacrontab', '/etc/default', '/etc/default/locale', '/etc/default/anacron', '/etc/default/crda', '/etc/default/ufw', '/etc/default/kerneloops', '/etc/default/console-setup', '/etc/default/grub.d', '/etc/default/grub.d/init-select.cfg', '/etc/default/rsync', '/etc/default/grub', '/etc/default/nss', '/etc/default/keyboard', '/etc/default/dbus', '/etc/default/useradd', '/etc/default/bsdmainutils', '/etc/default/intel-microcode', '/etc/default/alsa', '/etc/default/avahi-daemon', '/etc/default/acpid', '/etc/default/irqbalance', '/etc/default/openvpn', '/etc/default/saned', '/etc/default/im-config', '/etc/default/apport', '/etc/default/networkd-dispatcher', '/etc/default/cron', '/etc/default/acpi-support', '/etc/default/amd64-microcode', '/etc/mailcap', '/etc/usb_modeswitch.d', '/etc/profile.d', '/etc/profile.d/vte-2.91.sh', '/etc/profile.d/01-locale-fix.sh', '/etc/profile.d/apps-bin-path.sh', '/etc/profile.d/vte.csh', '/etc/profile.d/bash_completion.sh', '/etc/profile.d/im-config_wayland.sh', '/etc/profile.d/cedilla-portuguese.sh', '/etc/profile.d/xdg_dirs_desktop_session.sh', '/etc/gtk-2.0', '/etc/gtk-2.0/im-multipress.conf', '/etc/locale.gen', '/etc/skel', '/etc/skel/.bash_logout', '/etc/skel/.profile', '/etc/skel/.bashrc', '/etc/apparmor', '/etc/apparmor/init', '/etc/apparmor/init/network-interface-security', '/etc/apparmor/init/network-interface-security/sbin.dhclient', '/etc/apparmor/parser.conf', '/etc/kernel-img.conf', '/etc/fuse.conf', '/etc/libnl-3', '/etc/libnl-3/classid', '/etc/libnl-3/pktloc', '/etc/subuid', '/etc/bindresvport.blacklist', '/etc/systemd', '/etc/systemd/sleep.conf', '/etc/systemd/system.conf', '/etc/systemd/user', '/etc/systemd/user/default.target.wants', '/etc/systemd/user/default.target.wants/tracker-extract.service', '/etc/systemd/user/default.target.wants/pulseaudio.service', '/etc/systemd/user/default.target.wants/tracker-miner-fs.service', '/etc/systemd/user/default.target.wants/ubuntu-report.path', '/etc/systemd/user/sockets.target.wants', '/etc/systemd/user/sockets.target.wants/gpg-agent.socket', '/etc/systemd/user/sockets.target.wants/pk-debconf-helper.socket', '/etc/systemd/user/sockets.target.wants/dirmngr.socket', '/etc/systemd/user/sockets.target.wants/gpg-agent-browser.socket', '/etc/systemd/user/sockets.target.wants/gpg-agent-ssh.socket', '/etc/systemd/user/sockets.target.wants/pulseaudio.socket', '/etc/systemd/user/sockets.target.wants/gpg-agent-extra.socket', '/etc/systemd/network', '/etc/systemd/resolved.conf', '/etc/systemd/timesyncd.conf', '/etc/systemd/system', '/etc/systemd/system/sleep.target.wants', '/etc/systemd/system/sleep.target.wants/grub-initrd-fallback.service', '/etc/systemd/system/sleep.target.wants/grub-common.service', '/etc/systemd/system/snap-gnome\\x2d3\\x2d38\\x2d2004-119.mount', '/etc/systemd/system/dbus-org.bluez.service', '/etc/systemd/system/printer.target.wants', '/etc/systemd/system/printer.target.wants/cups.service', '/etc/systemd/system/emergency.target.wants', '/etc/systemd/system/emergency.target.wants/grub-initrd-fallback.service', '/etc/systemd/system/display-manager.service', '/etc/systemd/system/vmtoolsd.service', '/etc/systemd/system/snap-snap\\x2dstore-558.mount', '/etc/systemd/system/oem-config.service.wants', '/etc/systemd/system/oem-config.service.wants/gpu-manager.service', '/etc/systemd/system/snap-gnome\\x2d3\\x2d38\\x2d2004-115.mount', '/etc/systemd/system/snap-snap\\x2dstore-638.mount', '/etc/systemd/system/graphical.target.wants', '/etc/systemd/system/graphical.target.wants/switcheroo-control.service', '/etc/systemd/system/graphical.target.wants/accounts-daemon.service', '/etc/systemd/system/graphical.target.wants/udisks2.service', '/etc/systemd/system/dbus-org.freedesktop.resolve1.service', '/etc/systemd/system/final.target.wants', '/etc/systemd/system/final.target.wants/snapd.system-shutdown.service', '/etc/systemd/system/snap-snapd-17883.mount', '/etc/systemd/system/sysinit.target.wants', '/etc/systemd/system/sysinit.target.wants/systemd-pstore.service', '/etc/systemd/system/sysinit.target.wants/keyboard-setup.service', '/etc/systemd/system/sysinit.target.wants/setvtrgb.service', '/etc/systemd/system/sysinit.target.wants/systemd-timesyncd.service', '/etc/systemd/system/sysinit.target.wants/apparmor.service', '/etc/systemd/system/dbus-org.freedesktop.thermald.service', '/etc/systemd/system/paths.target.wants', '/etc/systemd/system/paths.target.wants/apport-autoreport.path', '/etc/systemd/system/paths.target.wants/acpid.path', '/etc/systemd/system/dbus-org.freedesktop.Avahi.service', '/etc/systemd/system/syslog.service', '/etc/systemd/system/cloud-final.service.wants', '/etc/systemd/system/cloud-final.service.wants/snapd.seeded.service', '/etc/systemd/system/dbus-org.freedesktop.ModemManager1.service', '/etc/systemd/system/snap-gtk\\x2dcommon\\x2dthemes-1535.mount', '/etc/systemd/system/multi-user.target.wants', '/etc/systemd/system/multi-user.target.wants/rsync.service', '/etc/systemd/system/multi-user.target.wants/networkd-dispatcher.service', '/etc/systemd/system/multi-user.target.wants/snapd.service', '/etc/systemd/system/multi-user.target.wants/snap-gnome\\x2d3\\x2d38\\x2d2004-119.mount', '/etc/systemd/system/multi-user.target.wants/rsyslog.service', '/etc/systemd/system/multi-user.target.wants/ubuntu-advantage.service', '/etc/systemd/system/multi-user.target.wants/run-vmblock\\x2dfuse.mount', '/etc/systemd/system/multi-user.target.wants/remote-fs.target', '/etc/systemd/system/multi-user.target.wants/pppd-dns.service', '/etc/systemd/system/multi-user.target.wants/snapd.autoimport.service', '/etc/systemd/system/multi-user.target.wants/open-vm-tools.service', '/etc/systemd/system/multi-user.target.wants/cups-browsed.service', '/etc/systemd/system/multi-user.target.wants/snapd.apparmor.service', '/etc/systemd/system/multi-user.target.wants/snap-snap\\x2dstore-558.mount', '/etc/systemd/system/multi-user.target.wants/snapd.core-fixup.service', '/etc/systemd/system/multi-user.target.wants/irqbalance.service', '/etc/systemd/system/multi-user.target.wants/snap-gnome\\x2d3\\x2d38\\x2d2004-115.mount', '/etc/systemd/system/multi-user.target.wants/kerneloops.service', '/etc/systemd/system/multi-user.target.wants/snap-snap\\x2dstore-638.mount', '/etc/systemd/system/multi-user.target.wants/secureboot-db.service', '/etc/systemd/system/multi-user.target.wants/ua-reboot-cmds.service', '/etc/systemd/system/multi-user.target.wants/snap-snapd-17883.mount', '/etc/systemd/system/multi-user.target.wants/wpa_supplicant.service', '/etc/systemd/system/multi-user.target.wants/cron.service', '/etc/systemd/system/multi-user.target.wants/snapd.recovery-chooser-trigger.service', '/etc/systemd/system/multi-user.target.wants/openvpn.service', '/etc/systemd/system/multi-user.target.wants/whoopsie.service', '/etc/systemd/system/multi-user.target.wants/dmesg.service', '/etc/systemd/system/multi-user.target.wants/snap-gtk\\x2dcommon\\x2dthemes-1535.mount', '/etc/systemd/system/multi-user.target.wants/cups.path', '/etc/systemd/system/multi-user.target.wants/unattended-upgrades.service', '/etc/systemd/system/multi-user.target.wants/thermald.service', '/etc/systemd/system/multi-user.target.wants/avahi-daemon.service', '/etc/systemd/system/multi-user.target.wants/systemd-resolved.service', '/etc/systemd/system/multi-user.target.wants/ModemManager.service', '/etc/systemd/system/multi-user.target.wants/snap-bare-5.mount', '/etc/systemd/system/multi-user.target.wants/anacron.service', '/etc/systemd/system/multi-user.target.wants/snapd.seeded.service', '/etc/systemd/system/multi-user.target.wants/grub-initrd-fallback.service', '/etc/systemd/system/multi-user.target.wants/console-setup.service', '/etc/systemd/system/multi-user.target.wants/snap-core20-1738.mount', '/etc/systemd/system/multi-user.target.wants/NetworkManager.service', '/etc/systemd/system/multi-user.target.wants/grub-common.service', '/etc/systemd/system/multi-user.target.wants/snap-core20-1611.mount', '/etc/systemd/system/multi-user.target.wants/ondemand.service', '/etc/systemd/system/multi-user.target.wants/ufw.service', '/etc/systemd/system/default.target.wants', '/etc/systemd/system/default.target.wants/e2scrub_reap.service', '/etc/systemd/system/default.target.wants/snap-gnome\\x2d3\\x2d38\\x2d2004-119.mount', '/etc/systemd/system/default.target.wants/snap-snap\\x2dstore-638.mount', '/etc/systemd/system/default.target.wants/snap-core20-1738.mount', '/etc/systemd/system/timers.target.wants', '/etc/systemd/system/timers.target.wants/fstrim.timer', '/etc/systemd/system/timers.target.wants/e2scrub_all.timer', '/etc/systemd/system/timers.target.wants/snapd.snap-repair.timer', '/etc/systemd/system/timers.target.wants/apt-daily-upgrade.timer', '/etc/systemd/system/timers.target.wants/motd-news.timer', '/etc/systemd/system/timers.target.wants/anacron.timer', '/etc/systemd/system/timers.target.wants/fwupd-refresh.timer', '/etc/systemd/system/timers.target.wants/apt-daily.timer', '/etc/systemd/system/timers.target.wants/ua-timer.timer', '/etc/systemd/system/timers.target.wants/man-db.timer', '/etc/systemd/system/timers.target.wants/logrotate.timer', '/etc/systemd/system/network-online.target.wants', '/etc/systemd/system/network-online.target.wants/NetworkManager-wait-online.service', '/etc/systemd/system/sockets.target.wants', '/etc/systemd/system/sockets.target.wants/snapd.socket', '/etc/systemd/system/sockets.target.wants/apport-forward.socket', '/etc/systemd/system/sockets.target.wants/uuidd.socket', '/etc/systemd/system/sockets.target.wants/acpid.socket', '/etc/systemd/system/sockets.target.wants/cups.socket', '/etc/systemd/system/sockets.target.wants/avahi-daemon.socket', '/etc/systemd/system/open-vm-tools.service.requires', '/etc/systemd/system/open-vm-tools.service.requires/vgauth.service', '/etc/systemd/system/dbus-fi.w1.wpa_supplicant1.service', '/etc/systemd/system/display-manager.service.wants', '/etc/systemd/system/display-manager.service.wants/gpu-manager.service', '/etc/systemd/system/dbus-org.freedesktop.timesync1.service', '/etc/systemd/system/rescue.target.wants', '/etc/systemd/system/rescue.target.wants/grub-initrd-fallback.service', '/etc/systemd/system/snap-bare-5.mount', '/etc/systemd/system/snap-core20-1738.mount', '/etc/systemd/system/bluetooth.target.wants', '/etc/systemd/system/bluetooth.target.wants/bluetooth.service', '/etc/systemd/system/snap-core20-1611.mount', '/etc/systemd/system/dbus-org.freedesktop.nm-dispatcher.service', '/etc/systemd/system/getty.target.wants', '/etc/systemd/system/getty.target.wants/getty@tty1.service', '/etc/systemd/user.conf', '/etc/systemd/pstore.conf', '/etc/systemd/networkd.conf', '/etc/systemd/journald.conf', '/etc/systemd/logind.conf', '/etc/dhcp', '/etc/dhcp/dhclient-exit-hooks.d', '/etc/dhcp/dhclient-exit-hooks.d/rfc3442-classless-routes', '/etc/dhcp/dhclient-exit-hooks.d/debug', '/etc/dhcp/dhclient-exit-hooks.d/zzz_avahi-autoipd', '/etc/dhcp/dhclient-exit-hooks.d/timesyncd', '/etc/dhcp/dhclient.conf', '/etc/dhcp/debug', '/etc/dhcp/dhclient-enter-hooks.d', '/etc/dhcp/dhclient-enter-hooks.d/avahi-autoipd', '/etc/dhcp/dhclient-enter-hooks.d/resolved', '/etc/dhcp/dhclient-enter-hooks.d/debug', '/etc/vmware-tools', '/etc/vmware-tools/resume-vm-default', '/etc/vmware-tools/xautostart.conf', '/etc/vmware-tools/scripts', '/etc/vmware-tools/scripts/vmware', '/etc/vmware-tools/scripts/vmware/network', '/etc/vmware-tools/poweron-vm-default', '/etc/vmware-tools/vgauth', '/etc/vmware-tools/vgauth/schemas', '/etc/vmware-tools/vgauth/schemas/XMLSchema.dtd', '/etc/vmware-tools/vgauth/schemas/saml-schema-assertion-2.0.xsd', '/etc/vmware-tools/vgauth/schemas/datatypes.dtd', '/etc/vmware-tools/vgauth/schemas/XMLSchema-instance.xsd', '/etc/vmware-tools/vgauth/schemas/xmldsig-core-schema.xsd', '/etc/vmware-tools/vgauth/schemas/xml.xsd', '/etc/vmware-tools/vgauth/schemas/XMLSchema.xsd', '/etc/vmware-tools/vgauth/schemas/xenc-schema.xsd', '/etc/vmware-tools/vgauth/schemas/XMLSchema-hasFacetAndProperty.xsd', '/etc/vmware-tools/vgauth/schemas/catalog.xml', '/etc/vmware-tools/statechange.subr', '/etc/vmware-tools/tools.conf.example', '/etc/vmware-tools/vgauth.conf', '/etc/vmware-tools/suspend-vm-default', '/etc/vmware-tools/poweroff-vm-default', '/etc/vmware-tools/tools.conf', '/etc/passwd', '/etc/update-notifier', '/etc/vim', '/etc/vim/vimrc', '/etc/vim/vimrc.tiny', '/etc/sgml', '/etc/sgml/docbook-xml.cat', '/etc/sgml/sgml-data.cat', '/etc/sgml/catalog', '/etc/sgml/docbook-xml', '/etc/sgml/docbook-xml/4.1.2', '/etc/sgml/docbook-xml/4.1.2/dbgenent.mod', '/etc/sgml/docbook-xml/4.0', '/etc/sgml/docbook-xml/4.0/dbgenent.ent', '/etc/sgml/docbook-xml/4.4', '/etc/sgml/docbook-xml/4.4/dbgenent.mod', '/etc/sgml/docbook-xml/4.5', '/etc/sgml/docbook-xml/4.5/dbgenent.mod', '/etc/sgml/docbook-xml/4.2', '/etc/sgml/docbook-xml/4.2/dbgenent.mod', '/etc/sgml/docbook-xml/4.3', '/etc/sgml/docbook-xml/4.3/dbgenent.mod', '/etc/sgml/xml-core.cat', '/etc/initramfs-tools', '/etc/initramfs-tools/scripts', '/etc/initramfs-tools/scripts/nfs-bottom', '/etc/initramfs-tools/scripts/local-bottom', '/etc/initramfs-tools/scripts/local-top', '/etc/initramfs-tools/scripts/init-top', '/etc/initramfs-tools/scripts/nfs-premount', '/etc/initramfs-tools/scripts/nfs-top', '/etc/initramfs-tools/scripts/init-bottom', '/etc/initramfs-tools/scripts/local-premount', '/etc/initramfs-tools/scripts/init-premount', '/etc/initramfs-tools/scripts/panic', '/etc/initramfs-tools/conf.d', '/etc/initramfs-tools/initramfs.conf', '/etc/initramfs-tools/modules', '/etc/initramfs-tools/hooks', '/etc/initramfs-tools/update-initramfs.conf', '/etc/dconf', '/etc/dconf/profile', '/etc/dconf/profile/ibus', '/etc/dconf/db', '/etc/dconf/db/ibus.d', '/etc/dconf/db/ibus.d/00-upstream-settings', '/etc/dconf/db/ibus', '/etc/opt', '/etc/logrotate.d', '/etc/logrotate.d/ppp', '/etc/logrotate.d/ufw', '/etc/logrotate.d/unattended-upgrades', '/etc/logrotate.d/wtmp', '/etc/logrotate.d/bootlog', '/etc/logrotate.d/btmp', '/etc/logrotate.d/speech-dispatcher', '/etc/logrotate.d/rsyslog', '/etc/logrotate.d/alternatives', '/etc/logrotate.d/cups-daemon', '/etc/logrotate.d/dpkg', '/etc/logrotate.d/apport', '/etc/logrotate.d/ubuntu-advantage-tools', '/etc/logrotate.d/apt', '/etc/rcS.d', '/etc/rcS.d/S01pppd-dns', '/etc/rcS.d/S01plymouth-log', '/etc/rcS.d/S01procps', '/etc/rcS.d/S01udev', '/etc/rcS.d/S01ufw', '/etc/rcS.d/S01alsa-utils', '/etc/rcS.d/S01apparmor', '/etc/rcS.d/S01kmod', '/etc/rcS.d/S01keyboard-setup.sh', '/etc/rcS.d/S01x11-common', '/etc/libaudit.conf', '/etc/networks', '/etc/dictionaries-common', '/etc/dictionaries-common/ispell-default', '/etc/dictionaries-common/words', '/etc/sudoers', '/etc/logcheck', '/etc/logcheck/ignore.d.paranoid', '/etc/logcheck/ignore.d.paranoid/cracklib-runtime', '/etc/logcheck/ignore.d.server', '/etc/logcheck/ignore.d.server/libsasl2-modules', '/etc/logcheck/ignore.d.server/rsyslog', '/etc/logcheck/ignore.d.server/gpg-agent', '/etc/pm', '/etc/pm/sleep.d', '/etc/pm/sleep.d/10_grub-common', '/etc/pm/sleep.d/10_unattended-upgrades-hibernate', '/etc/ghostscript', '/etc/ghostscript/fontmap.d', '/etc/ghostscript/cidfmap.d', '/etc/ghostscript/cidfmap.d/90gs-cjk-resource-japan2.conf', '/etc/ghostscript/cidfmap.d/90gs-cjk-resource-gb1.conf', '/etc/ghostscript/cidfmap.d/90gs-cjk-resource-cns1.conf', '/etc/ghostscript/cidfmap.d/90gs-cjk-resource-korea1.conf', '/etc/ghostscript/cidfmap.d/90gs-cjk-resource-japan1.conf', '/etc/shells', '/etc/dpkg', '/etc/dpkg/dpkg.cfg.d', '/etc/dpkg/dpkg.cfg.d/pkg-config-hook-config', '/etc/dpkg/origins', '/etc/dpkg/origins/default', '/etc/dpkg/origins/ubuntu', '/etc/dpkg/origins/debian', '/etc/dpkg/dpkg.cfg', '/etc/sudoers.d', '/etc/sudoers.d/README', '/etc/adduser.conf', '/etc/netplan', '/etc/netplan/01-network-manager-all.yaml', '/etc/zsh_command_not_found', '/etc/subgid-', '/etc/apport', '/etc/apport/blacklist.d', '/etc/apport/blacklist.d/README.blacklist', '/etc/apport/blacklist.d/firefox', '/etc/apport/blacklist.d/apport', '/etc/apport/crashdb.conf', '/etc/apport/native-origins.d', '/etc/apport/native-origins.d/firefox', '/etc/rc.local', '/etc/ssl', '/etc/ssl/certs', '/etc/ssl/certs/D-TRUST_Root_Class_3_CA_2_2009.pem', '/etc/ssl/certs/ANF_Secure_Server_Root_CA.pem', '/etc/ssl/certs/GlobalSign_Root_CA.pem', '/etc/ssl/certs/aee5f10d.0', '/etc/ssl/certs/ee64a828.0', '/etc/ssl/certs/SSL.com_Root_Certification_Authority_ECC.pem', '/etc/ssl/certs/NetLock_Arany_=Class_Gold=_Főtanúsítvány.pem', '/etc/ssl/certs/CA_Disig_Root_R2.pem', '/etc/ssl/certs/certSIGN_Root_CA_G2.pem', '/etc/ssl/certs/02265526.0', '/etc/ssl/certs/SSL.com_Root_Certification_Authority_RSA.pem', '/etc/ssl/certs/Entrust_Root_Certification_Authority_-_G2.pem', '/etc/ssl/certs/Secure_Global_CA.pem', '/etc/ssl/certs/6d41d539.0', '/etc/ssl/certs/48bec511.0', '/etc/ssl/certs/68dd7389.0', '/etc/ssl/certs/4bfab552.0', '/etc/ssl/certs/5273a94c.0', '/etc/ssl/certs/Amazon_Root_CA_3.pem', '/etc/ssl/certs/0f6fa695.0', '/etc/ssl/certs/a94d09e5.0', '/etc/ssl/certs/e-Szigno_Root_CA_2017.pem', '/etc/ssl/certs/607986c7.0', '/etc/ssl/certs/QuoVadis_Root_CA_3_G3.pem', '/etc/ssl/certs/8cb5ee0f.0', '/etc/ssl/certs/DigiCert_Assured_ID_Root_CA.pem', '/etc/ssl/certs/Microsec_e-Szigno_Root_CA_2009.pem', '/etc/ssl/certs/5f15c80c.0', '/etc/ssl/certs/Network_Solutions_Certificate_Authority.pem', '/etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem', '/etc/ssl/certs/Trustwave_Global_ECC_P384_Certification_Authority.pem', '/etc/ssl/certs/dc4d6a89.0', '/etc/ssl/certs/UCA_Extended_Validation_Root.pem', '/etc/ssl/certs/106f3e4d.0', '/etc/ssl/certs/e8de2f56.0', '/etc/ssl/certs/QuoVadis_Root_CA_2.pem', '/etc/ssl/certs/GlobalSign_Root_CA_-_R2.pem', '/etc/ssl/certs/3bde41ac.0', '/etc/ssl/certs/002c0b4f.0', '/etc/ssl/certs/7aaf71c0.0', '/etc/ssl/certs/773e07ad.0', '/etc/ssl/certs/GlobalSign_Root_E46.pem', '/etc/ssl/certs/Amazon_Root_CA_1.pem', '/etc/ssl/certs/AffirmTrust_Premium.pem', '/etc/ssl/certs/3fb36b73.0', '/etc/ssl/certs/064e0aa9.0', '/etc/ssl/certs/f387163d.0', '/etc/ssl/certs/Microsoft_RSA_Root_Certificate_Authority_2017.pem', '/etc/ssl/certs/e868b802.0', '/etc/ssl/certs/Trustwave_Global_ECC_P256_Certification_Authority.pem', '/etc/ssl/certs/b0e59380.0', '/etc/ssl/certs/TWCA_Global_Root_CA.pem', '/etc/ssl/certs/5ad8a5d6.0', '/etc/ssl/certs/TrustCor_RootCert_CA-2.pem', '/etc/ssl/certs/Staat_der_Nederlanden_EV_Root_CA.pem', '/etc/ssl/certs/8d86cdd1.0', '/etc/ssl/certs/76faf6c0.0', '/etc/ssl/certs/d4dae3dd.0', '/etc/ssl/certs/Amazon_Root_CA_4.pem', '/etc/ssl/certs/ca-certificates.crt', '/etc/ssl/certs/TUBITAK_Kamu_SM_SSL_Kok_Sertifikasi_-_Surum_1.pem', '/etc/ssl/certs/ISRG_Root_X1.pem', '/etc/ssl/certs/40547a79.0', '/etc/ssl/certs/653b494a.0', '/etc/ssl/certs/GLOBALTRUST_2020.pem', '/etc/ssl/certs/GlobalSign_Root_R46.pem', '/etc/ssl/certs/SwissSign_Gold_CA_-_G2.pem', '/etc/ssl/certs/fc5a8f99.0', '/etc/ssl/certs/Certum_Trusted_Root_CA.pem', '/etc/ssl/certs/4a6481c9.0', '/etc/ssl/certs/DigiCert_Trusted_Root_G4.pem', '/etc/ssl/certs/eed8c118.0', '/etc/ssl/certs/ACCVRAIZ1.pem', '/etc/ssl/certs/Entrust.net_Premium_2048_Secure_Server_CA.pem', '/etc/ssl/certs/AffirmTrust_Premium_ECC.pem', '/etc/ssl/certs/TrustCor_ECA-1.pem', '/etc/ssl/certs/D-TRUST_Root_Class_3_CA_2_EV_2009.pem', '/etc/ssl/certs/DigiCert_Assured_ID_Root_G2.pem', '/etc/ssl/certs/emSign_ECC_Root_CA_-_C3.pem', '/etc/ssl/certs/349f2832.0', '/etc/ssl/certs/3513523f.0', '/etc/ssl/certs/6b99d060.0', '/etc/ssl/certs/IdenTrust_Commercial_Root_CA_1.pem', '/etc/ssl/certs/749e9e03.0', '/etc/ssl/certs/ef954a4e.0', '/etc/ssl/certs/T-TeleSec_GlobalRoot_Class_2.pem', '/etc/ssl/certs/GDCA_TrustAUTH_R5_ROOT.pem', '/etc/ssl/certs/GTS_Root_R1.pem', '/etc/ssl/certs/1d3472b9.0', '/etc/ssl/certs/DigiCert_Global_Root_G2.pem', '/etc/ssl/certs/a3418fda.0', '/etc/ssl/certs/Hongkong_Post_Root_CA_3.pem', '/etc/ssl/certs/Atos_TrustedRoot_2011.pem', '/etc/ssl/certs/USERTrust_ECC_Certification_Authority.pem', '/etc/ssl/certs/TWCA_Root_Certification_Authority.pem', '/etc/ssl/certs/dd8e9d41.0', '/etc/ssl/certs/ssl-cert-snakeoil.pem', '/etc/ssl/certs/Buypass_Class_3_Root_CA.pem', '/etc/ssl/certs/COMODO_ECC_Certification_Authority.pem', '/etc/ssl/certs/0a775a30.0', '/etc/ssl/certs/Starfield_Class_2_CA.pem', '/etc/ssl/certs/5f618aec.0', '/etc/ssl/certs/de6d66f3.0', '/etc/ssl/certs/QuoVadis_Root_CA_2_G3.pem', '/etc/ssl/certs/cd58d51e.0', '/etc/ssl/certs/SecureTrust_CA.pem', '/etc/ssl/certs/03179a64.0', '/etc/ssl/certs/9b5697b0.0', '/etc/ssl/certs/0f5dc4f3.0', '/etc/ssl/certs/GlobalSign_ECC_Root_CA_-_R4.pem', '/etc/ssl/certs/Starfield_Root_Certificate_Authority_-_G2.pem', '/etc/ssl/certs/3e44d2f7.0', '/etc/ssl/certs/bf53fb88.0', '/etc/ssl/certs/DigiCert_Assured_ID_Root_G3.pem', '/etc/ssl/certs/Go_Daddy_Root_Certificate_Authority_-_G2.pem', '/etc/ssl/certs/062cdee6.0', '/etc/ssl/certs/ePKI_Root_Certification_Authority.pem', '/etc/ssl/certs/1e09d511.0', '/etc/ssl/certs/Go_Daddy_Class_2_CA.pem', '/etc/ssl/certs/5d3033c5.0', '/etc/ssl/certs/emSign_ECC_Root_CA_-_G3.pem', '/etc/ssl/certs/USERTrust_RSA_Certification_Authority.pem', '/etc/ssl/certs/EC-ACC.pem', '/etc/ssl/certs/emSign_Root_CA_-_C1.pem', '/etc/ssl/certs/GTS_Root_R2.pem', '/etc/ssl/certs/f51bb24c.0', '/etc/ssl/certs/9c8dfbd4.0', '/etc/ssl/certs/DigiCert_Global_Root_CA.pem', '/etc/ssl/certs/76cb8f92.0', '/etc/ssl/certs/OISTE_WISeKey_Global_Root_GC_CA.pem', '/etc/ssl/certs/18856ac4.0', '/etc/ssl/certs/06dc52d5.0', '/etc/ssl/certs/Certigna.pem', '/etc/ssl/certs/Security_Communication_RootCA2.pem', '/etc/ssl/certs/2923b3f9.0', '/etc/ssl/certs/b1159c4c.0', '/etc/ssl/certs/c28a8a30.0', '/etc/ssl/certs/Hellenic_Academic_and_Research_Institutions_RootCA_2011.pem', '/etc/ssl/certs/09789157.0', '/etc/ssl/certs/cbf06781.0', '/etc/ssl/certs/f0c70a8d.0', '/etc/ssl/certs/certSIGN_ROOT_CA.pem', '/etc/ssl/certs/E-Tugra_Certification_Authority.pem', '/etc/ssl/certs/9d04f354.0', '/etc/ssl/certs/SwissSign_Silver_CA_-_G2.pem', '/etc/ssl/certs/SSL.com_EV_Root_Certification_Authority_ECC.pem', '/etc/ssl/certs/b433981b.0', '/etc/ssl/certs/54657681.0', '/etc/ssl/certs/f3377b1b.0', '/etc/ssl/certs/4b718d9b.0', '/etc/ssl/certs/AffirmTrust_Networking.pem', '/etc/ssl/certs/40193066.0', '/etc/ssl/certs/TrustCor_RootCert_CA-1.pem', '/etc/ssl/certs/Certum_EC-384_CA.pem', '/etc/ssl/certs/cc450945.0', '/etc/ssl/certs/Hellenic_Academic_and_Research_Institutions_ECC_RootCA_2015.pem', '/etc/ssl/certs/f39fc864.0', '/etc/ssl/certs/0c31d5ce', '/etc/ssl/certs/Security_Communication_Root_CA.pem', '/etc/ssl/certs/Buypass_Class_2_Root_CA.pem', '/etc/ssl/certs/e113c810.0', '/etc/ssl/certs/AC_RAIZ_FNMT-RCM_SERVIDORES_SEGUROS.pem', '/etc/ssl/certs/OISTE_WISeKey_Global_Root_GB_CA.pem', '/etc/ssl/certs/ca6e4ad9.0', '/etc/ssl/certs/TeliaSonera_Root_CA_v1.pem', '/etc/ssl/certs/Amazon_Root_CA_2.pem', '/etc/ssl/certs/8160b96c.0', '/etc/ssl/certs/GTS_Root_R3.pem', '/etc/ssl/certs/GlobalSign_Root_CA_-_R6.pem', '/etc/ssl/certs/e18bfb83.0', '/etc/ssl/certs/IdenTrust_Public_Sector_Root_CA_1.pem', '/etc/ssl/certs/f249de83.0', '/etc/ssl/certs/988a38cb.0', '/etc/ssl/certs/XRamp_Global_CA_Root.pem', '/etc/ssl/certs/1636090b.0', '/etc/ssl/certs/ff34af3f.0', '/etc/ssl/certs/1001acf7.0', '/etc/ssl/certs/Entrust_Root_Certification_Authority_-_G4.pem', '/etc/ssl/certs/GlobalSign_Root_CA_-_R3.pem', '/etc/ssl/certs/Starfield_Services_Root_Certificate_Authority_-_G2.pem', '/etc/ssl/certs/2ae6433e.0', '/etc/ssl/certs/7719f463.0', '/etc/ssl/certs/ce5e74ef.0', '/etc/ssl/certs/d6325660.0', '/etc/ssl/certs/f30dd6ad.0', '/etc/ssl/certs/b7a5b843.0', '/etc/ssl/certs/GlobalSign_ECC_Root_CA_-_R5.pem', '/etc/ssl/certs/4304c5e5.0', '/etc/ssl/certs/Baltimore_CyberTrust_Root.pem', '/etc/ssl/certs/2b349938.0', '/etc/ssl/certs/d887a5bb.0', '/etc/ssl/certs/c01eb047.0', '/etc/ssl/certs/626dceaf.0', '/etc/ssl/certs/406c9bb1.0', '/etc/ssl/certs/1e08bfd1.0', '/etc/ssl/certs/e73d606e.0', '/etc/ssl/certs/Certigna_Root_CA.pem', '/etc/ssl/certs/5e98733a.0', '/etc/ssl/certs/NAVER_Global_Root_Certification_Authority.pem', '/etc/ssl/certs/f081611a.0', '/etc/ssl/certs/930ac5d2.0', '/etc/ssl/certs/14bc7599.0', '/etc/ssl/certs/32888f65.0', '/etc/ssl/certs/T-TeleSec_GlobalRoot_Class_3.pem', '/etc/ssl/certs/5443e9e3.0', '/etc/ssl/certs/57bcb2da.0', '/etc/ssl/certs/75d1b2ed.0', '/etc/ssl/certs/b727005e.0', '/etc/ssl/certs/4f316efb.0', '/etc/ssl/certs/5cd81ad7.0', '/etc/ssl/certs/QuoVadis_Root_CA_3.pem', '/etc/ssl/certs/b66938e9.0', '/etc/ssl/certs/244b5494.0', '/etc/ssl/certs/93bc0acc.0', '/etc/ssl/certs/3e45d192.0', '/etc/ssl/certs/SSL.com_EV_Root_Certification_Authority_RSA_R2.pem', '/etc/ssl/certs/Entrust_Root_Certification_Authority_-_EC1.pem', '/etc/ssl/certs/GTS_Root_R4.pem', '/etc/ssl/certs/Cybertrust_Global_Root.pem', '/etc/ssl/certs/4042bcee.0', '/etc/ssl/certs/emSign_Root_CA_-_G1.pem', '/etc/ssl/certs/Certum_Trusted_Network_CA_2.pem', '/etc/ssl/certs/Izenpe.com.pem', '/etc/ssl/certs/AffirmTrust_Commercial.pem', '/etc/ssl/certs/e35234b1.0', '/etc/ssl/certs/e36a6752.0', '/etc/ssl/certs/d7e8dc79.0', '/etc/ssl/certs/fe8a2cd8.0', '/etc/ssl/certs/SecureSign_RootCA11.pem', '/etc/ssl/certs/SZAFIR_ROOT_CA2.pem', '/etc/ssl/certs/fa5da96b.0', '/etc/ssl/certs/Actalis_Authentication_Root_CA.pem', '/etc/ssl/certs/CFCA_EV_ROOT.pem', '/etc/ssl/certs/1c7314a2', '/etc/ssl/certs/Entrust_Root_Certification_Authority.pem', '/etc/ssl/certs/0b1b94ef.0', '/etc/ssl/certs/b81b93f0.0', '/etc/ssl/certs/feffd413.0', '/etc/ssl/certs/COMODO_Certification_Authority.pem', '/etc/ssl/certs/Trustwave_Global_Certification_Authority.pem', '/etc/ssl/certs/Certum_Trusted_Network_CA.pem', '/etc/ssl/certs/Hongkong_Post_Root_CA_1.pem', '/etc/ssl/certs/QuoVadis_Root_CA_1_G3.pem', '/etc/ssl/certs/706f604c.0', '/etc/ssl/certs/COMODO_RSA_Certification_Authority.pem', '/etc/ssl/certs/0bf05006.0', '/etc/ssl/certs/DigiCert_Global_Root_G3.pem', '/etc/ssl/certs/8d89cda1.0', '/etc/ssl/certs/cd8c0d63.0', '/etc/ssl/certs/AC_RAIZ_FNMT-RCM.pem', '/etc/ssl/certs/9482e63a.0', '/etc/ssl/certs/UCA_Global_G2_Root.pem', '/etc/ssl/certs/Comodo_AAA_Services_root.pem', '/etc/ssl/certs/7f3d5d1d.0', '/etc/ssl/certs/Autoridad_de_Certificacion_Firmaprofesional_CIF_A62634068.pem', '/etc/ssl/certs/6fa5da56.0', '/etc/ssl/certs/Microsoft_ECC_Root_Certificate_Authority_2017.pem', '/etc/ssl/certs/Hellenic_Academic_and_Research_Institutions_RootCA_2015.pem', '/etc/ssl/private', '/etc/ssl/private/ssl-cert-snakeoil.key', '/etc/ssl/openssl.cnf', '/etc/rc1.d', '/etc/rc1.d/K01irqbalance', '/etc/rc1.d/K01cups-browsed', '/etc/rc1.d/K01gdm3', '/etc/rc1.d/K01speech-dispatcher', '/etc/rc1.d/K01open-vm-tools', '/etc/rc1.d/K01openvpn', '/etc/rc1.d/K01rsyslog', '/etc/rc1.d/K01kerneloops', '/etc/rc1.d/K01whoopsie', '/etc/rc1.d/K01avahi-daemon', '/etc/rc1.d/K01cups', '/etc/rc1.d/K01spice-vdagent', '/etc/rc1.d/K01bluetooth', '/etc/rc1.d/K01pulseaudio-enable-autospawn', '/etc/rc1.d/K01saned', '/etc/rc1.d/K01ufw', '/etc/rc1.d/K01uuidd', '/etc/rc1.d/K01alsa-utils', '/etc/legal', '/etc/hosts', '/etc/udisks2', '/etc/udisks2/udisks2.conf', '/etc/chatscripts', '/etc/chatscripts/gprs', '/etc/chatscripts/provider', '/etc/chatscripts/pap', '/etc/apt', '/etc/apt/preferences.d', '/etc/apt/apt.conf.d', '/etc/apt/apt.conf.d/60icons-hidpi', '/etc/apt/apt.conf.d/00trustcdrom', '/etc/apt/apt.conf.d/50command-not-found', '/etc/apt/apt.conf.d/20apt-esm-hook.conf', '/etc/apt/apt.conf.d/20packagekit', '/etc/apt/apt.conf.d/01autoremove', '/etc/apt/apt.conf.d/70debconf', '/etc/apt/apt.conf.d/00aptitude', '/etc/apt/apt.conf.d/20dbus', '/etc/apt/apt.conf.d/20archive', '/etc/apt/apt.conf.d/15update-stamp', '/etc/apt/apt.conf.d/99update-notifier', '/etc/apt/apt.conf.d/50unattended-upgrades', '/etc/apt/apt.conf.d/01-vendor-ubuntu', '/etc/apt/apt.conf.d/20auto-upgrades', '/etc/apt/apt.conf.d/60icons', '/etc/apt/apt.conf.d/10periodic', '/etc/apt/apt.conf.d/20snapd.conf', '/etc/apt/apt.conf.d/50appstream', '/etc/apt/sources.list', '/etc/apt/sources.bak', '/etc/apt/trusted.gpg.d', '/etc/apt/trusted.gpg.d/ubuntu-keyring-2012-archive.gpg', '/etc/apt/trusted.gpg.d/ubuntu-keyring-2018-archive.gpg', '/etc/apt/trusted.gpg.d/ubuntu-keyring-2012-cdimage.gpg', '/etc/apt/sources.list.d', '/etc/apt/auth.conf.d', '/etc/binfmt.d', '/etc/selinux', '/etc/selinux/semanage.conf', '/etc/networkd-dispatcher', '/etc/networkd-dispatcher/no-carrier.d', '/etc/networkd-dispatcher/dormant.d', '/etc/networkd-dispatcher/off.d', '/etc/networkd-dispatcher/degraded.d', '/etc/networkd-dispatcher/routable.d', '/etc/networkd-dispatcher/carrier.d', '/etc/UPower', '/etc/UPower/UPower.conf', '/etc/issue', '/etc/rsyslog.conf', '/etc/update-motd.d', '/etc/update-motd.d/98-fsck-at-reboot', '/etc/update-motd.d/95-hwe-eol', '/etc/update-motd.d/88-esm-announce', '/etc/update-motd.d/85-fwupd', '/etc/update-motd.d/91-contract-ua-esm-status', '/etc/update-motd.d/00-header', '/etc/update-motd.d/92-unattended-upgrades', '/etc/update-motd.d/91-release-upgrade', '/etc/update-motd.d/90-updates-available', '/etc/update-motd.d/50-motd-news', '/etc/update-motd.d/98-reboot-required', '/etc/update-motd.d/10-help-text', '/etc/debian_version', '/etc/rc2.d', '/etc/rc2.d/S01console-setup.sh', '/etc/rc2.d/S01plymouth', '/etc/rc2.d/S01rsyslog', '/etc/rc2.d/S01irqbalance', '/etc/rc2.d/S01cups', '/etc/rc2.d/K01speech-dispatcher', '/etc/rc2.d/S01cron', '/etc/rc2.d/S01spice-vdagent', '/etc/rc2.d/S01anacron', '/etc/rc2.d/S01openvpn', '/etc/rc2.d/S01unattended-upgrades', '/etc/rc2.d/S01rsync', '/etc/rc2.d/S01cups-browsed', '/etc/rc2.d/S01acpid', '/etc/rc2.d/S01apport', '/etc/rc2.d/S01kerneloops', '/etc/rc2.d/S01pulseaudio-enable-autospawn', '/etc/rc2.d/S01dbus', '/etc/rc2.d/S01grub-common', '/etc/rc2.d/S01avahi-daemon', '/etc/rc2.d/S01open-vm-tools', '/etc/rc2.d/S01uuidd', '/etc/rc2.d/S01gdm3', '/etc/rc2.d/S01bluetooth', '/etc/rc2.d/S01whoopsie', '/etc/rc2.d/S01saned', '/etc/bluetooth', '/etc/bluetooth/input.conf', '/etc/bluetooth/main.conf', '/etc/bluetooth/network.conf', '/etc/ssh', '/etc/ssh/ssh_config', '/etc/ssh/ssh_config.d', '/etc/shadow-']

files_in_etc = os.popen("find /etc/ -print").read().split("\n")
if files_in_etc[-1] == '':
	files_in_etc = files_in_etc[:-1]

print("\n\n")
print("PRINTING NONDEFAULT FILES IN /etc AND SUBDIRECTORIES AND DEFAULT FILES IN /etc AND SUBDIRECTORIES THAT DO NOT EXIST")
print("\n")

for file in files_in_etc:
	if file not in default_files_in_etc:
		print(f"nondefault /etc entry: {file}")

print("\n")
for file in default_files_in_etc:
	if file not in files_in_etc:
		print(f"default /etc entry that doesnt exist: {file}")			

		

print("\n\n")
print("PRINTING NONDEFAULT PROCS")
print("\n")

default_procs = ['/lib/systemd/systemd--system--deserialize21', '[kthreadd]', '[rcu_gp]', '[rcu_par_gp]', '[netns]', '[kworker/0:0H-events_highpri]', '[kworker/0:1H-kblockd]', '[mm_percpu_wq]', '[rcu_tasks_rude_]', '[rcu_tasks_trace]', '[ksoftirqd/0]', '[rcu_sched]', '[migration/0]', '[idle_inject/0]', '[cpuhp/0]', '[cpuhp/1]', '[idle_inject/1]', '[migration/1]', '[ksoftirqd/1]', '[kworker/1:0H-events_highpri]', '[kdevtmpfs]', '[inet_frag_wq]', '[kauditd]', '[khungtaskd]', '[oom_reaper]', '[writeback]', '[kcompactd0]', '[ksmd]', '[khugepaged]', '[kintegrityd]', '[kblockd]', '[blkcg_punt_bio]', '[tpm_dev_wq]', '[ata_sff]', '[md]', '[edac-poller]', '[devfreq_wq]', '[watchdogd]', '[kswapd0]', '[ecryptfs-kthrea]', '[kthrotld]', '[irq/24-pciehp]', '[irq/25-pciehp]', '[irq/26-pciehp]', '[irq/27-pciehp]', '[irq/28-pciehp]', '[irq/29-pciehp]', '[irq/30-pciehp]', '[irq/31-pciehp]', '[irq/32-pciehp]', '[irq/33-pciehp]', '[irq/34-pciehp]', '[irq/35-pciehp]', '[irq/36-pciehp]', '[irq/37-pciehp]', '[irq/38-pciehp]', '[irq/39-pciehp]', '[irq/40-pciehp]', '[irq/41-pciehp]', '[irq/42-pciehp]', '[irq/43-pciehp]', '[irq/44-pciehp]', '[irq/45-pciehp]', '[irq/46-pciehp]', '[irq/47-pciehp]', '[irq/48-pciehp]', '[irq/49-pciehp]', '[irq/50-pciehp]', '[irq/51-pciehp]', '[irq/52-pciehp]', '[irq/53-pciehp]', '[irq/54-pciehp]', '[irq/55-pciehp]', '[acpi_thermal_pm]', '[scsi_eh_0]', '[scsi_tmf_0]', '[scsi_eh_1]', '[scsi_tmf_1]', '[vfio-irqfd-clea]', '[kworker/1:1H-events_highpri]', '[mld]', '[ipv6_addrconf]', '[kstrp]', '[zswap-shrink]', '[kworker/u257:0-hci0]', '[charger_manager]', '[mpt_poll_0]', '[mpt/0]', '[scsi_eh_2]', '[scsi_tmf_2]', '[scsi_eh_3]', '[scsi_tmf_3]', '[scsi_eh_4]', '[scsi_tmf_4]', '[scsi_eh_5]', '[scsi_tmf_5]', '[scsi_eh_6]', '[scsi_tmf_6]', '[scsi_eh_7]', '[scsi_tmf_7]', '[scsi_eh_8]', '[scsi_tmf_8]', '[scsi_eh_9]', '[scsi_tmf_9]', '[scsi_eh_10]', '[scsi_tmf_10]', '[scsi_eh_11]', '[scsi_tmf_11]', '[scsi_eh_12]', '[scsi_tmf_12]', '[scsi_eh_13]', '[scsi_tmf_13]', '[scsi_eh_14]', '[scsi_tmf_14]', '[scsi_eh_15]', '[scsi_tmf_15]', '[scsi_eh_16]', '[scsi_tmf_16]', '[scsi_eh_17]', '[scsi_tmf_17]', '[scsi_eh_18]', '[scsi_tmf_18]', '[scsi_eh_19]', '[scsi_tmf_19]', '[scsi_eh_20]', '[scsi_tmf_20]', '[scsi_eh_21]', '[scsi_tmf_21]', '[scsi_eh_22]', '[scsi_tmf_22]', '[scsi_eh_23]', '[scsi_tmf_23]', '[scsi_eh_24]', '[scsi_tmf_24]', '[scsi_eh_25]', '[scsi_tmf_25]', '[scsi_eh_26]', '[scsi_tmf_26]', '[scsi_eh_27]', '[scsi_tmf_27]', '[scsi_eh_28]', '[scsi_tmf_28]', '[scsi_eh_29]', '[scsi_tmf_29]', '[scsi_eh_30]', '[scsi_tmf_30]', '[scsi_eh_31]', '[scsi_tmf_31]', '[scsi_eh_32]', '[scsi_tmf_32]', '[jbd2/sda5-8]', '[ext4-rsv-conver]', '[ipmi-msghandler]', '[ttm_swap]', '[irq/16-vmwgfx]', '[card0-crtc0]', '[card0-crtc1]', '[card0-crtc2]', '[card0-crtc3]', '[card0-crtc4]', '[card0-crtc5]', '[card0-crtc6]', '[card0-crtc7]', 'vmware-vmblock-fuse/run/vmblock-fuse-orw,subtype=vmware-vmblock,default_permissions,allow_other,dev,suid', 'vmware-vmblock-fuse/run/vmblock-fuse-orw,subtype=vmware-vmblock,default_permissions,allow_other,dev,suid', 'vmware-vmblock-fuse/run/vmblock-fuse-orw,subtype=vmware-vmblock,default_permissions,allow_other,dev,suid', '[kworker/u257:1-hci0]', '[cryptd]', '/usr/bin/VGAuthService', '/usr/bin/vmtoolsd', '/usr/bin/vmtoolsd', '/usr/bin/vmtoolsd', '/usr/bin/vmtoolsd', '/usr/lib/accountsservice/accounts-daemon', '/usr/lib/accountsservice/accounts-daemon', '/usr/lib/accountsservice/accounts-daemon', '/usr/sbin/acpid', 'avahi-daemon:running[ubuntu.local]', '/usr/lib/bluetooth/bluetoothd', '/usr/sbin/cron-f', '/usr/sbin/cupsd-l', '/usr/bin/dbus-daemon--system--address=systemd:--nofork--nopidfile--systemd-activation--syslog-only', '/usr/sbin/NetworkManager--no-daemon', '/usr/sbin/NetworkManager--no-daemon', '/usr/sbin/NetworkManager--no-daemon', '/usr/sbin/irqbalance--foreground', '/usr/sbin/irqbalance--foreground', '/usr/bin/python3/usr/bin/networkd-dispatcher--run-startup-triggers', '/usr/lib/policykit-1/polkitd--no-debug', '/usr/lib/policykit-1/polkitd--no-debug', '/usr/lib/policykit-1/polkitd--no-debug', '/usr/sbin/rsyslogd-n-iNONE', '/usr/sbin/rsyslogd-n-iNONE', '/usr/sbin/rsyslogd-n-iNONE', '/usr/sbin/rsyslogd-n-iNONE', '/usr/libexec/switcheroo-control', '/usr/libexec/switcheroo-control', '/usr/libexec/switcheroo-control', '/lib/systemd/systemd-logind', '/usr/lib/udisks2/udisksd', '/usr/lib/udisks2/udisksd', '/usr/lib/udisks2/udisksd', '/usr/lib/udisks2/udisksd', '/usr/lib/udisks2/udisksd', '/sbin/wpa_supplicant-u-s-O/run/wpa_supplicant', 'avahi-daemon:chroothelper', '/usr/sbin/ModemManager', '/usr/sbin/ModemManager', '/usr/sbin/ModemManager', '/usr/sbin/cups-browsed', '/usr/sbin/cups-browsed', '/usr/sbin/cups-browsed', '/usr/bin/python3/usr/share/unattended-upgrades/unattended-upgrade-shutdown--wait-for-signal', '/usr/bin/python3/usr/share/unattended-upgrades/unattended-upgrade-shutdown--wait-for-signal', '/usr/sbin/gdm3', '/usr/sbin/gdm3', '/usr/sbin/gdm3', '/usr/libexec/rtkit-daemon', '/usr/libexec/rtkit-daemon', '/usr/libexec/rtkit-daemon', '/usr/lib/upower/upowerd', '/usr/lib/upower/upowerd', '/usr/lib/upower/upowerd', '/usr/bin/whoopsie-f', '/usr/bin/whoopsie-f', '/usr/bin/whoopsie-f', '/usr/sbin/kerneloops--test', '/usr/sbin/kerneloops', '/usr/libexec/colord', '/usr/libexec/colord', '/usr/libexec/colord', 'gdm-session-worker[pam/gdm-password]', 'gdm-session-worker[pam/gdm-password]', 'gdm-session-worker[pam/gdm-password]', '/lib/systemd/systemd--user', '(sd-pam)', '/usr/bin/pulseaudio--daemonize=no--log-target=journal', '/usr/bin/pulseaudio--daemonize=no--log-target=journal', '/usr/bin/pulseaudio--daemonize=no--log-target=journal', '/usr/bin/pulseaudio--daemonize=no--log-target=journal', '/usr/libexec/tracker-miner-fs', '/usr/libexec/tracker-miner-fs', '/usr/libexec/tracker-miner-fs', '/usr/libexec/tracker-miner-fs', '/usr/libexec/tracker-miner-fs', '/usr/bin/dbus-daemon--session--address=systemd:--nofork--nopidfile--systemd-activation--syslog-only', '/usr/bin/gnome-keyring-daemon--daemonize--login', '/usr/bin/gnome-keyring-daemon--daemonize--login', '/usr/bin/gnome-keyring-daemon--daemonize--login', '/usr/bin/gnome-keyring-daemon--daemonize--login', '/usr/libexec/gvfsd', '/usr/libexec/gvfsd', '/usr/libexec/gvfsd', '/usr/libexec/gvfsd-fuse/run/user/1000/gvfs-f-obig_writes', '/usr/libexec/gvfsd-fuse/run/user/1000/gvfs-f-obig_writes', '/usr/libexec/gvfsd-fuse/run/user/1000/gvfs-f-obig_writes', '/usr/libexec/gvfsd-fuse/run/user/1000/gvfs-f-obig_writes', '/usr/libexec/gvfsd-fuse/run/user/1000/gvfs-f-obig_writes', '/usr/libexec/gvfsd-fuse/run/user/1000/gvfs-f-obig_writes', '/usr/libexec/gvfs-udisks2-volume-monitor', '/usr/libexec/gvfs-udisks2-volume-monitor', '/usr/libexec/gvfs-udisks2-volume-monitor', '/usr/libexec/gvfs-udisks2-volume-monitor', '/usr/libexec/gvfs-afc-volume-monitor', '/usr/libexec/gvfs-afc-volume-monitor', '/usr/libexec/gvfs-afc-volume-monitor', '/usr/libexec/gvfs-afc-volume-monitor', '/usr/libexec/gvfs-mtp-volume-monitor', '/usr/libexec/gvfs-mtp-volume-monitor', '/usr/libexec/gvfs-mtp-volume-monitor', '/usr/libexec/gvfs-gphoto2-volume-monitor', '/usr/libexec/gvfs-gphoto2-volume-monitor', '/usr/libexec/gvfs-gphoto2-volume-monitor', '/usr/libexec/gvfs-goa-volume-monitor', '/usr/libexec/gvfs-goa-volume-monitor', '/usr/libexec/gvfs-goa-volume-monitor', '/usr/libexec/goa-daemon', '/usr/libexec/goa-daemon', '/usr/libexec/goa-daemon', '/usr/libexec/goa-daemon', '/usr/libexec/goa-identity-service', '/usr/libexec/goa-identity-service', '/usr/libexec/goa-identity-service', '[krfcommd]', '/usr/lib/gdm3/gdm-x-session--run-scriptenvGNOME_SHELL_SESSION_MODE=ubuntu/usr/bin/gnome-session--systemd--session=ubuntu', '/usr/lib/gdm3/gdm-x-session--run-scriptenvGNOME_SHELL_SESSION_MODE=ubuntu/usr/bin/gnome-session--systemd--session=ubuntu', '/usr/lib/gdm3/gdm-x-session--run-scriptenvGNOME_SHELL_SESSION_MODE=ubuntu/usr/bin/gnome-session--systemd--session=ubuntu', '/usr/lib/xorg/Xorgvt2-displayfd3-auth/run/user/1000/gdm/Xauthority-backgroundnone-noreset-keeptty-verbose3', '/usr/lib/xorg/Xorgvt2-displayfd3-auth/run/user/1000/gdm/Xauthority-backgroundnone-noreset-keeptty-verbose3', '/usr/libexec/gnome-session-binary--systemd--systemd--session=ubuntu', '/usr/libexec/gnome-session-binary--systemd--systemd--session=ubuntu', '/usr/libexec/gnome-session-binary--systemd--systemd--session=ubuntu', '/usr/bin/ssh-agent/usr/bin/im-launchenvGNOME_SHELL_SESSION_MODE=ubuntu/usr/bin/gnome-session--systemd--session=ubuntu', '/usr/libexec/gvfsd-metadata', '/usr/libexec/gvfsd-metadata', '/usr/libexec/gvfsd-metadata', '/usr/libexec/at-spi-bus-launcher', '/usr/libexec/at-spi-bus-launcher', '/usr/libexec/at-spi-bus-launcher', '/usr/libexec/at-spi-bus-launcher', '/usr/bin/dbus-daemon--config-file=/usr/share/defaults/at-spi2/accessibility.conf--nofork--print-address3', '/usr/libexec/gnome-session-ctl--monitor', '/usr/libexec/gnome-session-ctl--monitor', '/usr/libexec/gnome-session-binary--systemd-service--session=ubuntu', '/usr/libexec/gnome-session-binary--systemd-service--session=ubuntu', '/usr/libexec/gnome-session-binary--systemd-service--session=ubuntu', '/usr/libexec/gnome-session-binary--systemd-service--session=ubuntu', '/usr/bin/gnome-shell', '/usr/bin/gnome-shell', '/usr/bin/gnome-shell', '/usr/bin/gnome-shell', '/usr/bin/gnome-shell', '/usr/bin/gnome-shell', '/usr/bin/gnome-shell', 'ibus-daemon--paneldisable--xim', 'ibus-daemon--paneldisable--xim', 'ibus-daemon--paneldisable--xim', '/usr/libexec/ibus-dconf', '/usr/libexec/ibus-dconf', '/usr/libexec/ibus-dconf', '/usr/libexec/ibus-dconf', '/usr/libexec/ibus-extension-gtk3', '/usr/libexec/ibus-extension-gtk3', '/usr/libexec/ibus-extension-gtk3', '/usr/libexec/ibus-extension-gtk3', '/usr/libexec/ibus-x11--kill-daemon', '/usr/libexec/ibus-x11--kill-daemon', '/usr/libexec/ibus-x11--kill-daemon', '/usr/libexec/ibus-portal', '/usr/libexec/ibus-portal', '/usr/libexec/ibus-portal', '/usr/libexec/at-spi2-registryd--use-gnome-session', '/usr/libexec/at-spi2-registryd--use-gnome-session', '/usr/libexec/at-spi2-registryd--use-gnome-session', '/usr/libexec/xdg-permission-store', '/usr/libexec/xdg-permission-store', '/usr/libexec/xdg-permission-store', '/usr/libexec/gnome-shell-calendar-server', '/usr/libexec/gnome-shell-calendar-server', '/usr/libexec/gnome-shell-calendar-server', '/usr/libexec/gnome-shell-calendar-server', '/usr/libexec/gnome-shell-calendar-server', '/usr/libexec/gnome-shell-calendar-server', '/usr/libexec/evolution-source-registry', '/usr/libexec/evolution-source-registry', '/usr/libexec/evolution-source-registry', '/usr/libexec/evolution-source-registry', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/evolution-calendar-factory', '/usr/libexec/dconf-service', '/usr/libexec/dconf-service', '/usr/libexec/dconf-service', '/usr/libexec/evolution-addressbook-factory', '/usr/libexec/evolution-addressbook-factory', '/usr/libexec/evolution-addressbook-factory', '/usr/libexec/evolution-addressbook-factory', '/usr/libexec/evolution-addressbook-factory', '/usr/libexec/evolution-addressbook-factory', '/usr/bin/gjs/usr/share/gnome-shell/org.gnome.Shell.Notifications', '/usr/bin/gjs/usr/share/gnome-shell/org.gnome.Shell.Notifications', '/usr/bin/gjs/usr/share/gnome-shell/org.gnome.Shell.Notifications', '/usr/bin/gjs/usr/share/gnome-shell/org.gnome.Shell.Notifications', '/usr/bin/gjs/usr/share/gnome-shell/org.gnome.Shell.Notifications', '/usr/libexec/gvfsd-trash--spawner:1.3/org/gtk/gvfs/exec_spaw/0', '/usr/libexec/gvfsd-trash--spawner:1.3/org/gtk/gvfs/exec_spaw/0', '/usr/libexec/gvfsd-trash--spawner:1.3/org/gtk/gvfs/exec_spaw/0', '/usr/libexec/gsd-a11y-settings', '/usr/libexec/gsd-a11y-settings', '/usr/libexec/gsd-a11y-settings', '/usr/libexec/gsd-a11y-settings', '/usr/libexec/gsd-color', '/usr/libexec/gsd-color', '/usr/libexec/gsd-color', '/usr/libexec/gsd-color', '/usr/libexec/gsd-datetime', '/usr/libexec/gsd-datetime', '/usr/libexec/gsd-datetime', '/usr/libexec/gsd-datetime', '/usr/libexec/gsd-housekeeping', '/usr/libexec/gsd-housekeeping', '/usr/libexec/gsd-housekeeping', '/usr/libexec/gsd-housekeeping', '/usr/libexec/gsd-keyboard', '/usr/libexec/gsd-keyboard', '/usr/libexec/gsd-keyboard', '/usr/libexec/gsd-keyboard', '/usr/libexec/gsd-media-keys', '/usr/libexec/gsd-media-keys', '/usr/libexec/gsd-media-keys', '/usr/libexec/gsd-media-keys', '/usr/libexec/gsd-power', '/usr/libexec/gsd-power', '/usr/libexec/gsd-power', '/usr/libexec/gsd-power', '/usr/libexec/gsd-print-notifications', '/usr/libexec/gsd-print-notifications', '/usr/libexec/gsd-print-notifications', '/usr/libexec/gsd-rfkill', '/usr/libexec/gsd-rfkill', '/usr/libexec/gsd-rfkill', '/usr/bin/vmtoolsd-nvmusr--blockFd3', '/usr/bin/vmtoolsd-nvmusr--blockFd3', '/usr/bin/vmtoolsd-nvmusr--blockFd3', '/usr/bin/vmtoolsd-nvmusr--blockFd3', '/usr/libexec/gsd-screensaver-proxy', '/usr/libexec/gsd-screensaver-proxy', '/usr/libexec/gsd-screensaver-proxy', '/usr/libexec/gsd-sharing', '/usr/libexec/gsd-sharing', '/usr/libexec/gsd-sharing', '/usr/libexec/gsd-sharing', '/usr/libexec/gsd-smartcard', '/usr/libexec/gsd-smartcard', '/usr/libexec/gsd-smartcard', '/usr/libexec/gsd-smartcard', '/usr/libexec/gsd-smartcard', '/usr/libexec/gsd-sound', '/usr/libexec/gsd-sound', '/usr/libexec/gsd-sound', '/usr/libexec/gsd-sound', '/usr/libexec/gsd-usb-protection', '/usr/libexec/gsd-usb-protection', '/usr/libexec/gsd-usb-protection', '/usr/libexec/gsd-usb-protection', '/usr/libexec/gsd-wacom', '/usr/libexec/gsd-wacom', '/usr/libexec/gsd-wacom', '/usr/libexec/gsd-wwan', '/usr/libexec/gsd-wwan', '/usr/libexec/gsd-wwan', '/usr/libexec/gsd-wwan', '/usr/libexec/gsd-xsettings', '/usr/libexec/gsd-xsettings', '/usr/libexec/gsd-xsettings', '/usr/libexec/gsd-xsettings', '/usr/libexec/gsd-disk-utility-notify', '/usr/libexec/gsd-disk-utility-notify', '/usr/libexec/gsd-disk-utility-notify', '/usr/libexec/evolution-data-server/evolution-alarm-notify', '/usr/libexec/evolution-data-server/evolution-alarm-notify', '/usr/libexec/evolution-data-server/evolution-alarm-notify', '/usr/libexec/evolution-data-server/evolution-alarm-notify', '/usr/libexec/evolution-data-server/evolution-alarm-notify', '/usr/libexec/evolution-data-server/evolution-alarm-notify', '/usr/libexec/ibus-engine-simple', '/usr/libexec/ibus-engine-simple', '/usr/libexec/ibus-engine-simple', '/usr/libexec/gsd-printer', '/usr/libexec/gsd-printer', '/usr/libexec/gsd-printer', 'update-notifier', 'update-notifier', 'update-notifier', 'update-notifier', '/usr/libexec/gnome-terminal-server', '/usr/libexec/gnome-terminal-server', '/usr/libexec/gnome-terminal-server', '/usr/libexec/gnome-terminal-server', '/usr/libexec/gnome-terminal-server', 'bash', 'sudosu', 'su', 'bash', '[kworker/u256:0-events_freezable_power_]', '/usr/bin/python3/usr/bin/update-manager--no-update--no-focus-on-map', '/usr/bin/python3/usr/bin/update-manager--no-update--no-focus-on-map', '/usr/bin/python3/usr/bin/update-manager--no-update--no-focus-on-map', '/usr/bin/python3/usr/bin/update-manager--no-update--no-focus-on-map', '/usr/bin/python3/usr/bin/update-manager--no-update--no-focus-on-map', '[kworker/1:0-events]', '/usr/libexec/xdg-desktop-portal', '/usr/libexec/xdg-desktop-portal', '/usr/libexec/xdg-desktop-portal', '/usr/libexec/xdg-desktop-portal', '/usr/libexec/xdg-desktop-portal', '/usr/libexec/xdg-document-portal', '/usr/libexec/xdg-document-portal', '/usr/libexec/xdg-document-portal', '/usr/libexec/xdg-document-portal', '/usr/libexec/xdg-document-portal', '/usr/libexec/xdg-document-portal', '/usr/libexec/xdg-desktop-portal-gtk', '/usr/libexec/xdg-desktop-portal-gtk', '/usr/libexec/xdg-desktop-portal-gtk', '/usr/libexec/xdg-desktop-portal-gtk', '[kworker/0:0-events]', '[kworker/0:2-rcu_par_gp]', '/lib/systemd/systemd-udevd', '/lib/systemd/systemd-resolved', '/lib/systemd/systemd-journald', '/lib/systemd/systemd-timesyncd', '/lib/systemd/systemd-timesyncd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '/usr/lib/snapd/snapd', '[xfsalloc]', '[xfs_mru_cache]', '[jfsIO]', '[jfsCommit]', '[jfsCommit]', '[jfsSync]', '[kworker/1:1-cgroup_destroy]', '[kworker/u256:2-events_unbound]', '[kworker/u256:1-events_unbound]', '[kworker/1:2-events]', '[kworker/u256:3-events_unbound]', '/usr/lib/packagekit/packagekitd', '/usr/lib/packagekit/packagekitd', '/usr/lib/packagekit/packagekitd', '[kworker/0:1-events]', 'python3processes.py', 'xclip-selclip', "/bin/sh-cpsaH-A|awk'{for(i=5;i<NF;i++)printf$i;if(NF>=5)print$NF;}'|awk'NR>1'", 'psaH-A', 'awk{for(i=5;i<NF;i++)printf$i;if(NF>=5)print$NF;}', 'awkNR>1']


current_procs = os.popen("ps aH -A | awk '{for (i=5; i<NF; i++) printf $i " "; if (NF >= 5) print $NF; }' | awk 'NR>1'").read().split("\n")
if current_procs[-1] == '':
	current_procs = current_procs[:-1]

for proc in current_procs:
	if proc not in default_procs:
		print(f"Nondefault proc: {proc}")

		
		
		
print("\n")
print("printing non default /etc/rc* files: ")
print("")

default_rc = ['K01alsa-utils', 'K01avahi-daemon', 'K01bluetooth', 'K01cups-browsed', 'K01gdm3', 'K01irqbalance', 'K01kerneloops', 'K01open-vm-tools', 'K01openvpn', 'K01plymouth', 'K01pulseaudio-enable-autospawn', 'K01saned', 'K01speech-dispatcher', 'K01spice-vdagent', 'K01udev', 'K01unattended-upgrades', 'K01uuiddK01alsa-utils', 'K01avahi-daemon', 'K01bluetooth', 'K01cups', 'K01cups-browsed', 'K01gdm3', 'K01irqbalance', 'K01kerneloops', 'K01open-vm-tools', 'K01openvpn', 'K01pulseaudio-enable-autospawn', 'K01saned', 'K01speech-dispatcher', 'K01spice-vdagent', 'K01ufw', 'K01uuidd', 'K01whoopsieK01speech-dispatcher', 'S01acpid', 'S01anacron', 'S01apport', 'S01avahi-daemon', 'S01bluetooth', 'S01console-setup.sh', 'S01cron', 'S01cups', 'S01cups-browsed', 'S01dbus', 'S01gdm3', 'S01grub-common', 'S01irqbalance', 'S01kerneloops', 'S01open-vm-tools', 'S01openvpn', 'S01plymouth', 'S01pulseaudio-enable-autospawn', 'S01rsync', 'S01saned', 'S01spice-vdagent', 'S01unattended-upgrades', 'S01uuidd', 'S01whoopsieK01speech-dispatcher', 'S01acpid', 'S01anacron', 'S01apport', 'S01avahi-daemon', 'S01bluetooth', 'S01console-setup.sh', 'S01cron', 'S01cups', 'S01cups-browsed', 'S01dbus', 'S01gdm3', 'S01grub-common', 'S01irqbalance', 'S01kerneloops', 'S01open-vm-tools', 'S01openvpn', 'S01plymouth', 'S01pulseaudio-enable-autospawn', 'S01rsync', 'S01saned', 'S01spice-vdagent', 'S01unattended-upgrades', 'S01uuidd', 'S01whoopsieK01speech-dispatcher', 'S01acpid', 'S01anacron', 'S01apport', 'S01avahi-daemon', 'S01bluetooth', 'S01console-setup.sh', 'S01cron', 'S01cups', 'S01cups-browsed', 'S01dbus', 'S01gdm3', 'S01grub-common', 'S01irqbalance', 'S01kerneloops', 'S01open-vm-tools', 'S01openvpn', 'S01plymouth', 'S01pulseaudio-enable-autospawn', 'S01rsync', 'S01saned', 'S01spice-vdagent', 'S01unattended-upgrades', 'S01uuidd', 'S01whoopsieK01speech-dispatcher', 'S01acpid', 'S01anacron', 'S01apport', 'S01avahi-daemon', 'S01bluetooth', 'S01console-setup.sh', 'S01cron', 'S01cups', 'S01cups-browsed', 'S01dbus', 'S01gdm3', 'S01grub-common', 'S01irqbalance', 'S01kerneloops', 'S01open-vm-tools', 'S01openvpn', 'S01plymouth', 'S01pulseaudio-enable-autospawn', 'S01rsync', 'S01saned', 'S01spice-vdagent', 'S01unattended-upgrades', 'S01uuidd', 'S01whoopsieK01alsa-utils', 'K01avahi-daemon', 'K01bluetooth', 'K01cups-browsed', 'K01gdm3', 'K01irqbalance', 'K01kerneloops', 'K01open-vm-tools', 'K01openvpn', 'K01plymouth', 'K01pulseaudio-enable-autospawn', 'K01saned', 'K01speech-dispatcher', 'K01spice-vdagent', 'K01udev', 'K01unattended-upgrades', 'K01uuiddS01alsa-utils', 'S01apparmor', 'S01keyboard-setup.sh', 'S01kmod', 'S01plymouth-log', 'S01procps', 'S01selinux-autorelabel', 'S01udev', 'S01ufw', 'S01x11-common']

current_rc = os.popen("for dir in $(ls /etc/ | grep 'rc.\.d');do ls /etc/$dir | tr '\n' ' ' | sed 's/ $//';done").read().split(" ")

for file in current_rc:
	if file not in default_rc:
		print(file)		
		

		
print("\n\n")
print("Printing non default environment variables: ")
print("\n")

user_dic = {}
default_env = ['COLORTERM=truecolor', 'TERM=xterm-256color', 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin', 'DISPLAY=:0', 'LANG=en_US.UTF-8', 'XAUTHORITY=/run/user/1000/.mutter-Xwaylandauth.PTHQX1', 'LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:', 'MAIL=/var/mail/', 'LOGNAME=', 'USER=', 'HOME=/home/', 'SHELL=/bin/bash', 'SUDO_COMMAND=/usr/bin/printenv', 'SUDO_USER=root', 'SUDO_UID=0', 'SUDO_GID=0', '']

for user in allowed_users:
	user_dic[user] = os.popen(f"sudo -u {user} printenv | sed 's/{user}//g'").read()


for user in allowed_users:
	for i in user_dic[user].split():
		if i not in default_env:
			print(f"{user}\n")
			print(i)
			print("")
	print("")		

#with open("/etc/pam.d/common-password","w") as file:
#	file.write("""
#password	requisite			pam_pwquality.so retry=3 gecoscheck=1 minlen=12 maxrepeat=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 difok=4 reject_username enforce_for_root
#
#password	requisite			pam_pwhistory.so remember=13
#
#password	[success=1 default=ignore]	pam_unix.so obscure use_authtok try_first_pass sha512
#password	requisite			pam_deny.so
#password	required			pam_permit.so
#password	optional	pam_gnome_keyring.so
#""")
"""
max_days_len = int(os.popen("cat /etc/login.defs | grep '^PASS_MAX_DAYS' | awk '{print $2}' | tr -d '\\n' | wc -c").read())
os.system(f"sed -i 's/PASS_MAX_DAYS\\t{'.' * max_days_len}/PASS_MAX_DAYS\\t45/' /etc/login.defs")

min_days_len = int(os.popen("cat /etc/login.defs | grep '^PASS_MIN_DAYS' | awk '{print $2}' | tr -d '\\n' | wc -c").read())
os.system(f"sed -i 's/PASS_MIN_DAYS\\t{'.' * min_days_len}/PASS_MIN_DAYS\\t1/' /etc/login.defs")

warn_age_len = int(os.popen("cat /etc/login.defs | grep '^PASS_WARN_AGE' | awk '{print $2}' | tr -d '\\n' | wc -c").read())
os.system(f"sed -i 's/PASS_WARN_AGE\\t{'.' * warn_age_len}/PASS_WARN_AGE\\t7/' /etc/login.defs")
print("\n\n")
"""
#LAST THING
#print(Fore.BLUE + Back.WHITE + Style.BRIGHT +"Set users passwords (q to quit)")
#os.system("echo -e 'P@ssword123!\nP@ssword123!' | passwd root 1>/dev/null 2>/dev/null")
#os.system('e="echo"; r="read"; $e "user:"; $r p; $e "password:"; $r i; while [ $i != "q" ]; do $e -e "$p\n$p" | (passwd $i); $r i; done')
