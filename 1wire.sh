mkdir /mnt/1wire

/opt/owfs/bin/owfs --i2c=ALL:ALL --allow_other /mnt/1wire/
sleep 1
cd /mnt/1wire/ 
sleep 1
ls -la
sleep 1
killall owfs
umount /mnt/1wire 