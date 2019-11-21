#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[1]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert Layout.ipynb')




# In[2]:


#get_ipython().run_line_magic('nbconvert', '')




# In[1]:


import logging
from pathlib import Path
import copy
from PIL import Image, ImageDraw, ImageFont




# In[2]:


# from . import layouts
# from . import constants
# from . import Block




# In[16]:


try: 
    from . import layouts
except ImportError as e:
    import layouts 
    
try:
    from . import constants
except ImportError as e:
    import constants

try:
    from . import Block as Block
except ImportError as e:
    import Block




# In[36]:


class Layout:
    '''Class for defining layout of epd screen
    
    This class allows screen layouts to be declared in terms of image blocks in an X, Y plane. 
    Block placement is defined in terms of absolute or relative positions. Only one block 
    with absolute coordinates is needed. Block size is calculated based on screen size.
    
    Examples:
    layotus.threeRow has the sections: 'title', 'album', 'artist', 'mode', 'coverart'
    # creates the object and calculates the positions based on the rules set 
    # in the layouts file and screen size
    l = Layout(resolution=(600, 448), layout=layouts.threeRow)
    # update/add content to the layout object, applying formatting from layout file
    l.update_contents({'title': 'Hannah Hunt', 'album': 'Modern Vampires of the City', 
                       'artist': 'Vampire Weekend', 'mode': 'playing', 
                       'coverart': '/temp/VampireWeekend_ModernVampires.jpg'})
    
    Attributes:
        resolution (:obj:`tuple` of :obj: `int`): X, Y screen resolution in pixles
        font (str): path to font file
        layout (dict): dictionary with layout instructions (see below)
        blocks (dict): dictionary of ImageBlock and TextBlock objects
        
    '''
    def __init__(self, resolution=(600, 448), layout=None, font=constants.FONT):
        logging.info('create layout')
        self.resolution = resolution
        self.font = str(Path(font).resolve())
        self.layout = copy.deepcopy(layout)
        self.images = None

    def _check_keys(self, dictionary={}, values={}):
        '''Check `dictionary` for missing key/value pairs specified in `values`
        
        Args:
            dictionary(dict): dictionary
            values(dict): dictionary
            
        Returns:
            dictionary(dict): dictionary with missing key/value pairs updated
        
        '''
        logging.debug('checking key/values')
        for k, v in values.items():
            try:
                dictionary[k]
            except KeyError as e:
                logging.debug(f'missing key: {k}; adding and setting to {v}')
                dictionary[k] = v
        return dictionary
    
    def _scalefont(self, font=None, lines=1, text="W W W ", dimensions=(100, 100)):
        '''Scale a font to fit the number of `lines` within `dimensions`
        
        Args:
            font(str): path to true type font
            lines(int): number of lines of text to fit within the `dimensions`
            dimensions(:obj:`tuple` of :obj:`int`): dimensions of pixles
            
        Returns:
            :obj:int: font size as integer
        
        '''
        if font:
            font = str(Path(font).resolve())
        else:
            font = str(Path(self.font).resolve())
            
        logging.debug('calculating font size')
        logging.debug(f'using font at path: {font}')
        
        
        # start calculating at size 1
        fontsize = 1
        x_fraction = .85        
        y_fraction = .7
        xtarget = dimensions[0]*x_fraction
        ytarget = dimensions[1]/lines*y_fraction
        testfont = ImageFont.truetype(font, fontsize)
        fontdim = testfont.getsize(text)
        
        logging.debug(f'target X font dimension {xtarget}')
        logging.debug(f'target Y dimension: {ytarget}')
        
        cont = True
        # work up until font covers img_fraction of the resolution return one smaller than this as the fontsize
#         while (fontdim[0] < xtarget) or (fontdim[1] < ytarget):
        while cont:
            fontsize += 1
            testfont = ImageFont.truetype(font, fontsize)
            
            fontdim = testfont.getsize(text)
#             logging.debug(f'size: {fontsize}; dimensions: {fontdim}')
            if fontdim[0] > xtarget:
                cont = False
                logging.debug(f'X target exceeded')
                
            if fontdim[1] > ytarget:
                cont = False
                logging.debug('Y target exceeded')
#             if (fontdim[0] > dimensions[0]) or (fontdim[1] > dimensions[1]):
#                 logging.warning(f'font dimension exceeds X or Y dimensions!')
#                 logging.debug(f'fontsize: {fontsize}; fontdim: {fontdim}; dimensions {dimensions}')
#                 logging.debug('setting font size to 1')
#                 return 1
            # need a check here to ensure that a minimum of 8-10 characters can fit on the line


            
        # back off one 
        fontsize -= 1
        logging.debug(f'test string: {text}; dimensions for fontsize {fontsize}: {fontdim}')
        return fontsize
    
    @property
    def layout(self):
        ''':obj:dict: dictonary of layout properties and rules for formatting text and image blocks
        
        Sets:
            blocks (dict): dict of ImageBlock or TextBlock objects 
        '''
        return self._layout
    
    @layout.setter
    def layout(self, layout):
        logging.debug(f'calculating values from layout for resolution {self.resolution}')
        if not layout:
            logging.info('no layout provided')
            self._layout = None
        else:
            self._layout = self._calculate_layout(layout)
            if self._layout:
                self._set_images()
            else:
                logging.debug('no layout provided')
    
    
    def _calculate_layout(self, layout):
        '''Calculate the size and position of each text block based on rules in layout
        
        Args:
            layout(dict): dictionary containing the layout to be used
        
        Returns:
            layout(dict): dictionary that includes rules and values for the layout
        '''
        if not layout:
            return None
        l = layout
        resolution = self.resolution
        # required values that will be used in calculating the layout
        values = {'image': None, 'max_lines': 1, 'padding': 0, 'width': 1, 'height': 1, 
                  'abs_coordinates': (None, None), 'hcenter': False, 'vcenter': False, 'rand': False,
                  'relative': False, 'font': self.font, 'fontsize': None, 'dimensions': None}        
        for section in l:
            logging.info(f'***{section}***')
            this_section = self._check_keys(l[section], values)
                    
            dimensions = (round(resolution[0]*this_section['width']), 
                          round(resolution[1]*this_section['height']))
            
            this_section['dimensions'] = dimensions
            logging.debug(f'dimensions: {dimensions}')       
        
            # set the thumbnail_size to resize the image
            if this_section['image']:
                maxsize = min(this_section['dimensions'])-this_section['padding']*2
                this_section['thumbnail_size'] = (maxsize, maxsize)
            
            # calculate the relative position if needed
            # if either of the coordinates are set as "None" - attempt to calculate the position
            if this_section['abs_coordinates'][0] is None or this_section['abs_coordinates'][1] is None:
                logging.debug(f'has calculated position')
                # store coordinates
                pos = []
                # check each value in relative section
                for idx, r in enumerate(this_section['relative']):
                    if r == section:
                        # use the value from this_section
                        pos.append(this_section['abs_coordinates'][idx])
                    else:
                        # use the value from another section
                        try:
                            pos.append(l[r]['dimensions'][idx] + l[r]['abs_coordinates'][idx])
                        except KeyError as e:
                            m = f'bad relative section value: "{r}" in section "{section}"'
                            raise KeyError(m)
                
                # save the values as a tuple
                this_section['abs_coordinates']=(pos[0], pos[1])
            else:
                logging.debug('has explict position')
                ac= this_section['abs_coordinates']
            logging.debug(f'abs_coordinates: {ac}')
                          
            # calculate fontsize
            if this_section['max_lines']:
                if not this_section['font']:
                    this_section['font'] = self.font
                          
                if not this_section['fontsize']:
                    this_section['fontsize'] = self._scalefont(font=this_section['font'], 
                                                               dimensions=this_section['dimensions'],
                                                               lines=this_section['max_lines'])    

            l[section] = this_section    
        return l
                              
    def _set_images(self):
        '''create dictonary of all image blocks with using the current set layout
        
         Sets:
            blocks (dict): dictionary of :obj:`TextBlock`, :obj:`ImageBlock`
            '''
                          
        
        layout = self.layout
        
        blocks = {}
        for sec in layout:
            logging.debug(f'***{sec}***)')
            section = layout[sec]
            # any section with max lines accepts text
            if section['max_lines']:
                logging.debug('set text block')
                blocks[sec] = Block.TextBlock(area=section['dimensions'], text='.', font=section['font'], 
                                       font_size=section['fontsize'], max_lines=section['max_lines'],
                                       hcenter=section['hcenter'], vcenter=section['vcenter'],
                                       rand=section['rand'], abs_coordinates=section['abs_coordinates'])
            if section['image']:
                logging.debug('set image block')
                blocks[sec] = Block.ImageBlock(image=None, abs_coordinates=section['abs_coordinates'], 
                                         area=section['dimensions'], hcenter=section['hcenter'],
                                         vcenter=section['vcenter'], padding=section['padding'])
        self.blocks = blocks
                              
    def update_contents(self, updates=None):
        '''Update the contents of the layout
        
        Args:
            updates(dict): dictionary of keys and values that match keys in `blocks`
        
        Sets:
            blocks 
        '''
        logging.debug('updating blocks')
        if not updates:
            logging.debug('nothing to do')
        
        for key, val in updates.items():
            if key in self.blocks:
                logging.debug(f'updating block: {key}')
                self.blocks[key].update(val)
            else:
                logging.debug(f'ignoring block {key}')




# In[29]:


# import logging
# # this works best as a global variable
# # logConfig = Path(cfg.LOGCONFIG)
# # logging.config.fileConfig(logConfig.absolute())
# # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')

# logging = logging.getlogging(__name__)
# logging.basicConfig(level=logging.DEBUG)




# In[37]:


# l = Layout(resolution=(600, 392))




# In[38]:


# l._scalefont(font='../fonts/Ubuntu/Ubuntu-Regular.ttf', dimensions=(600,392))




# In[ ]:







# In[ ]:





