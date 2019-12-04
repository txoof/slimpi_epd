#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[ ]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./Configuratiion.ipynb')

#get_ipython().run_line_magic('nbconvert', '')




# In[1]:


import sys
import argparse
import configparser
import re
from pathlib import Path

import logging



# # see this for inspiration https://github.com/szymonlipinski/examples/blob/master/python_settings/fixed.py


# In[25]:


logging.basicConfig(level=logging.DEBUG, format='%(name)s:%(funcName)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)




# In[152]:


class file():
    '''class that creates a pathlib.Path().expanduser().resolve() object from a string
    Args:
        file(`str`): string representation of a file path'''
    def __init__(self, file):
        self.file = file
        
    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, file):
        if file:
            f = Path(file).expanduser().resolve()
            if f.exists():
                self._file = f
                self.parent = f.parent
                self.exists = True
            else:
                logging.warning(f'file does not exist: {f}')
                self._file = None
                self.parent = None
                self.exists = False
        else:
            self._file = None
            self.exists = False
            
    def __repr__(self) -> Path:
        return repr(str(self.file))
    
    def __str__(self):
        return(str(self.file))




# In[259]:


class Options():
    '''parse command line options
    Args:
        args(`list`): sys.argv is typically passed here
    Properties:
        parser(`argparse.ArgumentParser`): argument parser object
        args(`list`): list of arguments
        options(NameSpace): argument parser generated namespace of arguments
        opts_dict(`dict`): namespace -> dictionary'''
    def __init__(self, args):
        self.parser = argparse.ArgumentParser()      
        self.args = args
    
    @property
    def parser(self):
        '''The argparser object'''
        return self._parser
    
    @parser.setter
    def parser(self, parser):
        if parser:
            self._parser = parser
    
    @property
    def options(self):
        '''argparser namespace of the parsed arguments'''
        try:
            return self._options
        except AttributeError as e:
            self._parse_args()
            return self._options

    
    @options.setter
    def options(self, options):
        if options:
            self._options = options
        else:
            self._options = None
    
    @property
    def opts_dict(self):
        '''namespace of dictionary of parsed options'''
        self._parse_args()
        self._opts_dict = vars(self.options)
        self.nested_opts_dict = self._nested_opts_dict(vars(self.options))
        return self._opts_dict
    
    def _nested_opts_dict(self, opts_dict):
        d = {}
        d['__no_section'] = {}

        for key in opts_dict:
            match = re.match('^(\w+)__(\w+)$', key)
            if match:
                section = match.group(1)
                option = match.group(2)
                if not section in d:
                    d[section] = {}
                d[section][option] = opts_dict[key]
            else:
                d['__no_section'][key] = opts_dict[key]
        return d    
    
    def _parse_args(self):
        '''parse known arguments and discard unknown arguments'''
        options, unknown = self.parser.parse_known_args()
        logging.info(f'discarding unknwon commandline arguments: {unknown}')
        self.options = options
    
    def add_argument(self, *args, **kwargs):
        '''add arguments to the parser using standard argparse.ArgumentParser
        Args:
            *args, **kwargs'''
        try:
            self.parser.add_argument(*args, **kwargs)
        except argparse.ArgumentError as e:
            logging.warning(f'failed adding conflicting option {e}')




# In[175]:


class ConfigFile():
    def __init__(self, default=None, user=None):
        self.cfg_files = []
        self.default = file(default)
        self.user = file(user)
        self.parse_config()
        
    def parse_config(self):
        if self.default.exists:
            self.cfg_files.append(self.default.file)
        if self.user.exists:
            self.cfg_files.append(self.user.file)
        if self.cfg_files:
            self.config = configparser.ConfigParser()
            self.config.read(self.cfg_files)
        
        if self.config.sections():
            self.config_dict = self._config_2dict(self.config)
        
        
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




# In[176]:


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


# In[260]:


# o = Options(sys.argv)

# o.add_argument('-c', '--config-file', type=str, default=None, 
#                         help='use the specified configuration file. Default is stored in ~/.config/myApp/config.ini')
# o.add_argument('-l', '--log-level', type=str, dest='logging__log_level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
#                         default = 'WARNING',
#                         help='set logging level: DEBUG, INFO, WARNING, ERROR')

# o.opts_dict

# o.nested_opts_dict


