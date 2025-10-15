# AIX Admin Cheatsheet

A fast, practical reference for IBM AIX (7.x focused). Use `smitty` for guided steps and the **SMIT fast paths** below for speed. Commands generally require root unless noted.

---

## System Basics
- Show OS/ML/TL:  
  ```sh
  oslevel -s            # e.g., 7200-05-05-2148
  oslevel -r            # Recommended maintenance level
  ```
- Kernel/uname:  
  ```sh
  uname -a              # Kernel, hostname, hardware
  bootinfo -K           # Kernel mode (32/64)
  ```
- Time/locale:  
  ```sh
  date; lsattr -El sys0 | grep -i time
  locale; chtz 'Asia/Manila'
  ```
- Filesets & packages:  
  ```sh
  lslpp -L              # List installed filesets
  lslpp -L | grep APAR  # Find APAR
  installp -acgXd <dev_or_dir> <fileset>  # Install/update
  emgr -l               # Emergency fixes (eFix)
  inutoc .              # Build .toc in install dir
  ```

## Users & Groups
- Manage accounts:  
  ```sh
  lsuser -a ALL <user>
  mkuser pgrp=staff home=/home/alice alice
  chuser login=false alice
  rmuser alice
  mkgroup staff; chgrp staff /path
  passwd <user>
  ```
- Limits & auth:  
  ```sh
  lssec -f /etc/security/limits -s default -a fsize
  chsec -f /etc/security/limits -s default -a fsize=-1
  lslogin; chuser login=true bob
  ```

## Devices & ODM
- Device inventory / configs:  
  ```sh
  lsdev -Cc disk|tape|adapter|if
  lsdev -C | grep Available
  lsattr -El hdisk0; lsattr -E -l en0
  chdev -l en0 -a mtu=9000 -P   # -P = next reboot
  chdev -l en0 -a mtu=9000      # live if supported
  cfgmgr -v                     # Probe and configure
  odmget -q "name='en0'" CuAt   # Query ODM
  ```

## Boot, Init, SRC (Subsystem Resource Controller)
- Boot controls:  
  ```sh
  bootlist -m normal -o
  bootlist -m normal hdisk0 hdisk1
  bosboot -ad /dev/hdisk0        # Rebuild boot image
  ```
- Runlevels & services:  
  ```sh
  who -r
  lssrc -a                       # List SRC subsystems
  startsrc -s inetd; stopsrc -s inetd; refresh -s inetd
  mkssys -s mysvc -p /usr/bin/mysvc -u 0 -S -n 15 -f 9 -a "-D"
  rmssys -s mysvc
  ```
- Logging:  
  ```sh
  alog -f /var/adm/ras/bootlog -o
  errpt -a | more                # Detailed error report
  errclear 0                     # Clear error log (caution)
  ```

## Filesystems (JFS2) & Storage (LVM)
- Quick view:  
  ```sh
  df -g; lsfs -q; mount; lsvg; lspv; lslv <lv>
  ```
- Create / extend FS (JFS2):  
  ```sh
  crfs -v jfs2 -g datavg -m /data -A yes -p rw -a size=10G
  chfs -a size=+5G /data
  mount /data; umount /data
  lsfs /data; fuser -cu /data    # Processes using FS
  ```
- LVM basics:  
  ```sh
  lspv                        # PVs
  lspv -l hdisk1              # LVs on a PV
  mkvg -y datavg hdisk1
  extendvg datavg hdisk2
  mkllog -f jfs2 datavg       # JFS2 log LV if needed
  mklv -t jfs2 -y datalv datavg 10    # in LPs
  crfs -v jfs2 -d /dev/datalv -m /data -A yes
  rmlv datalv; reducevg datavg hdisk2; exportvg datavg
  ```
- Snapshots (JFS2):  
  ```sh
  snapshot -o snapfrom=/data -n datasnap
  snapshot -o list -n datasnap
  snapshot -o unsnap -n datasnap
  ```
- Mirroring & striping:  
  ```sh
  mklvcopy datalv 2 datavg       # Mirror LV (2 copies)
  rmlvcopy datalv 1              # Remove a copy
  mklv -S -t jfs2 -y stripe1 datavg 10 2   # striped
  ```

## Disks, MPIO, SAN
- Pathing & health:  
  ```sh
  lspath; lspath -l hdisk3 -H
  chpath -l hdisk3 -p fscsi0 -s enable
  lsattr -El hdisk3 | grep PCM   # Path control module
  fcstat fcs0; lsdev -Cc adapter
  ```

## Network
- Interfaces & routes:  
  ```sh
  ifconfig -a
  ifconfig en0 192.168.1.10 netmask 255.255.255.0 up
  lsattr -El inet0 | egrep 'hostname|route'
  netstat -rn; route add -net 0.0.0.0/0 192.168.1.1
  no -a | more                   # Sockets tunables
  chdev -l en0 -a jumbo_frames=yes
  ```
- DNS / NTP:  
  ```sh
  cat /etc/resolv.conf; lsattr -El inet0 | grep dns
  lssrc -s xntpd; startsrc -s xntpd
  ```

## Performance & Monitoring
- CPU/Mem/IO/Net:  
  ```sh
  topas; nmon
  vmstat 2 5; svmon -G
  iostat -D 2 3; iostat -dT 2 3
  sar -u 2 5; sar -d 2 5; sar -n DEV 2 5
  netstat -v en0; entstat -d ent0
  filemon -O all -o /tmp/filemon.out -T 30; formon -i /tmp/filemon.out
  traceroute <host>; ping -c 3 <host>
  ```

## Tuning (AIX tunables)
- Using tunable commands:  
  ```sh
  vmo -a     # Virtual memory
  ioo -a     # I/O tuning
  no -a      # Network options
  nfso -a    # NFS options
  vmo -o minperm%=3 -o maxperm%=90 -p    # -p persistent
  ```

## Security & Auditing
- Audit:  
  ```sh
  lsaudit; chlaud
  audit start; audit stop
  ```
- Firewall (IPSec/IPFilter depends on TL/edition):  
  ```sh
  lssrc -a | grep ipsec
  lsconf | grep -i ipsec
  ```

## Backups, Migrations & DR
- mksysb (rootvg backup):  
  ```sh
  mksysb -i /backup/mksysb_$(date +%F).bff
  restore -T -qf /backup/mksysb_YYYY-MM-DD.bff  # List
  ```
- alt_disk_install (alt clones):  
  ```sh
  alt_disk_copy -d hdisk1
  alt_rootvg_op -X                      # Cleanup
  ```
- NIM (Network Install Manager):  
  ```sh
  lsnim -l; nimclient -C
  nim -o define -t lpp_source ...
  nimadm -j nimvg -s lppsrc -d hdisk1 -Y  # AIX migration
  ```

## VIOS (if using PowerVM / vio servers)
- On VIOS (padmin):  
  ```sh
  lsmap -all; lsmap -vadapter vhost0
  mkvdev -vdev hdisk3 -vadapter vhost0 -dev vtscsi3
  rmvdev -vtd vtscsi3
  lssea; chdev -dev ent0 -attr jumbo_frames=yes
  oem_setup_env   # Root shell (use sparingly)
  ```

## SMITTY Fast Paths (handy)
- Storage & FS:  
  - `smitty vg` (Volume Groups), `smitty lv`, `smitty fs`, `smitty jfs2`
  - `smitty chjfs2` (change FS), `smitty crjfs2` (create FS)
- Devices & Network:  
  - `smitty devices`, `smitty tcpip`, `smitty inet`
- Backup & Install:  
  - `smitty mksysb`, `smitty installp`, `smitty nim`
- Performance/Logs:  
  - `smitty perf`, `smitty errlog`, `smitty src`
- Security:  
  - `smitty user`, `smitty group`, `smitty audit`

## Troubleshooting Playbook (quick checks)
1. **Health**: `errpt | head`, `lssrc -a | grep inoperative`
2. **Space**: `df -g`, `du -sm /* 2>/dev/null | sort -n | tail`
3. **Memory**: `svmon -G | head`, `vmstat 2 5`
4. **Disks**: `lspath`, `iostat -D 2 3`, `lsvg -p <vg>`
5. **Network**: `netstat -rn`, `entstat -d ent0 | egrep 'Errors|CRC'`
6. **Filesets**: `lslpp -L | grep -i <name>`
7. **Reboot safety**: `bootlist -m normal -o`, `lsvg -o`, `quorum? lsvg rootvg`

## Handy One‑liners
```sh
# Top 10 CPU users (requires ps/awk)
ps aux | head -1; ps aux | sort -nrk 3 | head

# Find big files > 1GB, exclude NFS
find / \( -fstype jfs2 -o -fstype jfs \) -size +1024M -exec ls -lh {} \; 2>/dev/null

# Trace which files a PID uses
truss -p <PID> -f -rall -wall -o /tmp/truss.<PID>.out

# Check multipath states for all disks
for d in $(lspv | awk '{print $1}'); do echo "=== $d ==="; lspath -l $d; done
```

## Common Paths & Files
- Logs: `/var/adm/ras/*`, `/var/log/*`, `/var/adm/syslog`
- Configs: `/etc/inittab`, `/etc/objrepos/*` (ODM), `/etc/filesystems` (FS table)
- Network: `/etc/hosts`, `/etc/resolv.conf`, `/etc/netsvc.conf`
- Startups: `/etc/rc.tcpip`, `/etc/rc.nfs`, `/etc/rc.local`

## Safety Notes
- Prefer `smitty` to auto‑update ODM and configs safely.
- Use `-P` for deferred changes when supported; test first.
- For boot changes (`bosboot`, `bootlist`), double‑check disk IDs.
- Keep recent `mksysb` and consider `alt_disk_copy` before risky ops.

---



## Adding Disks and Extending Partitions (Step-by-Step)

