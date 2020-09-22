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
    return int(x.replace(",",""))


# In[15]:


url = "https://www.topcv.vn/tim-viec-lam-moi-nhat"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_r = soup.find("span", class_="big-number text-highlight").get_text()
total_jobs = to_int(total_jobs_r)
print(total_jobs)


# In[4]:


topcv_result = {'Total Jobs': total_jobs}
topcv_result_sen = pd.DataFrame(topcv_result, columns=['Total Jobs', 'Intern', 'Junior', 'Senior', 'Manager/Director'], index=[0])
topcv_result_sen


# In[ ]:


from datetime import date
topcv_result_sen.to_csv(f'topcv-sen-{date.today()}.csv')

