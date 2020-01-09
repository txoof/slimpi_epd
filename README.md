# Table of Contents
* [Introduction] (#Introduction)
* [Setup Python Environment] (#Setup Python Environment)

## Introduction
Stuff, things



## Configure HiFi Berry
See [HiFi Berry guide](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/)
- disable onboard sound in /boot/config.txt
  * `#dtparam=audio=on`
- add load device tree overlay file in /boot/config.txt
  * `dtoverlay=hifiberry-dacplus`
- configure ALSA by creating /etc/asound.conf
```
pcm.!default {
  type hw card 0
}
ctl.!default {
  type hw card 0
}
```
 * make sure no .asound.conf file exists in user home directory

## Setup Python Environment
### Requirements
- Debian Packages -- install with apt
  * libtiff5-dev libopenjp2-7-dev

- Python Libraries -- install with pipenv
  * RPi.GPIO
  * spidev
  * Pillow
- WaveShare -- not sure best way to manage yet install with pipenv -- this is a fork of the library with the RaspberryPi directory renamed to remove the ampersand (&) character
  * `pipenv install -e "git+https://github.com/txoof/e-Paper.git#egg=waveshare-epd&subdirectory=RaspberryPi_and_JetsonNano/python/"`


## Notes & Useful Links
[Pi Pinout](https://pinout.xyz/pinout/pin1_3v3_power)