### 1. Identify New Disks
After adding a new LUN or virtual disk from the SAN or VIOS, run:
```sh
cfgmgr -v                   # Detect new devices
lsdev -Cc disk              # List all disks
lspv                        # Show which disks belong to volume groups
```
Example output might show a new `hdisk3` as "None" (not in a VG).

### 2. Add Disk to a Volume Group
If the disk is new and available:
```sh
extendvg datavg hdisk3
```
- `datavg` = target VG name  
- Run `lsvg -p datavg` to confirm the disk was added successfully.

If the disk belongs to another VG, clear its metadata first:
```sh
reducevg -df <vgname> hdisk3   # forcibly remove from old VG
```
Then re-add to your target VG.

### 3. Create a New Logical Volume (LV)
To create a 10GB logical volume on the new disk:
```sh
mklv -t jfs2 -y data_lv datavg 10G
lslv data_lv
```

### 4. Create a New Filesystem on the LV
```sh
crfs -v jfs2 -d /dev/data_lv -m /data -A yes -p rw -a logname=INLINE
mount /data
```
Verify:
```sh
df -g | grep /data
```

### 5. Extend an Existing Filesystem
To grow an existing FS (`/data`) by 20GB:
```sh
chfs -a size=+20G /data
df -g /data
```
If the VG has free PPs on multiple disks, AIX will allocate automatically.

### 6. Check VG and FS Capacity
```sh
lsvg datavg
lsvg -p datavg
lslv data_lv
lsfs -q /data
```

### 7. Verify Persistence
Ensure `/etc/filesystems` contains the updated mount entry and that it’s set to mount automatically:
```
/data:
        dev             = /dev/data_lv
        vfs             = jfs2
        log             = INLINE
        mount           = true
        options         = rw
        account         = false
```

### 8. Optional — Mirror or Move LVs
- Mirror LV to another disk:
  ```sh
  mklvcopy data_lv 2 datavg
  syncvg -l data_lv
  ```
- Move LV to another disk (rebalancing):
  ```sh
  migratepv hdisk2 hdisk3
  ```

---




## WPAR Storage Extension (System & Application WPARs)

### 1. Identify the WPAR
```sh
lswpar
lswpar -L mywpar
```
Check if it’s **system** (full OS environment) or **application** (process-based).

### 2. Add a Filesystem from Global to WPAR
From the global AIX instance:
```sh
mkwpar -n mywpar -B /backup/wpar -D rootvg=yes
chwpar -N address=192.168.10.50 -N interface=en0 mywpar
```

To mount a new directory or FS inside the WPAR:
```sh
chwpar -M "source=/data,wparpath=/data,options=rw" mywpar
```
This shares `/data` from the global environment into the WPAR.

If you created a new LV for WPAR use:
```sh
crfs -v jfs2 -d /dev/data_lv -m /data -A yes
mount /data
chwpar -M "source=/data,wparpath=/data,options=rw,fs=jfs2" mywpar
```

### 3. Extend WPAR Filesystem
From the global zone (since WPAR FSs reside under `/wpars/<wparname>`):
```sh
lsvg rootvg
df -g /wpars/mywpar
chfs -a size=+10G /wpars/mywpar
```

### 4. Verify Inside WPAR
```sh
clogin mywpar
df -g
lsvg -o
```

---

## PowerVM SEA Disk Mapping and Virtual I/O Management

### 1. On VIOS (padmin shell)
List all virtual adapters and their mappings:
```sh
lsmap -all
lsmap -vadapter vhost0
```
View physical adapters and SEAs:
```sh
lsdev -type adapter
lsdev -type sea
lsattr -El entX | grep ha_mode
```

### 2. Map Physical Disk to Client LPAR
```sh
mkvdev -vdev hdisk3 -vadapter vhost0 -dev vtscsi3
lsmap -vadapter vhost0
```
This maps `hdisk3` (on VIOS) to `vtscsi3`, visible in the client LPAR as a new disk.

### 3. Remove Disk Mapping
```sh
rmvdev -vtd vtscsi3
```

### 4. Create a Shared Ethernet Adapter (SEA)
```sh
mkvdev -sea ent0 -vadapter ent1 -default ent1 -defaultid 1
```
- `ent0` = physical adapter (uplink)
- `ent1` = virtual adapter to client VLAN

Set attributes:
```sh
chdev -l entX -a ha_mode=sharing -a jumbo_frames=yes -P
```

### 5. SEA Failover and Redundancy
For dual VIOS (active/passive):
```sh
entstat -d entX | grep Priority
chdev -l entX -a ha_mode=auto -a ctl_chan=entY -a virt_adapters=ent1 -P
```
- Use `ctl_chan` for control channel between VIOS pairs.

### 6. Verify From Client LPAR
Inside client (AIX):
```sh
cfgmgr
lsdev -Cc disk
lspv
```
Disk mapped from VIOS should now appear as an available hdisk.

---


### Version
Generated: 2025-10-15
