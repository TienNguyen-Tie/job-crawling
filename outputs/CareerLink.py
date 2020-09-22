#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from pandas import DataFrame

def to_int(x):
    if type(x) is int:
        return x
    return int(x.replace(",","").replace(".",""))


# In[3]:


url = "https://www.careerlink.vn/vieclam/list?keyword_use=A"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

total_jobs_r = soup.find("div", class_="col-md-7").get_text()

total_jobs = total_jobs_r.split()[2]
total_jobs = to_int(total_jobs)
total_jobs


# In[18]:


url = "https://www.careerlink.vn/tim-viec-lam-nhanh"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()
full_job_inds_dict = {}
full_ind = []
job_inds = soup.find('div', class_='masonry-container').find_all('li')
for ind in job_inds:
    job_ind = ind.find('a').get_text()
    full_ind.append(job_ind)
    job_ind_no = ind.find('span').get_text()
    job_ind_no = to_int(job_ind_no[1:-1])
    full_job_inds_dict[f'{job_ind}'] = job_ind_no
careerlink_result_ind = pd.DataFrame(full_job_inds_dict.items(), columns = ['Industry','No. of Jobs'])
careerlink_result_ind = careerlink_result_ind.sort_values(by=['No. of Jobs'], ascending=False)
careerlink_result_ind


# In[19]:


#cut last 5 rows of the dataframe and transpose them
#create new dataframe
#merge

url_list = ['https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=I',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=N',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=L',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=T',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=P',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=M',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=D',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=S',
            'https://www.careerlink.vn/vieclam/tim-kiem-viec-lam?keyword_use=A&career_levels=E'
           ]

senority_list = ['Intern', 'Mới đi làm', 'Nhân viên', 'Kỹ thuật viên', 'Trưởng nhóm', 'Quản lý', 'Giám đốc', 'Quản lí cấp cao', 'Điều hành cấp cao']
senority_no = []
senority_dict = {}

for url in url_list:
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    senority_no_r = soup.find("div", class_="col-md-7").get_text()
    senority_no.append(to_int(senority_no_r.split()[2]))
    
senority_dict = dict(zip(senority_list, senority_no))
senority_dict
    


# In[20]:


Careerlink = {'Total Jobs': total_jobs,
              'Industry': full_ind}

Careerlink.update(senority_dict)

df = DataFrame(Careerlink, columns=['Total Jobs', 'Intern', 'Mới đi làm', 'Nhân viên', 'Kỹ thuật viên', 
                                    'Trưởng nhóm', 'Quản lý', 'Giám đốc', 'Quản lí cấp cao', 'Điều hành cấp cao', 
                                    'Industry'])

Careerlink_result = df.merge(careerlink_result_ind, on='Industry')
Careerlink_result


# In[21]:


sum_column_1 = Careerlink_result['Mới đi làm'] + Careerlink_result['Nhân viên'] + Careerlink_result['Kỹ thuật viên']
sum_column_2 = Careerlink_result['Trưởng nhóm'] + Careerlink_result['Quản lý']
sum_column_3 = Careerlink_result['Giám đốc'] + Careerlink_result['Quản lí cấp cao'] + Careerlink_result['Điều hành cấp cao']

Careerlink_result['Junior'] = sum_column_1
Careerlink_result['Senior'] = sum_column_2
Careerlink_result['Manager/Director'] = sum_column_3


# In[22]:


Careerlink_result = Careerlink_result.drop(['Mới đi làm','Nhân viên','Kỹ thuật viên','Trưởng nhóm','Quản lý',
                                            'Giám đốc','Quản lí cấp cao', 'Điều hành cấp cao',"Industry","No. of Jobs" ],axis=1)

Careerlink_result = Careerlink_result.reindex(columns=['Total Jobs','Intern','Junior','Senior',
                                                       'Manager/Director'])


# In[23]:


careerlink_result_sen = Careerlink_result.loc[[0]]
careerlink_result_sen


# In[ ]:


from datetime import date
careerlink_result_ind.to_csv(f'careerlink-ind-{date.today()}.csv')
careerlink_result_sen.to_csv(f'careerlink-sen-{date.today()}.csv')


# In[ ]:




