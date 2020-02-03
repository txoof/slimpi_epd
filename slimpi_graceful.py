#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[2]:


#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')
#get_ipython().run_line_magic('reload_ext', 'autoreload')




# In[346]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./slimpi_graceful.ipynb')




# In[348]:


#get_ipython().run_line_magic('nbconvert', '')




# In[4]:


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




# In[147]:


def do_exit(status=0, message=None):
    if message:
        border = '\n'+'#'*70 + '\n'
        message = border + message + border + '\n***Exiting***'
        print(message)
        
    try:
        sys.exit(status)
    except Exception as e:
        pass




# In[6]:


def scan_servers():
    """scan for and list all available LMS Servers and players"""
    print(f'Scanning for available LMS Server and players')
    servers = lmsquery.scanLMS()
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




# In[337]:


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
    
    # set the waveshare library
    waveshare = constants.waveshare
    
    # set plugins library
    plugins = constants.plugins
    
    # file containing layouts
    layouts_file = constants.layouts
    
    default_clock = constants.clock
    
    
    # FORMATTERS
    keyError_fmt = 'KeyError: configuration file section [{}] bad/missing value: "{}"'
    configError_fmt = 'configuration file error: see section [{}] in config file: {}'
    moduleError_fmt = 'failed to load module "{}" {}'
    
    
    #### CONFIGURATION ####
    
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
        epd_module = '.'.join([waveshare, config['layouts']['display']])
        epd = importlib.import_module(epd_module)
#         epd = importlib.import_module('.'.join([waveshare, 'foo']))
    except KeyError as e:
        myE = keyError_fmt.format('layouts', 'display')
        logging.fatal(myE)
#         do_exit(1, message=f'Bad or missing "display" type in section [layouts] in {config_file_list}')
        do_exit(1, message=myE)

    except ModuleNotFoundError as e:
        myE = configError_fmt.format('layouts', config_file_list)
        logging.fatal(myE)
#         do_exit(1, message=f'Bad or missing "display" in section [layouts] in {config_file_list}')
        do_exit(1, message=moduleError_fmt.format(epd_module, myE))
        
    ## SCREEN INIT ##
    screen = epdlib.Screen()
    try:
        screen.epd = epd
        
    except PermissionError as e:
        logging.critical(f'Error initializing EPD interface: {e}')
        logging.critical('The user executing this program does not have access to the SPI devices.')
        do_exit(0, 'This user does not have access to the SPI group\nThis can typically be resolved by running:\n$ sudo groupadd <username> spi')
    
    screen.initEPD()
      
    
    ## LAYOUT INIT ##
    
    # import layouts
    logging.debug(f'importing layouts from file: {layouts_file}')
    try:
        layouts = importlib.import_module(layouts_file)
        playing_layout_format = getattr(layouts, config['layouts']['now_playing'])
        plugin_layout_format = getattr(layouts, config['layouts']['plugin'])
        splash_layout_format = getattr(layouts, config['layouts']['splash'])
        error_layout_format = getattr(layouts, config['layouts']['error'])
    except ModuleNotFoundError as e: 
        myE = f'- could not load layouts from module {config_file}'
        logging.fatal(moduleError_fmt.format('layouts', myE))
        do_exit(1, message=moduleError_fmt.format('layouts', myE))
    
    except (KeyError, AttributeError) as e:
        logging.fatal(keyError_fmt.format('layouts', e.args[0]))
        logging.fatal(configError_fmt.format('layotus', config_file_list))
        do_exit(1, message=keyError_fmt.format('layouts', e.args[0]))
    
    
    playing_layout = epdlib.Layout(layout=playing_layout_format, resolution=screen.resolution)
    plugin_layout = epdlib.Layout(layout=plugin_layout_format, resolution=screen.resolution)
    error_layout = epdlib.Layout(layout=error_layout_format, resolution=screen.resolution)
        
    
    ## PLUGIN INIT ##
    try:
        plugin = importlib.import_module('.'.join([plugins, config['modules']['plugin']]))
    except KeyError as e:
        logging.error(keyError_fmt.format('modules', config['modules']['plugin']))
    except ModuleNotFoundError as e:
        logging.error(moduleError_fmt.format(config['modules']['plugin'], e.args[0]))
        logging.error('falling back to default')
        try:
            plugin = importlib.import_module('.'.join([plugins, default_clock]))
            plugin_layout_format = getattr(layouts, default_clock)
        except ModuleNotFoundError as e:
            myE = moduleError_fmt.format(default_clock, e.args[0])
            logging.fatal(myE)
            do_exit(1, myE)
    
    try:
        plugin_update = int(config['modules']['plugin_update'])
    except KeyError as e:
        myE = keyError_fmt.format('modules', 'plugin_update')
        logging.error(myE)
        logging.error('setting plugin update to 60 seconds')
        pluggin_update = 60
    
    
    #### EXECUTION ####
    logging.debug(f'starting with configuration: {config}')
    
    ## EXEC VARIABLES ##
    # signal handler for catching and handling HUP/KILL signals
    sigHandler = signalhandler.SignalHandler()
    
    # LMS Query rate limiter wrapper - allow max of `max_calls` per `period` (seconds)
    lmsQuery_ratelimit = RateLimiter(max_calls=1, period=3)
    
    # LMS Query Object creation - rate limit to once/30 seconds
    lmsDelay_ratelimit = RateLimiter(max_calls=1, period=30)
    
    # logitech media server interface object
    lms = None
    
    # refresh when true
    refresh = False
    refresh_delay = 60
    
    # vars for managing track ID, mode, album art
    nowplaying_id = None
    nowplaying_mode = "Pause"
    artwork_cache = cacheart.CacheArt(app_long_name)
    
    # check for the word `true` - config file is all stored as type `str`
    if config['main']['splash_screen'].lower() == 'true':
        splash_layout = epdlib.Layout(layout=splash_layout_format, resolution=screen.resolution)
        splash_layout.update_contents({'app_name': app_name,
                                       'version': f'version: {version}',
                                       'url': url})
        refresh = splash_layout
#         screen.elements = splash_layout.blocks.values()
#         screen.concat()
#         screen.writeEPD()
    else:
        pass
        
    
    try:
        while not sigHandler.kill_now:
            response = None
        
            # check of LMS query object is configured
            if lms:
                with lmsQuery_ratelimit:
                    try:
                        myE = f'query lms server for status of player {config["lms_server"]["player_name"]}: {lms.player_id}'
                        logging.debug(myE)
                        response = lms.now_playing()
                    except requests.exceptions.ConnectionError as e:
                        logging.warning(f'server could not find active player_id: {lms.player_id}')
                        logging.warning(f'is the specified player active?')
                        error_layout.update_contents({'message': f'{config["lms_server"]["player_name"]} does not appear to be available. Is it on?', 'time': 'NO PLAYER'})
                        refresh = error_layout
                        response = None
                        
                    except KeyError as e:
                        myE = f'No playlist is active on {config["lms_server"]["player_name"]}'
                        logging.info(myE)
                        response =  {'title': 'No music is queued', 'id': 'NONE', 'mode': 'No Playlist'}
                        nowplaying_mode = response['mode']                 
    
            else: # try to create an lms query object
                with lmsDelay_ratelimit:
                    try:
                        logging.debug('setting up lms query connection')
                        lms = lmsquery.LMSQuery(**config['lms_server'])
                        if not lms.player_id:
                            raise ValueError(keyError_fmt.format('lms_server', 'player_name'))
                        logging.info('lms query connection created')

                    except TypeError as e:
                        logging.critical(configError_fmt.format('lms_server', config_file_list))
                        error_layout.update_contents({'message': configError_fmt.format('lms_server', config_file_list)})
                        refresh = error_layout

                    except ValueError as e:
                        myE = keyError_fmt.format('lms_server', 'player_name')
                        logging.critical(myE)
                        myE = 'LMS QUERY ERROR: \n' + myE
                        error_layout.update_contents({'message': myE, 'time': 'LMS ERROR'})
                        refresh = error_layout
                        
                    except OSError as e:
                        myE = 'could not find LMS servers due to network error '
                        logging.warning(myE)
                        logging.warning('delaying start of LMS query connection')
                        myE = 'LMS QUERY ERROR: ' + myE + e.args[0]
                        error_layout.update_contents({'message': myE, 'time': 'LMS ERROR'})
                        refresh = error_layout
                        

            if response:
                resp_id = response['id']
                resp_mode = response['mode']
                if resp_id != nowplaying_id or resp_mode != nowplaying_mode:
                    logging.info(f'track/mode change to: {resp_mode}')
                    nowplaying_id = resp_id
                    nowplaying_mode = resp_mode
                    
                    # attempt to fetch artwork 
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
                    
                    # refresh contains the current layout
                    refresh = playing_layout
                    #set delay to 60 seconds
                    refresh_delay = 60
                else:
                    refresh = False
                
            if nowplaying_mode != "play" and screen.update.last_updated > refresh_delay:
                logging.debug(f'next update will be in {refresh_delay} seconds')
                logging.info('music appears to be paused, switching to plugin display')
                update = plugin.get_time()
                update['mode'] = nowplaying_mode
                plugin_layout.update_contents(update)
                refresh = plugin_layout
                refresh_delay = plugin_update                
            
            
            # check if `refresh` has been updated 
            if refresh and isinstance(refresh, epdlib.Layout):
                logging.debug('refresh display')
                screen.initEPD()
                screen.elements = refresh.blocks.values()
                screen.concat()
                screen.writeEPD()
                # set response to 
                refresh = False
            
            # sleep for half a second every cycle
            sleep(0.5)
            
    finally:
        print('Received exit signal - cleaning up')
        
        screen.initEPD()
        screen.clearEPD()
        
    return config




# In[324]:


if __name__ == '__main__':
    o = main()




# In[ ]:





