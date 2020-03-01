## Software Configuration
### Configuration Files
The SlimPi configuration is managed through the following three files which are loaded sequentially each superceeding the previous files. 

1. `./slimpi/slimpi.cfg` Basic default configuration file; this should not be edited
2. `/etc/slimpi.cfg` System-wide configuration file; this can be used to set any system-wide default settings
3. `~/.config/com.txoof.slimpi/slimpi.cfg` User level configuration file; this will be ignored when running as a daemon 
    * Required settings that must be configured in either `/etc/slimpi.cfg` or `~/.config/com.txoof.slimpi/slimpi.cfg`:
        - `display = waveShareEPDType`
        - example: `display = epd5in83`
            * The display type should match the model number of your e-Paper display
        - `player_name = "Name Of LMS Player on Local Network"` 
        - example: `player_name = slimpi`
            * The player name can be found by running `slimpi --list-servers`:
            
        ```
        slimpi --list-servers

        Scanning for available LMS Server and players
        servers found:
        [{'host': '192.168.178.9', 'port': 9000}]

        players found:
        name: Chilab'le <---player_name
        playerid: 00:04:20:07:e6:44
        modelname: Squeezebox Classic


        players found:
        name: slimpi <---player_name
        playerid: dc:a6:32:29:99:f0
        modelname: SqueezeLite   
        ```

### Configure as a System Process
SlimPi can run as a system process that starts at boot and runs in the background. 

1. Download and decompress [`slimpi_latest.tgz`](https://github.com/txoof/slimpi_epd/raw/master/slimpi_latest.tgz)
2. Run the included `install.sh` script
    * This script will attempt to install slimpi as a daemon process that starts at boot
        * `sudo install.sh`
3. Configure slimpi for your Logitech Media Server and e-Paper display
    * Set `player_name = ` and `display = ` settings in /etc/slimpi.cfg (see [Configuration Files](# Configuration_Files) above

### Configure HiFiBerry *(optional)*
A HiFiBerry DAC+ or similar can be used for audio output. HiFiBerry has a [great guide for configuring Linux 4 kernels](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/)

The quick and dirty version can be found below
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
    * Additional squeezelite arguments such as resampling rates can be passed here as well - for a complete list see `$man squeezelite`

### Disable Raspberry Pi Lights *(optional)*
To disable the activity and power lights on Pi 3 and use the included systemd service and scripts to disable the lights. This will automatically disable the lights at boot. The LEDs will remain off as long as this service is active.
```
$ sudo ./install/install_led_ctl.sh
```
The `install_led_ctl.sh` script creates the systemd `led_ctl.service` and copies the `led_ctl` script to `/usr/bin/`.

To temporarily enable the LEDs (until next reboot) use:
```
$ sudo systemctl stop led_ctl.service
```
or 
```
# enable the LEDS
$ /usr/bin/led_ctl on
# disable the LEDS
$ /usr/bin/led_ctl off
```


To permenantly re-enable the LEDs use:
```
$ sudo systemctl disable led_ctl.service 
```
To permenantly remove the service and the scripts:
```
$ sudo systemctl disable led_ctl.service
$ sudo rm /usr/bin/led_ctl
$ sudo rm /etc/systemd/system/led_ctl.service
```


```python
%alias mdconvert mdconvert Software_Configuration.ipynb
%mdconvert
```

    [NbConvertApp] Converting notebook Software_Configuration.ipynb to markdown



```python

```
