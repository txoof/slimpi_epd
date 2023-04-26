#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[7]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./clock.ipynb')

#get_ipython().run_line_magic('nbconvert', '')




# In[1]:


from datetime import datetime



# In[2]:


def time_now(time):
    if not time:
        time = datetime.now()
    t = time.timetuple()
    rounded_min = (t.tm_min + round(t.tm_sec/60)) % 60
    rounded_time = time.replace(minute=rounded_min)
    return rounded_time.strftime("%H:%M")




# In[6]:


def update(time=None):
    myTime = {'time': time_now(time),
              'mode': None}
    return  myTime




# In[ ]:





