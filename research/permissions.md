% Read permissions for /dev/hwrng

`/dev/hwrng` is created at boot time with these default permissions:

    crw------- 1 root root 10, 183 Mar 18 18:32 /dev/hwrn

So, to allow all users to read from this device, do *one* of the following:

1. Add the following line to `/etc/rc.conf` just above the last line `exit 0`:

        chmod a+r /dev/hwrng

2. Add the following cronjob to `/etc/crontab`:

        @reboot         root    chmod a+r /dev/hwrng

# Acknowledgements

    From: https://sites.google.com/site/astudyofentropy/project-definition/raspberry-pi-internal-hardware-random-number-generator
    Date: 2020-03-22
