---
layout: post
title:  "Using LVM Snapshots"
date:   2014-06-02 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# A not so known feature that really is useful.

As a system administrator, I daily use snapshots, either for backing up or to ensure a way to rollback when things might go nasty.

The system on which we will run the following things has some free space in the volgroup Volgroup.
Now we’ll create a specific logical volume called productiondata in which we’ll add some very important data:

## Creating a 1GB volume called “productiondata”

```bash
lvcreate -L1G -n productiondata VolGroup
	  Logical volume "productiondata" created
mkfs.ext3 /dev/mapper/VolGroup-productiondata
	mke2fs 1.41.12 (17-May-2010)
	Filesystem label=
	OS type: Linux
	Block size=4096 (log=2)
	Fragment size=4096 (log=2)
	Stride=0 blocks, Stripe width=0 blocks
	65536 inodes, 262144 blocks
	13107 blocks (5.00%) reserved for the super user
	First data block=0
	Maximum filesystem blocks=268435456
	8 block groups
	32768 blocks per group, 32768 fragments per group
	8192 inodes per group
	Superblock backups stored on blocks:
		32768, 98304, 163840, 229376

	Writing inode tables: done
	Creating journal (8192 blocks): done
	Writing superblocks and filesystem accounting information: done

	This filesystem will be automatically checked every 21 mounts or
	180 days, whichever comes first.  Use tune2fs -c or -i to override.
mkdir /mnt/productiondata
mount /dev/mapper/VolGroup-productiondata /mnt/productiondata/
```

## Creating some important data inside it

```bash
cd /mnt/productiondata/
for i in {1..10}; do date > $i.txt; done
ll
	total 56
	-rw-r--r--. 1 root root    30 May 23 15:31 10.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 1.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 2.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 3.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 4.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 5.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 6.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 7.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 8.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 9.txt
	drwx------. 2 root root 16384 May 23 15:29 lost+found
```

## Creating a snapshot and working with it

Now, create a snapshot of 512MB size

```bash
lvcreate -L512M -s -n productiondatabackup /dev/mapper/VolGroup-productiondata
  Logical volume "productiondatabackup" created
lvdisplay
  --- Logical volume ---
  LV Path                /dev/VolGroup/productiondata
  LV Name                productiondata
  VG Name                VolGroup
  LV UUID                BLcHEd-kjde-BpOq-IbOT-1rBc-1B7t-SeNUUa
  LV Write Access        read/write
  LV Creation host, time localhost.localdomain, 2014-05-23 15:28:33 +0200
  LV snapshot status     source of
                         productiondatabackup [active]
  LV Status              available
  # open                 1
  LV Size                1.00 GiB
  Current LE             256
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:2

  --- Logical volume ---
  LV Path                /dev/VolGroup/productiondatabackup
  LV Name                productiondatabackup
  VG Name                VolGroup
  LV UUID                O3dFho-eFIc-GfV1-MIgP-CryF-JKwp-tmzY1r
  LV Write Access        read/write
  LV Creation host, time localhost.localdomain, 2014-05-23 15:33:11 +0200
  LV snapshot status     active destination for productiondata
  LV Status              available
  # open                 0
  LV Size                1.00 GiB
  Current LE             256
  COW-table size         512.00 MiB
  COW-table LE           128
  Allocated to snapshot  0.00%
  Snapshot chunk size    4.00 KiB
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:3
```

Add some more data to productiondata

```bash
for i in {100..110}; do date > $i.txt; done
ll
	total 100
	-rw-r--r--. 1 root root    30 May 23 15:34 100.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 101.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 102.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 103.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 104.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 105.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 106.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 107.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 108.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 109.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 10.txt
	-rw-r--r--. 1 root root    30 May 23 15:34 110.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 1.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 2.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 3.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 4.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 5.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 6.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 7.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 8.txt
	-rw-r--r--. 1 root root    30 May 23 15:31 9.txt
	drwx------. 2 root root 16384 May 23 15:29 lost+found
```

Let’s mount the snapshot to see what’s inside

```bash
mount /dev/mapper/VolGroup-productiondatabackup /mnt/productiondatabackup/
ll /mnt/productiondatabackup/
total 56
- -rw-r--r--. 1 root root    30 May 23 15:31 10.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 1.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 2.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 3.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 4.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 5.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 6.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 7.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 8.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 9.txt
drwx------. 2 root root 16384 May 23 15:29 lost+found
```

Everything's fine so we’re going to delete the snapshot

```bash
umount /mnt/productiondatabackup
lvremove /dev/mapper/VolGroup-productiondatabackup
Do you really want to remove active logical volume productiondatabackup? [y/n]: y
  Logical volume "productiondatabackup" successfully removed
ll /mnt/productiondata
total 100
- -rw-r--r--. 1 root root    30 May 23 15:34 100.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 101.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 102.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 103.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 104.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 105.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 106.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 107.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 108.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 109.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 10.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 110.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 1.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 2.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 3.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 4.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 5.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 6.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 7.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 8.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 9.txt
drwx------. 2 root root 16384 May 23 15:29 lost+found
```

## Rollback in case of somethings wrong

```bash
lvcreate -L512M -s -n productiondatabackup /dev/mapper/VolGroup-productiondata
for i in *.txt; do echo "major fuckup" > $i; done
lvconvert --merge /dev/VolGroup/productiondatabackup
  Cannot merge over open origin volume
  Merging of snapshot productiondatabackup will start next activation.
cd
umount /dev/VolGroup/productiondata
lvchange -an /dev/VolGroup/productiondata
lvchange -ay /dev/VolGroup/productiondata
mount /dev/VolGroup/productiondata /mnt/productiondata
ll /mnt/productiondata
total 100
- -rw-r--r--. 1 root root    30 May 23 15:34 100.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 101.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 102.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 103.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 104.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 105.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 106.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 107.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 108.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 109.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 10.txt
- -rw-r--r--. 1 root root    30 May 23 15:34 110.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 1.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 2.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 3.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 4.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 5.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 6.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 7.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 8.txt
- -rw-r--r--. 1 root root    30 May 23 15:31 9.txt
drwx------. 2 root root 16384 May 23 15:29 lost+found
cat /mnt/productiondata/1.txt
Fri May 23 15:31:51 CEST 2014
```

Reverted ! Please note that the snapshot is GONE, before doing crap again, please create another

What happens if we allocate more than the snapshot size ? (512MB here)

```bash
dd if=/dev/zero of=/mnt/productiondata/fat.file bs=1M count=513
513+0 records in
513+0 records out
537919488 bytes (538 MB) copied, 8.83559 s, 60.9 MB/s
```

Here’s the extract of the logs:

```log
/dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 1073676288: Input/output error
/dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 1073733632: Input/output error
/dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 0: Input/output error
/dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 4096: Input/output error
```

Don’t worry, you are still able to write on your original volume

```bash
touch test
```

But the snapshot is unusable

```bash
mount /dev/mapper/VolGroup-productiondatabackup /mnt/productiondatabackup/
mount: you must specify the filesystem type
lvremove /dev/mapper/VolGroup-productiondatabackup
  /dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 1073676288: Input/output error
  /dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 1073733632: Input/output error
  /dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 0: Input/output error
  /dev/VolGroup/productiondatabackup: read failed after 0 of 4096 at 4096: Input/output error
Do you really want to remove active logical volume productiondatabackup? [y/n]: y
  Logical volume "productiondatabackup" successfully removed
```

To avoid getting in this situation (not being able to rollback), please make sure that you have enough space for what you intend to do. You should monitor the snapshot usage rate by looking at the ‘Allocated to snapshot’ line in lvdisplay output.