#!/usr/bin/env ipython
#!/usr/bin/env python
# coding: utf-8


# In[13]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./WordClock.ipynb')

#get_ipython().run_line_magic('nbconvert', '')




# In[7]:


from datetime import datetime
from random import choice




# In[8]:


def time():
    return  datetime.now().strftime("%H,%M").split(',')




# In[9]:


def time_now():
    return datetime.now().strftime("%H:%M")




# In[10]:


def maprange(a, b, s):
    '''map range `a` to `b` for value `s`

    Args:
        a(2 `tuple` of `int`): (start, end) of input values
        b(2 `tuple` of `int`): (start, end) of output values
        s(`float`, `int`): value to mape
    Returns:
        `int`'''
    
    (a1, a2), (b1, b2) = a, b
    return  int(b1 + ((s - a1) * (b2 - b1) / (a2 - a1)))




# In[12]:


def get_time():    
    hours = {'1':  ['one', 'late'],
             '2':  ['two', 'really late'],
             '3':  ['three', 'too late'],
             '4':  ['four', 'early morning'],
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
             '0' : ['midnight', 'twelve', "'o dark'"]}

    minutes = {'0': ["'o clock"],
               '6': ["'o clock"],
               '1': ['ten after'],
               '2': ['twenty after'],
               '3': ['half past', 'thirty after', 'thirty past'],
               '4': ["twenty 'til"],
               '5': ["ten 'til", 'twenty over half past']}

    stems = ['The time is', "It's about", "It's around"]

    # this range shifts the period of the list so times around the 'tens' round nicely up and down
    minute = maprange((-5, 55), (0, 6), int(time()[1]))
    hour_str = hours[time()[0]]
    min_str = minutes[str(minute)]
    
    myTime = {'wordtime': f'{choice(stems)} {choice(min_str).title()} {choice(hour_str).title()}',
              'time': time_now(),
              'mode': None}
    
    
    return myTime




# In[ ]:





