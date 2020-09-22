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


# In[2]:


url = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?hdn_tu_khoa=&tk_select_gate=&hdn_nganh_nghe_cap1=&hdn_dia_diem="
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_r = soup.find("span", class_="text-tim-nhat uppercase").get_text()
total_jobs = total_jobs_r[-5:-1]
total_jobs


# In[3]:


Vietlam24h = {
             'Total Jobs': to_int(total_jobs),
             }

master_df = DataFrame()


# In[4]:


url_ind_list = ["https://vieclam24h.vn/mien-nam/viec-lam-lao-dong-pho-thong/viec-lam-theo-nganh-nghe",
               'https://vieclam24h.vn/mien-nam/viec-lam-quan-ly/viec-lam-theo-nganh-nghe',
               'https://vieclam24h.vn/mien-nam/viec-lam-chuyen-mon/viec-lam-theo-nganh-nghe',
               'https://vieclam24h.vn/mien-nam/viec-lam-ban-thoi-gian/viec-lam-theo-nganh-nghe']
result = []
for url_ind in url_ind_list:
    page = requests.get(url_ind)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup.prettify()

    senority = soup.find('span', class_='txt-ghi mb10 font13 italic').get_text()
    senority = senority[16:]

    industries_url = []
    full_ind_dict = {}
    full_ind = []
    industries_jobs_no = []

    industries_url_raw = soup.find('div', class_='pl_8 pr_8').find_all('a', href=True)
    def unique(list1): 

        # insert the list to the set 
        list_set = set(list1) 
        # convert the set to the list 
        unique_list = (list(list_set)) 
        return unique_list

    industries_url_raw=unique(industries_url_raw)

    for industry in industries_url_raw:
        href = industry.get('href')
        industries_url.append(href)

    for industry in industries_url:
        page = requests.get(industry)

        soup = BeautifulSoup(page.text, 'html.parser')

        industry_no_r = soup.find('div', class_='box_white mt_16 bold').get_text()
        industry_name_r = soup.find('div', class_='box_white mt_16 bold').find_all('span', class_='text_pink')[1].get_text()
        full_ind.append(industry_name_r)
        for s in industry_no_r.split(): 
            if s.isdigit():
                industries_jobs_no = int(s)

        full_ind_dict[f'{industry_name_r}'] = to_int(industries_jobs_no)   
    result.append(full_ind_dict)


# In[5]:


final = {}

def checkNone(x, key):
    if key not in x:
        return 0
    else:
        return x[key]

for key in result[3].keys():
    total = checkNone(result[0],key) + checkNone(result[1],key) + checkNone(result[2],key) + checkNone(result[3],key)
    final[key] = total

total_jobs = sum(final.values())


# In[6]:


Vietlam24h = {
             'Total Jobs': total_jobs,
             'Industry': full_ind,
             }

df = DataFrame(Vietlam24h, columns=['Total Jobs', 'Industry'])


# In[7]:


senior_pd_r = pd.DataFrame.from_dict(result)
no_of_senior = senior_pd_r.sum(axis=1, skipna=True)
no_of_senior = pd.DataFrame(no_of_senior)

dictionary = no_of_senior.to_dict()
d = dictionary.get(0)
Vietlam24h.update(d)

df = DataFrame(Vietlam24h, columns=['Total Jobs',3,0,2,1],index=[0])
df.rename(columns={3:'Intern', 0:'Junior', 2: 'Senior', 1: 'Manager/Director'}, inplace = True)
Vietlam24h_result_sen = df
Vietlam24h_result_sen


# In[8]:


senior_pd = senior_pd_r.transpose()

data = senior_pd.sum(axis = 1, skipna=True)


# In[9]:


data = data.to_frame()


# In[10]:


data = data.reset_index()
data.rename(columns={'index':'Industry', 0:'No. of Jobs'}, inplace = True)
Vietlam24h_result_ind = data
Vietlam24h_result_ind = Vietlam24h_result_ind.sort_values(by=['No. of Jobs'], ascending=False)
Vietlam24h_result_ind


# In[ ]:


from datetime import date
Vietlam24h_result_ind.to_csv(f'vietlam24h-ind-{date.today()}.csv')
Vietlam24h_result_sen.to_csv(f'vietlam24h-sen-{date.today()}.csv')


# In[ ]:




