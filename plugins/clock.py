#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[7]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./clock.ipynb')

#get_ipython().run_line_magic('nbconvert', '')




# In[1]:


from datetime import datetime




# In[2]:


def time_now():
    return datetime.now().strftime("%H:%M")




# In[6]:


def update():
    myTime = {'time': time_now(),
              'mode': None}
    return  myTime




# In[ ]:





