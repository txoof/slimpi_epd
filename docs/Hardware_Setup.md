## Hardware Setup
The basic installation is very straightforward. If you are using another HAT, double check that the physical Pi GPIO pins are not in use. The HiFiBerry DAC+ PRO does not conflict with the WaveShare HAT (1 March 2020). See the Notes below if you have a conflict.

1. Shut down the Pi -- installing hardware while the Pi is on is a great way to let out the magic blue smoke.
2. Check the [switch settings on the WaveShare HAT](https://www.waveshare.com/wiki/E-Paper_Driver_HAT#Switch_settings) -- the A and B settings must match your board type.
3. Attach the ribbon cables as shown [here](https://youtu.be/f4yoYbSWctI?t=137)
4. Install the HAT on GPIO pins 
    * the HAT should fit logically over the Pi; all pins should be covered
    * If you are using a HiFiBerry DAC+, you may need to [solder the GPIO pins onto the board before proceeding](https://www.hifiberry.com/docs/hardware/gpio-usage-of-hifiberry-boards/)
5. Boot the Pi and enable SPI (see [System Setup](#system-setup) below)


| HAT JST Pin | Pi Pin Name | Physical Pin Number |
|-------------|-------------|---------------------|
| 3.3V        | 3.3V        | 1                   |
| GND         | GND         | 3                   |
| DIN         | MOSI        | 19                  |
| CLK         | SCLK        | 23                  |
| CS          | CE0         | 24                  |
| DC          | 25(BCM)     | 22                  |
| RST         | 17(BCM)     | 11                  |
| BUSY        | 24(BCM)     | 18                  |

### Hardware Test
It is a good idea to test the hardware and make sure the display works properly before proceeding. The screen should run through some sample images. 

1. Clone the WaveShare repo:
    * ` git clone https://github.com/waveshare/e-Paper.git`
        * if git is not installed: `sudo apt-get install git`
2. Change into the examples directory:
    * `cd e-Paper/RaspberryPi\&JetsonNano/python/examples/`
3. Execute the test script for the appropriate display:
    * `python3 epd_5in83_test.py`

If the display does not work properly, check the troubleshooting section below.


### Notes
If you have a conflict, it *may* be possible to adjust the pin numbers in the `./waveshare_epd/epdconfig.py`, but this has yet to be tested.
```
class RaspberryPi:
    # Pin definition
    RST_PIN         = 17
    DC_PIN          = 25
    CS_PIN          = 8
    BUSY_PIN        = 24
```




```python
%alias mdconvert mdconvert Hardware_Setup.ipynb
%mdconvert
```

    [NbConvertApp] Converting notebook Hardware_Setup.ipynb to markdown

