#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[108]:


#get_ipython().magic(u'alias nbconvert nbconvert ./Configuration.ipynb')

#get_ipython().magic(u'nbconvert')




# In[48]:


import sys
import argparse
import configparser
import re
from pathlib import Path, PosixPath

import logging




# In[20]:


logging.basicConfig(level=logging.DEBUG, format='%(name)s:%(funcName)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)




# In[ ]:


def merge_dict(a, b):
    '''recursivley merge two dictionarys overwriting values
        known issue: if `a` contains a different data type than `b`, 
        `b` will completely overwrite the data in `a`
        
    Args:
        a(`dict`): nested dictionary
        b(`dict`): nested dictionary 
        
    Returns:
        `dict`
    '''
    c = dict(a) # make a copy of dict `a`
    for key in b:
        if key in a:
            if isinstance(b[key], dict) and isinstance(a[key], dict):
                c[key] = merge_dict(a[key], b[key])
            else:
                c[key] = b[key]
        else:
            c[key] = b[key]
    return c




# In[ ]:


def fullPath(path):
    '''expand user paths and resolve string into a path
    
    Args:
        path(`str`): string representation of a path 
            `~`, `.` and `..` notation will be expanded
            and resolved
    Returns:
        `path.Path()`'''
    if path is None:
        path = None
    else:
        path = Path(path).expanduser().resolve()
    return path




# In[ ]:


class Options():
    '''command line parser object 
    
    Args:
        args(`list`): sys.argv is typically passed here
        
    Properties:
        parser(`argparse.ArgumentParser`): argument parser object
        args(`list`): list of arguments
        options(NameSpace): argument parser generated namespace of arguments
        opts_dict(`dict`): namespace -> dictionary'''
    def __init__(self, args=None):
        self.parser = argparse.ArgumentParser()
        self.ignore_none = []
        self.ignore_false = []
        self.args = args
        self.options = None
        self.opts_dict = None
        self.nested_opts_dict = None
    
    @property
    def options(self):
        '''argparser Namespace of the parsed arguments'''
        return self._options
    
    @options.setter
    def options(self, options):
        if options:
            self._options = options
        else:
            self._options = None
    
    def parse_args(self, args=None): #, discard_false=[], discard_none=[]):
        '''parse arguments and set dictionaries
        
        Args:
            args(`list`): list of commandline arguments to process
            set_args(`bool`): set arguments property (default=True)
            discard_false(`list`): discard any keys that are set as False
            discard_none(`list`): discard any keys that are set as None
            
        Sets:
            args(`list`): list of arguments
            options(Nampespace): namespace of parsed known arguments
            opts_dict(`dict`): flat dictionary containing arguments
            nested_opts_dict(`dict` of `dict` of `str`): parsed arguments
                nested to match ConfigFile.opts_dict:
                {'section_name': {'option1': 'valueY'
                                  'option2': 'valueZ'}
                                  
                 'section_two':  {'optionX': 'setting1'
                                  'optionY': 'other_setting'}}
                                  
            see add_argument() for more information'''
            
        if args:
            my_args = args
        else:
            my_args = self.args
                
        if my_args:
            options, unknown = self.parser.parse_known_args()
            logging.warning(f'ignoring unknown options: {unknown}')
            self.options = options
            self.opts_dict = options
#             for key in discard_false:
#                 try:
#                     if self.opts_dict[key] is False:
#                         logging.info(f'popping: {key}')
#                         self.opts_dict.pop(key)
#                 except KeyError as e:
#                     logging.debug(f'{key} not found, ignoring')
                    
#             for key in discard_none:
#                 try:
#                     if self.opts_dict[key] is None:
#                         logging.info(f'popping: {key}')
#                         self.opts_dict.pop(key)                    
#                 except KeyError as e:
#                     logging.debug(f'{key} not found, ignoring')
                    
            self.nested_opts_dict = self.opts_dict
 
    
    @property
    def opts_dict(self):
        '''dictionary of namespace of parsed options
        
        Args:
            options(namespace): configparser.ConfigParser.parser.parse_known_args() options
        
        Returns:
            `dict` of `namespace` of parsed options
            '''
        return self._opts_dict
    
    @opts_dict.setter
    def opts_dict(self, options):
        if options:
            self._opts_dict = vars(self.options)
        else:
            self._opts_dict = None

    @property
    def nested_opts_dict(self):
        '''nested dictionary of configuration options
            `nested_opts_dict` format follows the same format as ConfigFile.config_dict
            see add_argument for more information 
            
        Args:
            opts_dict(`dict`): flat dictionary representation of parser arguments'''
        return self._nested_opts_dict
    
    @nested_opts_dict.setter
    def nested_opts_dict(self, opts_dict):
        if not opts_dict:
            # skip processing
            self._nested_opts_dict = None
        else:
            # nest everything that comes from the commandline under this key
            cmd_line = '__cmd_line'
            d = {}
            # create the key for command line options
            d[cmd_line] = {}
            
            # process all the keys in opts_dict
            for key in opts_dict:
                if key in self.ignore_none or key in self.ignore_false:
                    # do not include these keys in the nested dictionary
                    continue
                # match those that are in the format [[SectionName]]__[[OptionName]]
                match = re.match('^(\w+)__(\w+)$', key)
                if match:
                    # unpack into {sectionName: {OptionName: Value}}
                    section = match.group(1)
                    option = match.group(2)
                    if not section in d:
                        # add the section if needed
                        d[section] = {}
                    d[section][option] = opts_dict[key]
                else:
                    # if not in `section__option format`, do not unpack add to dictionary
                    # under `cmd_line` key
                    d[cmd_line][key] = opts_dict[key]
            
            self._nested_opts_dict = d
            

    
    def add_argument(self, *args, **kwargs):
        '''add arguments to the parser.argparse.ArgumentParser object 
            use the standard *args and **kwargs for argparse
            
            arguments added using the kwarg `dest=section__option_name`
            note the format [[section_name]]__[[option_name]]
            will be nested in the `opts_dict` property in the format:
            {'section': 
                        {'option_name': 'value'
                         'option_two': 'value'}}
                         
            the `nested_opts_dict` property can then be merged with a ConfigFile 
            `config_dict` property using the merge_dicts() function:
            merge_dicts(obj:`ConfigFile.config_dict`, obj:`Options.nested_opts_dict`) 
            to override the options set in the configuration file(s) with
            commandline arguments
        
        Args:
            ignore_none(`bool`): ignore this when building 
            ignore_false(`bool`):
            *args, **kwargs'''
        # pop out these keys to avoid sending to 
        ignore_none = kwargs.pop('ignore_none', False)
        ignore_false = kwargs.pop('ignore_false', False)

        if 'dest' in kwargs:
            dest = kwargs['dest']
        elif len(args) == 2:
            dest = args[1]
        else:
            #FIXME need to strip out `--` and turn `-` to `_`
            dest = args[0]
        
        dest = dest.strip('-').replace('-', '_')
        
        if ignore_none:
            self.ignore_none.append(dest)
        if ignore_false:
            self.ignore_none.append(dest)
        
        try:
            self.parser.add_argument(*args, **kwargs)
        except argparse.ArgumentError as e:
            logging.warning(f'failed adding conflicting option {e}')




# In[ ]:


# o = Options(sys.argv)

# o.add_argument('-c', '--config-file', type=str, default=None, 
#                         help='use the specified configuration file. Default is stored in ~/.config/myApp/config.ini')
# o.add_argument('-l', '--log-level', ignore_none=True, 
#                         type=str, dest='logging__log_level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
#                         default = None,
#                         help='set logging level: DEBUG, INFO, WARNING, ERROR')


# o.parse_args()
# print(o.opts_dict)
# print(o.nested_opts_dict)




# In[ ]:


# o.ignore_none




# In[103]:


class ConfigFile():
    '''Read and parse one or more INI style configuration files
    
        Creates a configparser.ConfigParser() object and reads multiple
        configuration files. Settings in each file supersedes pervious files
        `config_files`=[default, system, user] 
        * default - read first
        * system - read second and overwrites default
        * suer - read last and overwrites system
        
    Args:
        config_files(`list`): list of configuration files to read'''
    
    def __init__(self, cfg_files=[]):
        self.cfg_files = cfg_files
        self.parser = configparser.ConfigParser()
        
    @property
    def cfg_files(self):
        return self._cfg_files
    
    @cfg_files.setter
    def cfg_files(self, cfg_files):
        if not isinstance(cfg_files, list):
            raise TypeError(f'Type mismatch: expected {list}, but received {type(cfg_files)}: {cfg_files}')
        
        self._cfg_files = [Path(i).expanduser().resolve() for i in cfg_files]
    
    def parse_config(self):   
        for file in self.cfg_files:
            if file.exists():
                self.parser.read(file)
            else:
                logging.warning(f'{file} does not exist')
                
        if self.parser.sections():
            self.config_dict = self._config_2dict(self.parser)        
                
    def _config_2dict(self, configuration):
        '''convert an argparse object into a dictionary

        Args:
            configuration(`configparser.ConfigParser`)

        Returns:
            `dict`'''
        d = {}
        for section in configuration.sections():
            d[section] = {}
            for opt in configuration.options(section):
                d[section][opt] = configuration.get(section, opt)

        return d    




# In[106]:


# c = ConfigFileN(['./slimpi.cfg', '~/.config/com.txoof.slimpi/slimpi.cfg'])
# c.parse_config()

# c.config_dict




# In[ ]:


# class ConfigFile():
#     def __init__(self, default=None, user=None):
#         self.cfg_files = []
# #         self.default = file(default)
#         self.default = fullPath(default)
# #         self.user = file(user)
#         self.user = fullPath(user)
#         self.parse_config()
    
#     def parse_config(self):
#         '''parse the config file(s) overriding the default configuration 
#             with the user configuration (if provided)
            
#         Sets:
#             config(obj:`configparser.ConfigParser`): parser object
#             config_dict(`dict` of `dict` of `str`): dictionary representation of 
#                 merged configuration files'''
#         def append(file):
#             if file:
#                 if file.exists:
#                     self.cfg_files.append(file)
#                 else:
#                     logging.warning(f'configuration file does not exist: {file}')
                    
#         append(self.default)
#         append(self.user)
# #         if self.default.exists:
# # #             self.cfg_files.append(self.default.file)
# #             self.cfg_files.append(self.default)
# #         if self.user.exists:
# # #             self.cfg_files.append(self.user.file)
# #             self.cfg_files.append(self.user)
#         if self.cfg_files:
#             self.config = configparser.ConfigParser()
#             self.config.read(self.cfg_files)
        
#         if self.config.sections():
#             self.config_dict = self._config_2dict(self.config)
        
        
#     def _config_2dict(self, configuration):
#         '''convert an argparse object into a dictionary

#         Args:
#             configuration(`configparser.ConfigParser`)

#         Returns:
#             `dict`'''
#         d = {}
#         for section in configuration.sections():
#             d[section] = {}
#             for opt in configuration.options(section):
#                 d[section][opt] = configuration.get(section, opt)

#         return d    




# In[ ]:


# c = ConfigFile(default='./slimpi.cfg', user='~/.config/com.txoof.slimpi/slimpi.cfg')

# c.cfg_files

# c.config.options('main')

# c.config_dict



# create a "Default" configuration object from the builtin config
# Create a "user" configuration based on the user config
# merge the default and the user overriding the default with the user version
# merge the command line over the top of everything
# 
# finally creating a dictionary of options


# In[ ]:


# merge_dict(c.config_dict, o.nested_opts_dict)




# In[ ]:


# aa = dict(a)
# bb = dict(b)

# aa = {'a': {'cow': 'cynthia', 'bear': 'barney', 'horse': 'ed'}, 'b': 10, 'c': [1, 3, 5, 7, 9], 'foo': 'bar'}
# bb = {'a': {'cow': 'Zed', 'bear': 'barney', 'zebra': 'yellow'}, 'b': 10, 'c': [2, 4, 6, 8, 10]}

# print(aa)

# print(bb)

# merge_dict(aa, bb)




# In[ ]:





