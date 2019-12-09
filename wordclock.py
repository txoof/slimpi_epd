#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[28]:


#get_ipython().magic(u'alias nbconvert nbconvert ./wordclock.ipynb')

#get_ipython().magic(u'nbconvert')




# In[48]:


import logging
from datetime import datetime
from random import choice




# In[40]:


def time_list(time):
    '''Returns time as list [h, m] of type int
    
    Args:
        time(`str`): time in colon separated format - 09:34; 23:15'''
    return  [int(i)  for i in time.split(':')]




# In[14]:


def time_now():
    return datetime.now().strftime("%H:%M")




# In[89]:


def map_val(a, b, s):
    '''map range `a` to `b` for value `s`

    Args:
        a(2 `tuple` of `int`): (start, end) of input values
        b(2 `tuple` of `int`): (start, end) of output values
        s(`float`, `int`): value to map
    Returns:
        `int`'''
    a1, a2 = a
    b1, b2 = b
    
    t = b1 + ((s-a1) * (b2-b1))/(a2-a1)
    
    return round(t)




# In[90]:


# def maprange(a, b, s):
#     '''map range `a` to `b` for value `s`

#     Args:
#         a(2 `tuple` of `int`): (start, end) of input values
#         b(2 `tuple` of `int`): (start, end) of output values
#         s(`float`, `int`): value to mape
#     Returns:
#         `int`'''
    
#     (a1, a2), (b1, b2) = a, b
#     return  int(b1 + ((s - a1) * (b2 - b1) / (a2 - a1)))




# In[293]:


def get_time(time=None):    
    hours = {'1':  ['one', 'late'],
             '2':  ['two', 'really late', 'go to bed'],
             '3':  ['three', 'too late', "why aren't you in bed"],
             '4':  ['four', 'early morning', 'stupid early'],
             '5':  ['five'],
             '6':  ['six'],
             '7':  ['seven'],
             '8':  ['eight'],
             '9':  ['nine'],
             '10': ['ten'],
             '11': ['eleven'],
             '12': ['noon', 'twelve'],
             '13': ['one'],
             '14': ['two'],
             '15': ['three'],
             '16': ['four'],
             '17': ['five'],
             '18': ['six'],
             '19': ['seven'],
             '20': ['eight'],
             '21': ['nine'],
             '22': ['ten'],
             '23': ['eleven'],
             '0' : ['midnight', 'twelve', 'dark']}

    minutes = {'0': ["'o clock", "on the dot"],
               '6': ["'o clock", "on the dot"],
               '1': ['ten after'],
               '2': ['twenty after'],
               '3': ['half past', 'thirty after', 'thirty past'],
               '4': ["twenty 'til"],
               '5': ["ten 'til"]}

    stems = ['The time is', "It is about", "It is around", "It is almost"]


    if time:
        now = time
        logging.debug(f'using {time}')
        t_list = time_list(time)
    else:
        now = time_now()
        logging.debug(f'using {now}')
        t_list = time_list(now)
        
    # this range shifts the period of the list so times around the 'tens' round nicely up and down        
    minute = map_val((1, 59), (0, 6), t_list[1])

    # set the hour appropriately
    if t_list[1] <= 30:
        hour_str = hours[str(t_list[0])]
    else:
        try:
            hour_str = hours[str(t_list[0]+1)]
        except KeyError as e:
            # wrap around to zero'th index in the hours list
            hour_str = hours[str(t_list[0]+1 - len(hours))]
            hour_str = hours[str(0)]
        
    min_str = minutes[str(minute)]
    
    # properly organize the time string
    # 'o clock times
    if minute == 0 or minute == 6:
        time_str = f'{choice(hour_str).title()} {choice(min_str).title()}'
                      
    else: 
        time_str = f'{choice(min_str).title()} {choice(hour_str).title()}'
    
    
    myTime = {'wordtime': f'{choice(stems)} {time_str}',
              'time': now,
              'mode': None}
    
    
    return myTime




# In[292]:


get_time('12:25')




# In[96]:


for i in range(60):
    print(f'{i} maps to: {map_vals((1, 59), (0, 6), i)}')




# In[95]:


for i in range(60):
     print(f'{i}: maps to {maprange((-4, 55), (0, 6), i)}')


