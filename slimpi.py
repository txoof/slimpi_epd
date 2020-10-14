#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[1]:


#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')
#get_ipython().run_line_magic('reload_ext', 'autoreload')




# In[2]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./slimpi.ipynb')
#get_ipython().run_line_magic('nbconvert', '')




# In[3]:


import logging
import logging.config

# change directory to the location where the script is running
from os import chdir

# parse arguments
import sys

# handle importing libraries based on config file
import importlib

# loop delay - sleep
from time import sleep

# clock
from datetime import datetime
from datetime import timedelta

##### PyPi Modules #####
# handle http requests
import requests

# rate limit the queries on the LMS server
from ratelimiter import RateLimiter

# lmsquery-fork for managing communications with lms server
import lmsquery

import constants
import epdlib
from library import configuration
from library import signalhandler
from library import cacheart

import waveshare_epd # explicitly import this to make sure that PyInstaller can find it




# In[4]:


def do_exit(status=0, message=None):
    if message:
        border = '\n'+'#'*70 + '\n'
        message = border + message + border + '\n***Exiting***'
        print(message)
        
    try:
        sys.exit(status)
    except Exception as e:
        pass




# In[18]:


def scan_servers():
    """scan for and list all available LMS Servers and players"""
    print(f'Scanning for available LMS Server and players')
    servers = lmsquery.LMSQuery().scanLMS()
    if not servers:
        print('Error: no LMS servers were found on the network. Is there one running?')
        do_exit(1)
    print('servers found:')
    print(servers)
    players = lmsquery.LMSQuery().get_players()
    # print selected keys for each player
    keys = ['name', 'playerid', 'modelname']
    for p in players:
        print('players found:')
        try:
            for key in keys:
                print(f'{key}: {p[key]}')
            print('\n')
        except KeyError as e:
            pass 




# In[6]:


logger = logging.getLogger(__name__)
logger.root.setLevel('DEBUG')




# In[8]:


def main():
    #### CONSTANTS ####
    # pull the absolute path from the constants file that resides in the root of the project
    absPath = constants.absPath
    # change the working directory - simplifies all the other path work later
    chdir(absPath)
    
    version = constants.version
    app_name = constants.app_name
    app_long_name = constants.app_long_name
    url = constants.url
        
    ## CONFIGURATION FILES ##
    # logging configuration file
    logging_cfg = constants.logging_cfg
    
    # default base configuration file
    default_cfg = constants.default_cfg
    system_cfg = configuration.fullPath(constants.system_cfg)
    user_cfg = configuration.fullPath(constants.user_cfg)
    
    # file for no artwork
    noartwork = constants.noartwork
    
    # set the waveshare library
    waveshare = constants.waveshare
    
    # set plugins library
    plugins = constants.plugins
    
    # file containing layouts
    layouts_file = constants.layouts
    
