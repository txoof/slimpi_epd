#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[16]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./decimal_binary_clock.ipynb')

#get_ipython().run_line_magic('nbconvert', '')




# In[4]:


from datetime import datetime
from PIL import Image, ImageDraw
import re




# In[5]:


def check_num(func):
    """decorator function wrapper"""
    def func_wrapper(d, *args, **kwargs):
        """Check for positive integers
        Params:
            d(int): integer to check
        
        Raises:
            ValueError - values that are negative, not integer or greater than 99"""
#         if d > 99:
#             raise ValueError (f'{d} is > 99')
        if not isinstance(d, int):
            raise ValueError (f'{d} is not an integer')
        if d < 0:
            raise ValueError (f'{d} < 0 {func} only accepts values >= 0')
        return func(d, *args, **kwargs)
    return func_wrapper




# In[6]:


@check_num
def split_place_value(d):
    tens = int((d-(d%10))/10)
    ones = int(d-tens*10)
    return tens, ones




# In[7]:


def time_now():
    return datetime.now().strftime("%H:%M")




# In[8]:


def split_by_place(d):
    num_list = []
    for i in str(d):
        num_list.append(int(i))
    
    return num_list




# In[9]:


@check_num
def dec2bin(d, min_bits=4):
    bin_array = []
    whole = d
    while whole > 0:
        remainder = whole%2 
        whole = int(whole/2)
        bin_array.append(remainder)
        
    if len(bin_array) < min_bits:
        for i in range(0, min_bits-len(bin_array)):
            bin_array.append(0)

    return bin_array[::-1]




# In[10]:


def dot_array(r, border, array, padding):
    dim = [(r*2)+padding*2, len(array)*(r*2)+padding*(len(array)+1)] 
    image = Image.new('1', dim, color=1)
    d = ImageDraw.Draw(image)
    for idx, val in enumerate(array):
        topOuter = [0+padding, (r*2*idx)+padding+padding*idx]
        bottomOuter = [r*2+padding, r*2*(idx+1)+padding+padding*idx]
        topInner = [topOuter[0]+border, topOuter[1]+border]
        bottomInner = [bottomOuter[0]-border, bottomOuter[1]-border]
        d.ellipse(topOuter+bottomOuter, fill=0)
        if val==0:
            d.ellipse(topInner+bottomInner, fill=1)
    
    return image




# In[11]:


def separator(dim, padding):
    dim = [dim[0]+padding, dim[1]+padding]
    top = [padding, padding]
    bottom = dim
    i = Image.new('1', dim, color=1)
    d = ImageDraw.Draw(i)
    d.rectangle(top+bottom, fill=0)
    
    return i




# In[14]:


def update(time=None):
    r = 80
    border = 10
    padding = 10
    time_array = []
    img_x = 0
    img_y = 0
    img_array = []
    return_time = None

    # break the time string into digits if provided
    if time:
        return_time = str(time)
        time = str(time)
        match = re.search('([0-9]{1,2}):([0-9]{1,2})', time)
        hour = match.group(1)
        minute = match.group(2)
    else:
        hour = datetime.now().hour
        minute = datetime.now().minute
        return_time = f'{hour:02}:{minute:02}'
    
    
    # make sure there are two digits in hour
    if len(str(hour)) < 2:
        time_array = [0]
    
    # join up the hours and the colon 
    time_array = time_array + split_by_place(hour) + [-1]
    
    # make sure there are two digits in minute
    if len(str(minute)) < 2:
        time_array = time_array + [0]
    
    # join up the hours, colon and minute
    time_array = time_array + split_by_place(minute)
    
    # build an array of the images
    for i in time_array:
        # separator is represented by a negative number
        if i < 0:
            img_array.append(separator(dim=[r, 4*(r*2)+padding*5], padding=0))
        # create a dot array for each decimal place
        else:
            img_array.append(dot_array(r=r, border=border, padding=padding, array=dec2bin(i)))
    
    # determine dimensions of array
    for j in img_array:
        img_x = img_x + j.width
        if j.height > img_y:
            img_y = j.height
            
    # create a blank image
    img = Image.new('1', [img_x, img_y], color=1)
    
    # build the composite image
    x_pos = 0
    y_pos = 0
    for j in img_array:
        img.paste(j, [x_pos, y_pos])
        x_pos = x_pos + j.width
    
    return {'bin_img': img, 'time': return_time, 'mode': None}     




# In[ ]:





