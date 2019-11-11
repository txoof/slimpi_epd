#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[ ]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./TextBlock.ipynb')




# In[ ]:


#get_ipython().run_line_magic('nbconvert', '')




# In[1]:


import logging
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import constants




# In[2]:


class TextBlock:
    '''Class for creating 1 bit image of word-wrapped text.
    
    TextBlock objects contain an image of formatted text bounded by size `area` 
    that can be used to assemble a larger composite image. The text is 
    word-wrapped and formatted based on area size, font size, and centering rules.
    TextBlocks are aware of their position (`abs_coordinates`) within a larger 
    image and the position of the formatted text. The position of the text, 
    relative to the larger image is calculated and stored in `img_coordinates`. 
    
    example: t = TextBlock(text='Lorem ipsum dolor sit amet', max_lines=2, 
                           font_size=24, hcenter=True, vcenter=False, 
                           abs_coordinates=(100, 96))
    
    Attributes:
        area (:obj:`tuple` of :obj: `int`): x, y integer dimensions of 
            maximum area in pixles
        text (str): text to be formatted and converted into image
        font (str): path to TTF font
        font_size (int): size of font in points
        max_lines (int): maximum number of lines to return after wrapping text
        maxchar (int): maximum number of characters per line (calculated if not provided
        abs_coordinates (:obj:`tuple` of `int`): x, y integer coordinates of image area
            within a larger image
        hcenter (boolean): True - horizontal-align text within the area, 
            False - left-align text
        vcenter (boolean): True - vertical-align text within the area,
            False - top-align text
        img_coordinates (:obj:`tuple` of `int`): x, y calculated integer 
            coordinates of image within the larger image - calculation is based 
            on centering, image size
        chardist (:obj:dict of :obj:str : :obj:float): dictionary describing
            letter frequency in a language for calcualting maxchar
        image (PIL.Image): Image to be formatted and resized to fit within
            area
    '''
    
    def __init__(self, area=(600, 448), text=' ', font=None, font_size=24, max_lines=1,
                maxchar=None, hcenter=False, vcenter=False, abs_coordinates=(0,0), 
                chardist=None):
        '''Constructor for TextBlock Class.
        
        Args:
            area (:obj:`tuple` of :obj: `int`): x, y integer dimensions of 
                maximum area in pixles
        text (str): text to be formatted and converted into image
        font (str): path to TTF font
        font_size (int): size of font in points
        max_lines (int): maximum number of lines to return after wrapping text
        maxchar (int): maximum number of characters per line (calculated if not provided
        hcenter (boolean, optional): True - horizontal-align text within the area, 
            False - left-align text
        vcenter (boolean, optional): True - vertical-align text within the area,
            False - top-align text
        abs_coordinates (:obj:`tuple` of `int`): x, y integer coordinates of image area
            within a larger image            
        chardist (:obj:dict of :obj:str : :obj:float): dictionary describing
            letter frequency in a language for calcualting maxchar
            '''    
        
        self.area = area
        if font:
            self.font = ImageFont.truetype(str(Path(font).absolute()), size=font_size)
        else:
            self.font = ImageFont.truetype(str(Path(constants.FONT).absolute()), size=font_size)
        
        if chardist:
            self._chardist = chardist
        else:
            self._chardist = constants.USA_CHARDIST
        self.max_lines = max_lines
        self.maxchar = maxchar
        
        self.hcenter = hcenter
        self.vcenter = vcenter
        
        self.abs_coordinates = abs_coordinates
        
        self.image = None
        
        self.text = text
    
    def update(self, update=None):
        '''Generic update function the object with the incoming data.
        
        Method is used by other class objects to update all image blocks 
        
        Args:
            update (str): path to image file
                
        Returns:
            bool: True upon success'''
        if update:
            try:
                self.text = update
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
    def maxchar(self):
        '''int: maximum number of characters per line - if no value 
                is provided, this will be calculated
        
        If no value is provided, a random string of characters is generated based on the
        frequency tables: `chardist`. The default distribution is American English. 
        Based on this string the maximum number of characters for a given font and font size.
            
        '''
        return self._maxchar
    
    @maxchar.setter
    def maxchar(self, maxchar):
        if maxchar:
            self._maxchar = maxchar
        else:
            s = ''
            n = 1000
            # create a string of characters containing the letter distribution
            for char in self._chardist:
                s = s+(char*int(self._chardist[char]*n))
            s_length = self.font.getsize(s)[0] # string length in Pixles
            avg_length = s_length/len(s)
            maxchar = round(self.area[0]/avg_length)
            self._maxchar = maxchar
            logging.debug(f'maximum characters per line: {maxchar}')
    
    @property
    def abs_coordinates(self):
        ''':obj:`tuple` of :obj:`int`: absolute_coordinates of area within larger image.
        
        Setting `abs_coordinates` atomatically sets `img_coordinates` to the same value.'''
        return self._abs_coordinates
    
    @abs_coordinates.setter
    def abs_coordinates(self, abs_coordinates):
        if self._coordcheck(abs_coordinates):
            self._abs_coordinates = abs_coordinates
            self.img_coolrdinates = abs_coordinates
            logging.debug(f'absolute coordinates: {abs_coordinates}')
        else:
            raise ValueError(f'bad absoluote coordinates: {abs_coordinates}')
            
    
    @property
    def text(self):
        ''':obj:`str`: raw text to be formatted.
        
        setting or resetting this property will also set the following attributes
            text (str): unformatted raw text
            text_formatted (list): of (str): wrapped text
            image (:obj:`PIL.Image`): image based on wrapped and formatted text
            img_coordinates (:obj:`tuple` of :obj:`int`): coordinates of text image adjusted 
                for size of textblock'''
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text
        self.text_formatted = self.text_formatter()
        self.image = self._text2image()
    
    def text_formatter(self, text=None, max_lines=None, maxchar=None):
        '''format text using word-wrap strategies. 
        
        Formatting is based on number of lines, area size and maximum characters per line
        
        Args:
            text (str): raw text
            maxchar (int): maximum number of characters on each line
            max_lines (int): maximum number of lines
            
        Returns:
            :obj:`list` of :obj:`str`
        '''
        if not text:
            text = self.text
        if not maxchar:
            maxchar = self.maxchar
        if not max_lines:
            max_lines = self.max_lines
        
        wrapper = textwrap.TextWrapper(width=maxchar, max_lines=max_lines)
        formatted = wrapper.wrap(text)
        logging.debug(f'formatted list:\n {formatted}')
        return(formatted)
    
    def _text2image(self):
        '''produces 1 bit image containing wrapped text.
        
        calling this method will set `img_coordinates`
            based on image size, hcenter and vcenter rules
        
        Sets:
            dimensions (tuple): of (int) - dimensions of text image
            img_coordinates (tuple): of int - absolute coordinates of text image 
        
        Returns:
            :obj:`PIL.Image`
        '''
        
        # determine the extents of the text block image
        y_total = 0
        x_max = 0
        
        for line in self.text_formatted:
            x, y = self.font.getsize(line)
            y_total += y # accumulate the total height
            if x > x_max:
                x_max = x # find the longest line
        
        # set dimensions of the text block image
        self.dimensions = (x_max, y_total)
        logging.debug(f'text image dimensions: {self.dimensions}')
        
        # build image
        image = Image.new('1', self.dimensions, 255)
        # get a drawing context
        draw = ImageDraw.Draw(image)
        
        y_total = 0
        for line in self.text_formatted:
            x_pos = 0
            x, y = self.font.getsize(line)
            if self.hcenter:
                logging.debug(f'h-center line: {line}')
                x_pos = round(self.dimensions[0]/2-x/2)
            draw.text((x_pos, y_total), line, font=self.font)
            y_total += y
        
        # set image coordinates
        new_x, new_y = self.abs_coordinates
        if self.hcenter:
            logging.debug(f'h-center image coordinates')
            new_x = self.abs_coordinates[0] + round(self.area[0]/2 - self.dimensions[0]/2)

            
        if self.vcenter:
            logging.debug(f'v-center image coordinates')
            new_y = self.abs_coordinates[1] + round(self.area[1]/2 - self.dimensions[1]/2)
        
        if self.hcenter or self.vcenter:
            logging.debug(f'image coordinates {(new_x, new_y)}')
            self.img_coordinates = (new_x, new_y)
        
        return image
    
    
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




# In[4]:





