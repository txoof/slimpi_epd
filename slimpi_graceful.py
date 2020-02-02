#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[2]:


#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')
#get_ipython().run_line_magic('reload_ext', 'autoreload')




# In[144]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./slimpi_graceful.ipynb')




# In[149]:


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




# In[125]:


def main():
    #### CONSTANTS ####
    # pull the absolute path from the constants file that resides in the root of the project
    absPath = constants.absPath
    # change the working directory - simplifies all the other path work later
    chdir(absPath)
    
    
    ## CONFIGURATION FILES ##
    # logging configuration file
    logging_cfg = constants.logging_cfg
    
    # default base configuration file
    default_cfg = constants.default_cfg
    system_cfg = configuration.fullPath(constants.system_cfg)
    user_cfg = configuration.fullPath(constants.user_cfg)
    
    # set the waveshare library
    waveshare = constants.waveshare
    
    # file containing layouts
    layouts_file = constants.layouts
    
    
    # FORMATTERS
    keyError_fmt = 'KeyError: configuration file section [{}] missing value: {}'
    configError_fmt = 'configuration file error: see section [{}] in config file: {}'
    
    
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
    options.add_argument('-p', '--player-id', type=str, required=False, metavar='playerName',
                         default=False, dest='lms_server__player_id', ignore_none=True,
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
        print(f'{version}')
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
    config_file = configuration.ConfigFile(config_files=config_file_list)
    
    # merge the configuration file(s) values with command line options
    # command line options override config files
    config = configuration.merge_dict(config_file.config_dict, options.nested_opts_dict)
    
    # kludge to work around f-strings with quotes in Jupyter
    ll = config['main']['log_level']
    logging.root.setLevel(ll)
    logging.debug(f'log level set: {ll}')
    
    #### Objects ####
    # signal handler for catching and handling HUP/KILL signals
    sigHandler = signalhandler.SignalHandler()
    
    
    #### HARDWARE INIT ####
    ## EPD INIT ##
    try:
        epd = importlib.import_module('.'.join([waveshare, config['layouts']['display']]))
#         epd = importlib.import_module('.'.join([waveshare, 'foo']))
    except KeyError as e:
        logging.fatal(keyError_fmt.format('layouts', '"display"'))
        do_exit(0, message=f'Bad or missing "display" type in section [layouts] in {config_file_list}')

    except ModuleNotFoundError as e:
        logging.fatal(configError_fmt.format('layouts', config_file_list))
        logging.fatal(f'{e}, {str(type(e))}')
        do_exit(0, message=f'Bad or missing "display" type in section [layouts] in {config_file_list}')

    
    
    try:
        while not sigHandler.kill_now:
            # sleep for half a second every cycle
            sleep(0.5)
            
    finally:
        print('Received exit signal - cleaning up')
        
    return config




# In[141]:


if __name__ == '__main__':
    o = main()




# In[120]:


print(o)




# In[ ]:





