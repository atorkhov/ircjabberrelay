# appliance-creator -c fedora-ircjabberrelay.ks -t /mnt/data2/tmp --cache=/mnt/data2/live/17 --verbose -n fedora-ircjabberrelay

# Kickstart file to build the appliance operating
# system for fedora.
# This is based on the work at http://www.thincrust.net
lang C
keyboard us
timezone Europe/Moscow
auth --useshadow --enablemd5
selinux --disabled
firewall --disabled
bootloader --timeout=1 --append="acpi=force"
network --bootproto=dhcp --device=eth0 --onboot=on
services --enabled=network --enabled=ircjabberrelay

# Uncomment the next line
# to make the root password be thincrust
# By default the root password is emptied
#rootpw --iscrypted $1$uw6MV$m6VtUWPed4SqgoW6fKfTZ/

#
# Partition Information. Change this as necessary
# This information is used by appliance-tools but
# not by the livecd tools.
#
part biosboot --fstype=biosboot --size=1 --ondisk sda
part / --size 1024 --fstype ext4 --ondisk sda

#
# Repositories
#
#repo --name=rawhide --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=rawhide&arch=$basearch
repo --name=fedora --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=fedora-$releasever&arch=$basearch
repo --name=updates --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f$releasever&arch=$basearch
#repo --name=updates-testing --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-testing-f$releasever&arch=$basearch
repo --name=local --baseurl=file:///home/alex/repo/17

#
# Add all the packages after the base packages
#
%packages --excludedocs --instLangs=C --nobase
bash
kernel
grub2
e2fsprogs
passwd
rootfiles
yum
vim-minimal
acpid
#needed to disable selinux
lokkit

#Allow for dhcp access
dhclient
iputils

python-ircjabberrelay

#
# Packages to Remove
#

# no need for kudzu if the hardware doesn't change
-kudzu
-prelink
-setserial
-ed

# Remove the authconfig pieces
-authconfig
-rhpl
-wireless-tools

# Remove the kbd bits
-kbd
-usermode

# these are all kind of overkill but get pulled in by mkinitrd ordering
-mkinitrd
-kpartx
-dmraid
-mdadm
-lvm2
-tar

# selinux toolchain of policycoreutils, libsemanage, ustr
-policycoreutils
-checkpolicy
-selinux-policy*
-libselinux-python
-libselinux

# Things it would be nice to loose
-fedora-logos
generic-logos
-fedora-release-notes
%end

#
# Add custom post scripts after the base post.
#
%post

ln -sf /usr/lib/systemd/system/multi-user.target /etc/systemd/system/default.target
sed -i -e '/GRUB_TIMEOUT/s/5/1/' /etc/default/grub
sed -i -e '/timeout/s/5/1/' /boot/grub2/grub.cfg
cat > /etc/ircjabberrelay/config.py <<EOF
IGNORE_LIST_FILEPATH = '/etc/ircjabberrelay/ignore'

cfg = {
    'ircchannel': '#channel',
    'ircnick': 'bot',
    'ircserver': 'irc.freenode.net',
    'ircport': 6667,

    'jabberjid': 'jid@jabber.ru/bot',
    'jabberpass': 'xxxxxxxx',
    'jabberchannel': 'channel',
    'jabbernick': 'bot',
    'jabberserver': 'conference.jabber.ru'
}
EOF

%end

