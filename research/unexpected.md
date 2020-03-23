% "Well, that was unexpected...": The Raspberry Pi's Hardware Random Number Generator

    From: http://scruss.com/blog/2013/06/07/well-that-was-unexpected-the-raspberry-pis-hardware-random-number-generator/
    Date: 2020-03-22

Most computers can’t create true random numbers. They use a formula
which makes a very long stream of pseudo-random numbers, but real
randomness comes from thermal noise in analogue components. The Raspberry
Pi has such a circuit in its SoC, as it helps making the seed data for
secure transactions. It was only recently that a driver for this circuit
was supplied. To enable it (on Raspbian): I think the module is enabled
by default now for the different versions of the SoC.

1. Make sure your system is up to date with

        sudo apt-get update
        sudo apt -y upgrade

2. Install the module:

        sudo modprobe bcm2708-rng

3. To make sure it’s always loaded, add the following line to `/etc/modules` (editing as root):

        bcm2708-rng

4. For some RNG-related stuff, install rng-tools:

        sudo apt-get install rng-tools

The `/dev/hwrng` device should now be available, but can only be read by the root user.


[Nico](https://www.nico-maas.de/?p=1562) pointed out that you also need to:

1. Edit /etc/default/rng-tools, and remove the # at the start of the line

        HRNGDEVICE=/dev/hwrng

2. Restart rng-tools with

        sudo service rng-tools restart


## What random looks like

Random data look pretty dull. Here are random RGB values made with:

    sudo cat /dev/hwrng  | rawtoppm -rgb 256 256 | pnmtopng > random$(date +%Y%m%d%H%M%S).png

(you’ll need to install the netpbm toolkit to do this.)

![Random RGB image from `/dev/hwrng`](random.png "Random RGB image from /dev/hwrng")
