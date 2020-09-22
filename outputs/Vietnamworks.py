#!/usr/bin/env python
# coding: utf-8

# In[50]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

def to_int(x):
    return int(x.replace(",",""))


# In[51]:


url="https://jf8q26wwud-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser&x-algolia-application-id=JF8Q26WWUD&x-algolia-api-key=2bc790c0d4f44db9ab6267a597d17f1a"

payload={"requests":[{"indexName":"vnw_job_v2","params":"query=&query=&facetFilters=%5B%5D&numericFilters=%5B%5D&page=0&hitsPerPage=50&restrictSearchableAttributes=%5B%22jobTitle%22%2C%22skills%22%2C%22company%22%5D&attributesToRetrieve=%5B%22*%22%2C%22-jobRequirement%22%2C%22-jobDescription%22%5D"}]}


# In[52]:


import json
r = requests.post(url, data=json.dumps(payload))


# In[53]:


total_job = r.json()["results"][0]["nbHits"]


# In[54]:


industry_url="https://www.vietnamworks.com/tim-viec-lam"

page = requests.get(industry_url)

soup = BeautifulSoup(page.text, 'html.parser')


# In[55]:


industries = soup.find("div", class_="highlight").find_all("dd")

full_ind = []
full_no_of_job = []
for industry in industries:
  tmp = industry.get_text().split()
  no_of_jobs=str(tmp[-1])[1:-1]
  tmp = tmp[0:-1]
  ind = " ".join(tmp)
  full_ind.append(ind)
  full_no_of_job.append(int(no_of_jobs))


# In[56]:


Vietnamwork_ind = {'Industry': full_ind,
                   'No. of Jobs': full_no_of_job}
Vietnamwork_result_ind = pd.DataFrame(Vietnamwork_ind, columns=['Industry', 'No. of Jobs'])
Vietnamwork_result_ind = Vietnamwork_result_ind.sort_values(by=['No. of Jobs'], ascending=False)

Vietnamwork_result_ind


# In[57]:


Vietnamwork = {'Total Jobs': total_job}

df = DataFrame(Vietnamwork, columns= ['Total Jobs'], index=[0])


# In[58]:


industries = soup.find_all("div", class_="highlight")[2].find_all("dd")


full_ind = []
full_no_of_job = []

for industry in industries:
  tmp = industry.get_text().split()
  no_of_jobs=str(tmp[-1])[1:-1]
  tmp = tmp[0:-1]
  ind = " ".join(tmp)
  full_ind.append(ind)
  full_no_of_job.append(int(no_of_jobs))

demo = {'Senority': full_ind,
        'Jobs by Senority': full_no_of_job
        }

senority_pd_r = DataFrame(demo, columns= ['Senority', 'Jobs by Senority'])


# In[59]:


s = senority_pd_r.set_index('Senority')
senority_pd = s.transpose()

senority_dict = senority_pd.to_dict()
# d = senority_dict.get(0)
# d
# Vietnamwork.update(senority_dict)

senority_final = {}
for key in senority_dict.keys():
    senority_final[key] = senority_dict[key]["Jobs by Senority"]
Vietnamwork.update(senority_final)

df = DataFrame(Vietnamwork, columns=['Total Jobs','Thời vụ/Hợp đồng ngắn hạn','Mới tốt nghiệp', 'Senior', 'Cấp quản lý điều hành'], index=[0])
df.rename(columns={3:'Intern', 0:'Junior', 2: 'Senior', 1: 'Manager/Director'}, inplace = True)


# In[61]:


df = df.rename(columns={"Thời vụ/Hợp đồng ngắn hạn": "Intern", "Mới tốt nghiệp": "Junior", 'Cấp quản lý điều hành': 'Manager/Director'})

Vietnamwork_result_sen = df
Vietnamwork_result_sen


# In[ ]:


from datetime import date
Vietnamwork_result_ind.to_csv(f'vietnamwork-ind-{date.today()}.csv')
Vietnamwork_result_sen.to_csv(f'vietnamwork-sen-{date.today()}.csv')


# In[ ]:





# In[ ]:




