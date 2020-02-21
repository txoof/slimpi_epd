from pathlib import Path
# application version number
version = '0.3.93'

# url of github project
url = 'https://github.com/txoof/slimpi_epd'

# short name of application
app_name = 'slimpi'

# developer's name in reverse DNS format
devel_name = 'com.txoof'

# reverse dns name for this project
app_long_name = '.'.join([devel_name, app_name])



##### configuration files

# logging configuration
logging_cfg = './logging.cfg'

# default configuration file name
default_cfg_name = 'slimpi.cfg'

# default configuration location
default_cfg = f'./{default_cfg_name}'

# default system configuration location for daemon
system_cfg = f'/etc/{default_cfg_name}'

# default user configuration
#user_cfg = '/'.join(['~/.config', app_long_name, default_cfg_name])
user_cfg = Path(f'~/.config/{app_long_name}/{default_cfg_name}').expanduser()

# location of default image for albums that fail to return ablum art
noartwork = './images/No-album-art.png'

###### python modules that may change
# EPD library
waveshare = 'waveshare_epd'

# layouts file for display
layouts = 'layouts'

# plugins directory - clocks;
plugins = 'plugins'

# defualt clock module to use if no other is specified
clock = 'clock'


##### Runtime Constants #####
max_startup_loops = 10


from pathlib import Path
absPath = Path(__file__).absolute().parent
