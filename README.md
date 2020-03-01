# SlimPi 
## ePaper based Logitech Media Player Display
For complete build instructions and links to a spiffy case, head over to the [Project Log at Hackaday.io](https://hackaday.io/project/170051-slimpi).
<img width="300" src="./docs/SlimPi_splash.png">

SlimPi provides a Logitech Media Player display using a [WaveShare e-Paper display](https://www.waveshare.com/product/oleds-lcds/e-paper.htm) and a Raspberry Pi.

<img width="500" src="./docs/Slim_Pi-in_action.jpg">

- [Features](#features)
- [Quick Install](#quick-install)
- [Requirements](#requirements)
  * [Required Hardware](#required-hardware)
  * [Optional Hardware](#optional-hardware)
  * [Required Software](#required-software)
  * [Opational Software](#opational-software)
- [System Setup](./docs/System_Setup.md)
- [Software Configuration](./docs/Software_Configuration.md)
- [Hardware Setup](./docs/Hardware_Setup.md)
- [Building SlimPi](./docs/Building.md)
- [Screen Layouts](./docs/Screen_Layouts.md)
- [Plugin Modules](./docs/Plugin_Modules.md)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Features

SlimPi provides a *now playing* display for a selected Logitech Media Player. When the player is paused, an alternative screen is displayed.

<img width="500" src="./docs/SlimPi_playing.png"></img>

Display includes: 
* Track Title
* Artist Name
* Album Name
* Album Artwork (if available)
* Now Playing Mode: e.g. play, stop, pause

When the music is paused, the display shows an alternative screen.

**Word Clock** (default)

<img width="200" src="./docs/SlimPi_wordclock.png">

**Clock**

<img width="200" src="./docs/SlimPi_clock.png">

**Binary Clock**

<img width = "200" src="./docs/SlimPi_binary_clock.png">

The refresh rate of HAT compatable waveshare displays is relatively slow (5-20 seconds) and does not support partial refreshes. This results in the display pulsing between an all-white and all-black state several times during each refresh. 

To limit the visual disturbance of a pulsing screen, the default clock is the Word Clock with a refresh rate of around 5 minutes.


## Software Quick Install
If you have a working EPD installed, the following instructions will get you up and runing quickly. If you do not yet have a working screen installed, check the Hardware Setup instructions below.
1. Download the installable package from [git hub](https://github.com/txoof/slimpi_epd/raw/master/slimpi_latest.tgz)
2. Decompress the tarball: `tar xvzf slimpi_latest.tgz`
3. Run the installer: 
   * `install.sh` for a daemon that starts automatically at boot, or see below for running in user space
   * `user_install.sh` to setup the user space configuration files
4. Edit the appropriate configuation file: `/etc/slimpi.cfg` for daemon or `~/.config/com.txoof.slimpi/slimpi.cfg` for user space
    * **Required** settings that must be set:
        - `display = waveShareEPDType`
        - example: `display = epd5in83`
            * The display type should match the model number of your HAT compatable e-Paper display
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

## Requirements
### Required Hardware
* Raspberry Pi 4 Model B
    * RPI 3 Model A should work as well, but is untested
* [WaveShare e-Paper display with e-Paper HAT](https://www.waveshare.com/product/oleds-lcds/e-paper.htm)
    * Any waveshare display should work  
    * [Supported WaveShare ePaper Displays](https://www.waveshare.com/wiki/E-Paper_Driver_HAT#Resources)

### Optional Hardware
* [HiFiBerry hat](https://www.hifiberry.com/shop/#boards) (*optional*) 
    * The HiFiBerry DAC+ PRO and similar boards add high-quality audio output to the Pi so it can act as a display and also work as a LMS client player using squeezelite
    * GPIO 2x20 headers **must be added** to the board to support WaveShare HAT
    * HiFiBerry's [DAC+ Bundle](https://www.hifiberry.com/shop/bundles/hifiberry-dac-bundle-4/) with the following configuraiton is a good choice:
        * DAC+ Pro 
        * Acrylic Case for (RCA) AND DIGI+
        * Raspberry Pi 4B 2GB (1GB should be sufficient as well)
        * 16GB SD Card
        * PowerSupply (USB C 5.1V/3A)
        * 2x20 Pin Male Header (required for WaveShare HAT)
    
### Required Software
* [Logitech Media Server](http://wiki.slimdevices.com/index.php/Logitech_Media_Server) running on local network
    * An LMS instance can be run on the Raspberry Pi - [Home Hack - Creating a Raspberry Pi Squeezebox server](https://homehack.nl/creating-a-raspberry-pi-squeezebox-server/) 

### Opational Software
* [squeezelite](http://wiki.slimdevices.com/index.php/Squeezelite) *(optional)*
    * Squeezelite, in combination with a HiFiBerry, allows the Pi to be usded as LMS display **and** client player



```python
%alias mdconvert mdconvert README.ipynb
%mdconvert
```

    [NbConvertApp] Converting notebook README.ipynb to markdown



```python

```
