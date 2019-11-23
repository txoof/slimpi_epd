#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[1]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./Screen.ipynb')




# In[320]:


#get_ipython().run_line_magic('nbconvert', '')




# In[5]:


import logging
from PIL import Image, ImageDraw, ImageFont
import time




# In[321]:


class Update:
    '''class for creating a montotonicly aware object that records passage of time
    
    create an update aware object:
        myObj = Update()
        
    Time since creation:
        myObj.age
        
    Time since last updated:
        myObj.last_updated
        
    
    Update the object:
        myObj.update = True

    '''
    
    def __init__(self):
        '''constructor for Update class'''
        
        self.start = self.now
        self.update = True
        
    @property
    def age(self):
        '''age of the object in seconds since created'''
        return self.now - self.start
    
    @property
    def now(self):
        return time.clock_gettime(time.CLOCK_MONOTONIC)
    
    @property
    def last_updated(self):
        '''seconds since object was last updated'''
        return self.now - self._last_updated
    
    @last_updated.setter
    def update(self, update=True):
        '''update the object
        
        Args:
            update(boolean): True updates object'''
        if update:
            self._last_updated = self.now
    




# In[8]:


class Screen:
    '''Class for interfacting with WaveShare EPD screens.
    
    `Screen` creates an object that provides methods for assembling images
    and updating a WaveShare EPD.
    
    Attributes:
        resolution (:obj:`tuple` of :obj: `int`): resolution of EPD
        elements (:obj:`list` of :obj:`ImageBlock` or `TextBlock`): images to be assembled
        image (:obj:`PIL.Image`): composite image to be written to screen
        epd (:obj:`waveshare.epd`): waveshare EPD object 
    '''
    def __init__(self, resolution=(600, 448), elements=[], epd=None):
        '''Constructor for Screen class.
        
        Args:
            resolution (:obj:`tuple` of :obj:`int`): resolution of EPD
            elements (:obj:`list` of :obj:`ImageBlock` or `TextBlock`): images to be assembled
            image (:obj:`PIL.Image`): composite image to be written to screen
            epd (:obj:`waveshare.epd`): waveshare EPD object
        Properties:
            resolution (tuple): resolution of screen
            elements (:obj:`list` of :obj:`PIL.Image`: list of all image objects that form the larger image'''
        self.resolution = resolution
        self.elements = elements
        self.image = self.clearScreen()
        self.epd = epd
        self.update = Update()
        
    def clearScreen(self):
        '''Sets a clean base image for building screen layout.
        
        Returns:
            :obj:PIL.Image
        '''
        image = Image.new('L', self.resolution, 255)
        return image
    
    def concat(self, elements=None):
        '''Concatenate multiple image objects into a single composite image
        
        Args:
            elements (:obj:`list` of :obj:`ImageBlock` or `TextBlock`) - if none are
                provided, use the existing elements
                
        Sets:
            image (:obj:`PIL.Image`): concatination of all image members of `elements` 
            last_updated (:obj: `Update`): registeres the time the images were updated
            
        Returns:
            image (:obj:`PIL.Image`)
        '''
        self.image = self.clearScreen()
        # register that the object has been modified
        self.update.update = True
        if elements:
            elements = elements
        else:
            elements = self.elements
            
        for e in elements:
            logging.debug(f'pasting image at: {e.img_coordinates}')
            self.image.paste(e.image,  e.img_coordinates)
        return(self.image)
    
    def initEPD(self):
        '''Initialize the connection with the EPD Hat.
        
        Returns:
            bool: True if successful
        '''
        if not self.epd:
            raise UnboundLocalError('no epd object has been assigned')
        try:
            self.epd.init()
        except Exception as e:
            logging.error(f'failed to init epd: {e}')
        return True
    
    def clearEPD(self):
        '''Clear the EPD screen.
        
        Raises:
            UnboundLocalError: no EPD has been intialized
        
        Returns:
            bool: True if successful'''
        if not self.epd:
            raise UnboundLocalError('no epd object has been assigned')
        try:
            self.epd.Clear();
        except Exception as e:
            logging.error(f'failed to clear epd: {e}')
        return True
    
    def writeEPD(self, image=None, sleep=True):
        '''Write an image to the EPD.
        
        Args:
            image (:obj:`PIL.Image`, optional): if none is provided use object `image`
            sleep (bool): default - True; put the EPD to low power mode when done writing
            
        Returns:
            bool: True if successful
        '''
        epd = self.epd
        if not self.epd:
            raise UnboundLocalError('no epd object has been assigned')
        try:
            epd.display(epd.getbuffer(self.image))
            if sleep:
                epd.sleep()
        except Exception as e:
            logging.error(f'failed to write to epd: {e}')
            return False
        return True
        


