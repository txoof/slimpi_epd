## System Setup
SlimPi and the WaveShare display requries that SPI is enabled on the Raspberry Pi and the user running SlimPi is a member of the GPIO and SPI groups
* Enable SPI
    * `sudo raspi-config` Interfacing Options > SPI > Would you Like the SPI interface to be enabled > Yes
* `usermod -a -G spi,gpio <current user>`

### Configure HiFiBerry *(optional)*
A HiFiBerry DAC+ or similar can be used for audio output. HiFiBerry has a [great guide for configuring Linux 4 kernels](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/)

#### Quick and Dirty Configuration
1. Disable onboard sound in `/boot/config.txt` 
    * `#dtparam=audio=on`
2. Load deviced tree overlay for HiFiBerry in `/boot/config.txt`
    * `dtoverlay=hifiberry-dacplus`
3. Configure ALSA output *(optional)*
    * Check that there is not a conflicing `.asound.conf` file in `~/`
    * Create `/etc/asound.conf` and include the following:
    ```
    pcm.!default {
    type hw card 0
    }
    ctl.!default {
    type hw card 0
    }
    ```
    
### Install and Configure Squeeze Lite *(optional)*
Squeezelite is a light-weight headless Squeezebox LMS player that works well with a HiFiBerry.

* Install squeezelite package: `$ sudo apt-get install squeezelite`
* Squeezelite uses the hostname as its default name to change the name do one of the following:
    * Change the hostname:
        1. `$ raspi-config` Network Options > Hostname
        2. Edit `/etc/default/squeezelite` and edit `SL_NAME=YOUR_NAME_HERE`
    * Additional squeezelite arguments such as resampling rates can be passed here as well - for a complete list see `man squeezelite`


```python
%alias mdconvert mdconvert System_Setup.ipynb
%mdconvert
```

    [NbConvertApp] Converting notebook System_Setup.ipynb to markdown



```python

```
