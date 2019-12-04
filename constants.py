# application version number
version = 'version 0.2.0'

# url of github project
url = 'https://github.com/txoof/slimpi_epd'

# short name of application
app_name = 'slimpi'

# developer's name
devel_name = 'com.txoof'

app_long_name = '.'.join([devel_name, app_name])



##### configuration files

# logging configuration
logging_cfg = 'logging.cfg'

# default configuration
default_cfg = 'slimpi.cfg'

# user configuration
user_cfg = '/'.join(['~/.config/', app_long_name])

# location of default image for albums that fail to return ablum art
noartwork = './images/No-album-art.png'

###### python modules that may change
# EPD library
waveshare = 'waveshare_epd' 
# layouts for display
layouts = 'layouts'

