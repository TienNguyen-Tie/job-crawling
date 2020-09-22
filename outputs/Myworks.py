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


# In[12]:


#Total Jobs of Vietlam24h
url = "https://mywork.com.vn/tuyen-dung"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_r = soup.find("div", id="idJobNew").find("p").get_text()

total_jobs = total_jobs_r.split()[2]
total_jobs = to_int(total_jobs)
print(total_jobs)


# In[15]:


#Jobs by Senority
url_list = ('https://mywork.com.vn/tuyen-dung?ranks=1',
           'https://mywork.com.vn/tuyen-dung?ranks=2',
           'https://mywork.com.vn/tuyen-dung?ranks=3',
           'https://mywork.com.vn/tuyen-dung?ranks=4',
           'https://mywork.com.vn/tuyen-dung?ranks=5',
           'https://mywork.com.vn/tuyen-dung?ranks=6',
           'https://mywork.com.vn/tuyen-dung?ranks=7',
           'https://mywork.com.vn/tuyen-dung?ranks=8')

jobs_senority = ['Intern', 'Nhân Viên', 'Trưởng Nhóm', 'Trưởng Phòng', 'Phó Giám Đốc', 'Giám Đốc', 'Tổng Giám Đốc Điều Hành', 'Khác']
jobs_senority_no = []

for url_se in url_list:
    page = requests.get(url_se)
    
    soup = BeautifulSoup(page.text, 'html.parser')
    soup.prettify()

    total_jobs_senority_r = soup.find("div", id="idJobNew").find("p").get_text()

    total_jobs_senority = total_jobs_senority_r.split()[2]
    
    total_jobs_senority = to_int(total_jobs_senority)
    jobs_senority_no.append(total_jobs_senority)
    
jobs_senority_dict = dict(zip(jobs_senority, jobs_senority_no))


# In[22]:


Myworks = pd.DataFrame.from_dict(jobs_senority_dict, orient='index')
Myworks = Myworks.transpose()

Myworks.insert(0, 'Total Jobs', total_jobs)

Myworks


# In[23]:


sum_exe = Myworks['Nhân Viên'] + Myworks['Khác']
sum_lead = Myworks['Trưởng Phòng'] + Myworks['Trưởng Nhóm']
sum_mana = Myworks['Phó Giám Đốc'] + Myworks['Giám Đốc'] + Myworks['Tổng Giám Đốc Điều Hành']

Myworks["Junior"] = sum_exe
Myworks["Senior"] = sum_lead
Myworks["Manager/Director"] = sum_mana

Myworks = Myworks.drop(['Nhân Viên','Giám Đốc', 'Trưởng Nhóm', 'Trưởng Phòng', 'Phó Giám Đốc', 'Tổng Giám Đốc Điều Hành', 'Khác'],axis=1)
Myworks_results_sen = Myworks
Myworks_results_sen


# In[ ]:


# Jobs by industries
# url = "https://mywork.com.vn/tuyen-dung"
# page = requests.get(url)

# soup = BeautifulSoup(page.text, 'html.parser')
# soup.prettify()


# industries_url = []
# full_ind_dict = {}
# full_ind = []
# industries_jobs_no = []

# print(soup)

# industries_url_raw = soup.find('div', class_='pd-15').find_all('a', href=True)
# print(industries_url_raw)

# industry_name_r = soup.find('div', class_='box_white mt_16 bold').find_all('span', class_='text_pink')[1].get_text()
# full_ind.append(industry_name_r)

# def unique(list1): 
#     # insert the list to the set 
#     list_set = set(list1) 
#     # convert the set to the list 
#     unique_list = (list(list_set)) 
#     return unique_list

# industries_url_raw=unique(industries_url_raw)

# for industry in industries_url_raw:
#     href = industry.get('href')
#     industries_url.append(href)

# for industry in industries_url:
#     page = requests.get(industry)

#     soup = BeautifulSoup(page.text, 'html.parser')

#     industry_no_r = soup.find('div', class_='box_white mt_16 bold').get_text()
#     industry_name_r = soup.find('div', class_='box_white mt_16 bold').find_all('span', class_='text_pink')[1].get_text()
#     full_ind.append(industry_name_r)
#     for s in industry_no_r.split(): 
#         if s.isdigit():
#             industries_jobs_no = int(s)

#     full_ind_dict[f'{industry_name_r}'] = to_int(industries_jobs_no)   
# result.append(full_ind_dict)




# In[ ]:


from datetime import date
Myworks_results_sen.to_csv(f'mywork-sen-{date.today()}.csv')

