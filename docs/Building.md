## Building SlimPi
To build an executable package suitable for installing SlimPi requires several Debian development packages as well as several python libraries. See below for specifics.

### Quick and Dirty Build
The `build.sh` script will attempt to check the build environment and suggest any missing Debian packages. The next step is to build a virtualenv using pipenv. The final step is to create an executable package using pyinstaller. See below for more detailed requirements.
-  run: `./build.sh`

### Build Requirements
- System Software
    * python3 
        `apt-get install python3`
    * pip
        `apt-get install python3-pip`
    * pipevn
        - `pip3 install pipenv`
- System Libraries
    * `libtiff5-dev, libopenjp2-7-dev`
        * install with `sudo apt-get install libtiff5-dev libopenjp2-7-dev`
- Python Libraires from PyPi using pipenv:
    * `epdlib, cachepath, ratelimiter, lmsquery-fork, spidev, RPi.GPIO`
    *  Install with pipenv:
        - `pipenv --three; pipenv sync` 
            - This will create a virtual environment and install the appropriate packages and dependencies        
            - NOTE: pipenv cannot handle installing `RPi.GPIO` from the command line. It must be added by hand to Pipfile by and and quotated: `"RPi.GPIO" = "*" `

### Building SlimPi
- Create a runnable package using PyInstaller
    * PyInstaller must be run within the virtual environment:
        * `pipenv run pyinstaller --clean 


```python
%alias mdconvert mdconvert Building.ipynb
%mdconvert
```

    [NbConvertApp] Converting notebook Building.ipynb to markdown