#     default_clock = constants.clock
    max_startup_loops = constants.max_startup_loops
    
    ## FORMATTERS
    # configKeyError_fmt.format(`section name`, `key name`)
    configKeyError_fmt = 'Configuration KeyError: section [{}], key {}'
    # moduleNotFoundError_fmt.format(`module name`, `error message`)
    moduleNotFoundError_fmt = 'could not load module: {} - error: {}'
    
    ## LOGGING INIT
    logging.config.fileConfig(logging_cfg)
    
    #### COMMANDLINE ARGS ####
    options = configuration.Options(sys.argv)
    # add options to the configuration object
    # options that override the configuration file options, add in the format: 
    # dest=[[ConfigFileSectionName]]__[[Option_Name]]
    #                               ^^ <-- TWO underscores `__`
    # specifying arguments with #ignore_none=True and ignore_false=True will exclude
    # these arguments entirely from the nested dictionary making it easier to merge
    # the command line arguments into the configuration file without adding unwanted options
    # with default values that potentially conflict or overwrite the config files
    
    # set logging level
    options.add_argument('-l', '--log-level', ignore_none=True, metavar='LOG_LEVEL',
                         type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                         dest='main__log_level', 
                         help='set logging level: DEBUG, INFO, WARNING, ERROR')

    # alternative user_cfg file -- do not add this to the options dictionary if NONE
    options.add_argument('-c', '--config', type=str, required=False, metavar='/path/to/cfg/file.cfg',
                         dest='user_cfg', ignore_none=True, default=user_cfg,
                         help=f'use the specified configuration file; default user config: {user_cfg}')
    
    # daemon mode
    options.add_argument('-d', '--daemon', required=False,
                         default=False, dest='main__daemon', action='store_true', 
                         help='run in daemon mode (ignore user configuration)')
    
    # list servers 
    options.add_argument('-s', '--list-servers', action='store_true', 
                         dest='list_servers',
                         default=False, 
                         help='list servers and any players found on local network and exit')
    
    # set the player-id on the command line -- do not add if set to NONE
    options.add_argument('-p', '--player-name', type=str, required=False, metavar='playerName',
                         default=False, dest='lms_server__player_name', ignore_none=True,
                         help='set the name of the player to monitor')
    
    # display the version and exit
    options.add_argument('-V', '--version', action='store_true', required=False,
                         dest='version', default=False, 
                         help='display version nubmer and exit')
    
    #output the current image displayed to a temporary directory - debugging, screenshoting
    options.add_argument('-t', '--screenshot', metavar = 'INT', type=int, default=None,
                         required=False, dest='main__screenshot', ignore_none=True,
                         help='output the current screen image into the temporary folder for debugging')

    
    # parse the command line options
    options.parse_args()
    
    #### ACTION COMMAND LINE ARGUMENTS ####
    # print version and exit
    if options.options.version:
        print(f'version: {version}')
        do_exit(0)
    
    # scan for local LMS servers and players, then exit
    if options.options.list_servers:
        scan_servers()
        do_exit(0)
    
    # user a user specified configuration file
    if 'user_cfg' in options.opts_dict:
        user_cfg = options.opts_dict['user_cfg']
    
    # always try to use these two configuration files at launch
    config_file_list = [default_cfg, system_cfg]
    
    # check if running in daemon mode; append user config file
    if not options.options.main__daemon:
        config_file_list.append(user_cfg)
    
    # read all the configuration files in the list - values in left most file is default
    # values in each file to the right override previous values
    try:
        config_file = configuration.ConfigFile(config_files=config_file_list)
    except FileNotFoundError as e:
        logging.error(f'could not open one or more config files: {e}')
        logging.error('attempting to continue without above files')
        
    # merge the configuration file(s) values with command line options
    # command line options override config files
    config = configuration.merge_dict(config_file.config_dict, options.nested_opts_dict)
        
    # kludge to work around f-strings with quotes in Jupyter
    ll = config['main']['log_level']
    logging.root.setLevel(ll)
    logging.debug(f'log level set: {ll}')
    
    #### HARDWARE INIT ####
    ## EPD INIT ##
    try:
        # create the name of the module
        epd_module = '.'.join([waveshare, config['layouts']['display']])
        # load the epd module
        logging.debug(f'creating epd display object: {epd_module}')
        epd = importlib.import_module(epd_module)
        
    except KeyError as e:
        myE = configKeyError_fmt.format('layouts', 'display')
        logging.fatal(myE)
        do_exit(1, message=myE)
    except ModuleNotFoundError as e:
        myE = configKeyError_fmt.format('layouts', 'display')
        logging.fatal(myE)
        myE = moduleNotFoundError_fmt.format(epd_module, e)
        logging.fatal(myE)
        do_exit(1, message=myE)
        
    ## SCREEN INIT ##
    rotation = int(config['main'].get('rotate', 0))
    logging.debug(f"configured rotation: {rotation}")
    if rotation not in (180, 90, -90):
        logging.fatal(f"a screen rotation of {rotation} is not supported (only 0, 90, -90 and 180 are supported)")

    screen = epdlib.Screen(rotation=rotation)
    try:
        screen.epd = epd
    except PermissionError as e:
        logging.critical(f'Error initializing EPD interface: {e}')
        logging.critical('The user executing this program does not have access to the SPI devices.')
        do_exit(0, 'This user does not have access to the SPI group\nThis can typically be resolved by running:\n$ sudo groupadd <username> spi')
        
    screen.initEPD()



    ## LAYOUT INIT ##
    logging.debug(f'importing layouts from file: {layouts_file}')
    try:
        layouts = importlib.import_module(layouts_file)
        playing_layout_format = getattr(layouts, config['layouts']['now_playing'])
        plugin_layout_format = getattr(layouts, config['layouts']['plugin'])
        splash_layout_format = getattr(layouts, config['layouts']['splash'])
        error_layout_format = getattr(layouts, config['layouts']['error'])
    except ModuleNotFoundError as e: 
        myE = moduleNotFoundError_fmt.format(layouts_file, e)
        logging.fatal(myE)
        do_exit(1, myE)
        
    except KeyError as e:
        myE = configKeyError.format('layouts', e.args[0])
        logging.fatal(myE)
        do_exit(1, myE)
        
    playing_layout = epdlib.Layout(layout=playing_layout_format, resolution=screen.resolution)
    plugin_layout = epdlib.Layout(layout=plugin_layout_format, resolution=screen.resolution)
    error_layout = epdlib.Layout(layout=error_layout_format, resolution=screen.resolution)
    
    ## PLUGIN INIT ##
    try:
        plugin = importlib.import_module('.'.join([plugins, config['modules']['plugin']]))
    except KeyError as e:
        myE = configKeyError_fmt.format('modules', 'plugin')
        logging.fatal(myE)
        do_exit(1, myE)
    except ModuleNotFoundError as e:
        myE = moduleNotFoundError_fmt.format(plugin, e)
        logging.fatal(myE)
        do_exit(1, myE)
    
    try:
        plugin_update = int(config['modules']['plugin_update'])
    except KeyError as e:
        myE = configKeyError_fmt.format('modules', 'plugin_update')
        logging.error(myE)
        do_exit(1, myE)
        
    
    
    #### EXECUTION ####
    logging.info('starting execution loop')
    
    ## EXEC VARIABLES ##
    # signal handler for catching and handling HUP/KILL signals
    sigHandler = signalhandler.SignalHandler()
    
    # LMS Query rate limiter wrapper - allow max of `max_calls` per `period` (seconds)
    lmsQuery_ratelimit = RateLimiter(max_calls=1, period=3)
    
    # LMS Query Object creation - rate limit to once/30 seconds
    lmsDelay_ratelimit = RateLimiter(max_calls=1, period=30)
    
    # logitech media server interface object
    lms = None
    
    # refresh placeholder
    refresh = False
    
    # refresh delay - seconds to wait before refreshing
    refresh_delay = 60
    
    # startup loop
    startup_counter = 0
    while not sigHandler.kill_now and not lms:
        if startup_counter == 0 and config['main']['splash_screen'].lower() == 'true':
            splash_layout = epdlib.Layout(layout=splash_layout_format, resolution=screen.resolution)
            splash_layout.update_contents({'app_name': app_name,
                                       'version': f'version: {version}',
                                       'url': url})
        
            refresh = splash_layout

        # write to the display
        if refresh and isinstance(refresh, epdlib.Layout):
            logging.debug('refresh display')
            screen.initEPD()
            image = refresh.concat()
