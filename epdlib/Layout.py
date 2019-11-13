#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[11]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert Layout.ipynb')




# In[14]:


#get_ipython().run_line_magic('nbconvert', '')




# In[16]:


import logging
from pathlib import Path
import copy
from . import layouts
from . import constants
from PIL import Image, ImageDraw, ImageFont
# from TextBlock import TextBlock
# from ImageBlock import ImageBlock
from . import Block




# In[5]:


class Layout:
    '''Class for defining layout of epd screen
    
    This class allows screen layouts to be declared in terms of image blocks in an X, Y plane. 
    Block placement is defined in terms of absolute or relative positions. Only one block 
    with absolute coordinates is needed. Block size is calculated based on screen size.
    
    Attributes:
        resolution (:obj:`tuple` of :obj: `int`): X, Y screen resolution in pixles
        font (str): path to font file
        layout (dict): dictionary with layout instructions (see below)
        
    '''
    def __init__(self, resolution=(600, 448), layout=None, font=constants.FONT):
        self.resolution = resolution
        self.font = str(Path(font).resolve())
        self.layout = copy.deepcopy(layout)
        self.images = None

    def _check_keys(self, dictionary={}, values={}):
        logging.debug('checking key/values')
        for k, v in values.items():
            try:
                dictionary[k]
            except KeyError as e:
                logging.debug(f'missing key: {k}; adding and setting to {v}')
                dictionary[k] = v
        return dictionary
    
    def _scalefont(self, font=None, lines=1, text="W", dimensions=(100, 100)):
        
        if font:
            font = str(Path(font).resolve())
        else:
            font = str(Path(self.font).resolve())
            
        logging.debug('calculating font size')
        logging.debug(f'using font at path: {font}')
        
        
        # start calculating at size 1
        fontsize = 1
        y_fraction = .7
        target = dimensions[1]/lines*y_fraction
        testfont = ImageFont.truetype(font, fontsize)
        fontdim = testfont.getsize(text)
        
        logging.debug(f'target Y fontsize: {target}')
        
        # work up until font covers img_fraction of the resolution return one smaller than this as the fontsize
        while fontdim[1] < target:
            fontdim = testfont.getsize(text)
            if fontdim[1] > dimensions[1]:
                logging.warn('font Y dimension is larger than Y area; bailing out')
                break
            fontsize += 1
            testfont = ImageFont.truetype(font, fontsize)
            
        # back off one 
        fontsize -= 1
        logging.debug(f'fontsize: {fontsize}')
        return fontsize
    
    @property
    def layout(self):
        return self._layout
    
    @layout.setter
    def layout(self, layout):
        logging.debug(f'calculating values from layout for resolution {self.resolution}')
        if not layout:
            logging.info('no layout provided')
            self._layout = None
        else:
            self._layout = self.calculate_layout(layout)
#             self.set_images()
    
    
    def calculate_layout(self, layout):
        if not layout:
            return None
        l = layout
        resolution = self.resolution
        # required values that will be used in calculating the layout
        values = {'image': None, 'max_lines': 1, 'padding': 0, 'width': 1, 'height': 1, 
                  'abs_coordinates': (None, None), 'hcenter': False, 'vcenter': False, 'relative': False, 
                  'font': self.font, 'fontsize': None, 'dimensions': None}        
        for section in l:
            logging.debug(f'***{section}***')
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
                        pos.append(l[r]['dimensions'][idx] + l[r]['abs_coordinates'][idx])
                
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
                              
    def set_images(self):
        '''create dictonary of all image blocks with using the current set layout
        
            Sets
            ----
                ::blocks :dict of: TextBlock(), ImageBlock()
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
                                       abs_coordinates=section['abs_coordinates'])
            if section['image']:
                logging.debug('set image block')
                blocks[sec] = Block.ImageBlock(image=None, abs_coordinates=section['abs_coordinates'], 
                                         area=section['dimensions'], hcenter=section['hcenter'],
                                         vcenter=section['vcenter'], padding=section['padding'])
        self.blocks = blocks
                              
    def update_contents(self, updates=None):
        if not updates:
            logging.debug('nothing to do')
        
        for key, val in updates.items():
            self.blocks[key].update(val)


