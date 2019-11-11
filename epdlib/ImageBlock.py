#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[3]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./ImageBlock.ipynb')




# In[12]:


#get_ipython().run_line_magic('nbconvert', '')




# In[5]:


import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont




# In[11]:


class ImageBlock:
    '''Class for creating 1 bit image of word-wrapped text.
    
    ImageBlock objects contain an image block bounded by size `area` that can 
    be used to assemble a larger composite image. ImageBlocks are aware of 
    their position (`abs_coordinates`) within the larger image and the position 
    of the formatted (resized) image. The position of the formatted image, 
    relative to the larger image is calculated and stored in `img_coordinates`. 
    
    example: i = ImageBlock(image='./cover.jpg', area=(150, 205), 
                            abs_coordinates=(0, 0), hcenter=True, 
                            vcenter=False, padding=10)
        
    Attributes:
        image (PIL.Image): Image to be formatted and resized to fit within
            area
        area (:obj:`tuple` of :obj: `int`): x, y integer dimensions of 
            maximum area in pixles
        abs_coordinates (:obj:`tuple` of `int`): x, y integer coordinates of image area
            within a larger image
        img_coordinates (:obj:`tuple` of `int`): x, y calculated integer 
            coordinates of image within the larger image - calculation is based 
            on centering, image size
        hcenter (boolean): True - horizontal-align image within the area, 
            False - left-align image
        vcenter (boolean): True - vertical-align image within the area,
            False - top-align image
        padding (int): amount of padding between resized image and edge of area
    '''
    def __init__(self, image=None, area=(0, 0), abs_coordinates=(0, 0), hcenter=False, vcenter=True, padding=0):
        '''Constructor for ImageBlock Class.
        
        Args:
            image (PIL.Image): Image to be formatted and resized to fit within
                area
            area (:obj:`tuple` of :obj: `int`): x, y integer dimensions of 
                maximum area in pixles
            abs_coordinates (:obj:`tuple` of `int`): x, y integer coordinates of image area
                within a larger image
            hcenter (boolean, optional): True - horizontal-align image within the area, 
                False - left-align image
            vcenter (boolean, optional): True - vertical-align image within the area,
                False - top-align image
            padding (int, optional): amount of padding between resized image and edge of area'''
        self.area = area
        self.abs_coordinates = abs_coordinates
        self.hcenter = hcenter
        self.vcenter = vcenter
        self.padding = padding
        self.image = image

    def update(self, update=None):
        '''Generic update function the object with the incoming data.
        
        Method is used by other class objects to update all image blocks 
        
        Args:
            update (str): path to image file
                
        Returns:
            bool: True upon success'''
        if update:
            try:
                self.image = update
            except Excepiton as e:
                logging.error(f'failed to update: {e}')
                return False
            return True
    
    @property
    def area(self):
        ''':obj:`tuple` of :obj:`int`: maximum area of imageblock'''
        return self._area

    @area.setter
    def area(self, area):
        if self._coordcheck(area):
            self._area = area
            logging.debug(f'maximum area: {area}')
        else:
            raise ValueError(f'bad area value: {area}')    

    @property
    def abs_coordinates(self):
        ''':obj:`tuple` of :obj:`int`: absolute_coordinates of area within larger image.
        
        Setting `abs_coordinates` atomatically sets `img_coordinates` to the same value.
        '''
        return self._abs_coordinates
    
    @abs_coordinates.setter
    def abs_coordinates(self, abs_coordinates):
        if self._coordcheck(abs_coordinates):
            self.img_coordinates = abs_coordinates
            self._abs_coordinates = abs_coordinates
        else:
            raise ValueError(f'bad absolute coordinates: {abs_coordinates}')
    
    @property
    def image(self):
        ''':obj:`PIL.Image`: resizes, and centers image to fit within the `area`
        
        Setting/Updating `image` recalculates `img_coordinates`'''
        return self._image
    
    @image.setter
    def image(self, image):
        if not image:
            self._image = None
            return None
        logging.debug(f'formatting image: {image}')
        dim = min(self.area)-self.padding
        logging.debug(f'set image dimensions: {dim}')
        size = (dim, dim)
        im = Image.open(image)
        im.convert(mode='L', colors=2)
        im.thumbnail(size)
        self.dimensions = im.size
        x_new, y_new = self.abs_coordinates
        
        if self.hcenter:
            x_new = self.abs_coordinates[0] + round(self.area[0]/2 - self.dimensions[0]/2)
        if self.vcenter:
            y_new = self.abs_coordinates[1] + round(self.area[1]/2 - self.dimensions[1]/2)
        
        if self.hcenter or self.vcenter:
            self.img_coordinates = (x_new, y_new)
        logging.debug(f'set img_coordinates: {self.img_coordinates}')
            
        self._image = im
        return im
    
    def _coordcheck(self, coordinates):
        '''Check that coordinates are of type int and positive.
        
        Args:
            coordinates (:obj:`tuple` of :obj: `int`)
            
        Raises:
            TypeError: `coordinates` are not a list or tuple
            TypeError: `coordinates` elements are not an integer
            ValueError: `coordinates` are not >=0
            '''
        if not isinstance(coordinates, (tuple, list)):
            raise TypeError(f'must be type(list, tuple): {coordinates}')
        for i, c in enumerate(coordinates):
            if not isinstance(c, int):
                raise TypeError(f'must be type(int): {c}')
                return False
            if c < 0:
                raise ValueError(f'coordinates must be positive: {c}')
                return False
        return True            