#                 screen.elements = refresh.blocks.values()
#                 image = screen.concat()
            screen.writeEPD(image)
        
        logging.info(f'{max_startup_loops - startup_counter} start up attempts reamain')
        logging.info('setting up LMS query connection')
        try:
            lms = lmsquery.LMSQuery(**config["lms_server"])
        except Exception as e:
            logging.error(f'failed to setup connection: {e}')
            error_layout.update_contents({'message': f'Could not find any LMS servers on network. Will try {max_startup_loops-startup_counter} more times', 'time': 'NO SERVER'})            
            refresh = error_layout
            
        if startup_counter >= max_startup_loops:
            sigHandler.kill_now = True
            lms = None
        
        startup_counter += 1
    if not lms:
        do_exit(1, 'startup failed')
        
        
    logging.info('startup complete')
    
    # vars for managing track ID, mode, album art
    nowplaying_id = None
    nowplaying_mode = "Pause"
    artwork_cache = cacheart.CacheArt(app_long_name)

    
    try:
        screenshot_max = int(config['main']['screenshot'])
    except KeyError as e:
        myE = configKeyError_fmt.format('main', 'screenshot')
        logging.error(myE)
        logging.error('saving 0 screenshots')
        screenshot_max = 0

    if screenshot_max > 0:
        screenshot_max
        logging.info(f'creating screenshot object - storing {screenshot_max} images in {artwork_cache.cache_path}')
        screenshot = epdlib.ScreenShot(path=artwork_cache.cache_path, n=screenshot_max)
    else:
        logging.debug('not collecting screenshots')
        screenshot = False
    
    

    while not sigHandler.kill_now:
        response = None
        
        if not lms:
            myE = 'No LMS query object is available. Exiting.'
            logging.fatal(myE)
            do_exit(1, myE)
            
        with lmsQuery_ratelimit:
            try:
                logging.debug(f'query lms server for status of player {config["lms_server"]["player_name"]}: {lms.player_id}')
                response = lms.now_playing()
            except requests.exceptions.ConnectionError as e:
                logging.warning(f'server could not find active player_id: {lms.player_id}')
                logging.warning(f'is the specified player active?')
                logging.warning(f'error: {e}')
                error_layout.update_contents({'message': f'{config["lms_server"]["player_name"]} does not appear to be available. Is it on?', 'time': 'NO PLAYER'})
                refresh = error_layout
                response = None 
            except KeyError as e:
                logging.warning(f'bad response from lms server: {response}')
                logging.warning('retrying...')
                response = None
                
                
        if response:
            try:
                resp_id = response['id']
                resp_mode = response['mode']
                time = response['time']
            except KeyError as e:
                logging.warning(f'bad or incomplete response from server: {e}')
                resp_id = None
                resp_mode = 'QUERY ERROR'
                time = 0.001
        
            # if the track or now playing status have changed, prepare an update
            if resp_id != nowplaying_id or resp_mode != nowplaying_mode:
                logging.info('track/mode change detected')
                nowplaying_id = resp_id
                nowplaying_mode = resp_mode
                
                # fetch the artwork here                    
                try:
                    logging.debug('attempting to download artwork')
                    artwork = artwork_cache.cache_artwork(response['artwork_url'], response['album_id'])
                except KeyError as e:
                    logging.warning('no artwork available')
                    artwork = None
                if not artwork:
                    logging.warning(f'using default artwork file: {noartwork}')
                    artwork = noartwork
                # add the path to the downloaded album art into the response
                response['coverart'] = str(artwork)

                # update the layout with the values in the response            
                playing_layout.update_contents(response)
                refresh_delay = 60
                refresh = playing_layout
            else:
                refresh = False

        if nowplaying_mode != "play" and screen.update.last_updated > refresh_delay:
            logging.debug(f'next update will be in {refresh_delay} seconds')
            logging.info('music appears to be paused, switching to plugin display')
            update = plugin.update(datetime.now() + timedelta(seconds=screen.update_lag))
            update['mode'] = nowplaying_mode
            plugin_layout.update_contents(update)
            refresh = plugin_layout
            refresh_delay = plugin_update            
                
        # check if refresh contains a Layout object; refresh the screen
        if refresh and isinstance(refresh, epdlib.Layout):
            logging.info('refresh display')
            screen.initEPD()
            image = refresh.concat()
            screen.writeEPD(image)

            if screenshot:
                screenshot.save(image)

            refresh = False

        
        
        # sleep for half a second every cycle
        sleep(0.5)    
    
    print('Received exit signal - cleaning up')

    screen.initEPD()
    screen.clearEPD()
    artwork_cache.clear_cache()    
    
    return config







# In[19]:


if __name__ == '__main__':
    o = main()




# In[ ]:







# In[ ]:





