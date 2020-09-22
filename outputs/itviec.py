#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

def to_int(x):
    if type(x) is int:
        return x
    return int(x.replace(",","").replace(".",""))


# In[2]:


url = "https://itviec.com/it-jobs"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

jobs = soup.find("div", id ="jobs").find("h1").get_text()
total_jobs = to_int(jobs.split()[0])


# In[3]:


url = "https://itviec.com/it-jobs/senior"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

jobs = soup.find("div", id ="jobs").find("h1").get_text()
senior = to_int(jobs.split()[0])


# In[4]:


url = "https://itviec.com/it-jobs/manager"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

jobs = soup.find("div", id ="jobs").find("h1").get_text()
manager = to_int(jobs.split()[0])


# In[6]:


ITViec = {
        'Total Jobs': total_jobs,
        'Junior': senior-manager,
        'Senior': senior,
        'Manager/Director': manager,
        }

df = DataFrame(ITViec, columns= ['Total Jobs', 'Junior', 'Senior', 'Manager/Director'],index=[0])


# In[12]:


from datetime import date
df.to_csv(f'itviec-sen-{date.today()}.csv')


# In[ ]:




