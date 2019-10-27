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

- Python Libraries -- install with pip
  * RPi.GPIO
  * spidev
  * Pillow
- WaveShare -- not sure best way to manage yet
  * epd-library: epd-library

