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


#Total Jobs of CareerBuilder
url = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-vi.html"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs = soup.find("div", class_="job-found").find("p").get_text()
total_jobs = to_int(total_jobs[:6])
total_jobs


# In[3]:


#Jobs by Industry
full_ind = []
full_no_of_jobs = []

industries = soup.find_all('ul', class_="filter-list")[1].find_all("li")

for industry in industries:
    ind = industry.find("div").get_text()[2:-1]
    no_of_jobs = industry.find("span").get_text()
    full_ind.append(ind)
    full_no_of_jobs.append(to_int(no_of_jobs))


# In[20]:


#Jobs by Senority
#Jobs Sinh Viên
url_sv = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe1-vi.html"

page = requests.get(url_sv)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_sv = soup.find("div", class_="job-found").find("p").get_text()[0:-9]


#Jobs Tốt nghiệp
url_tn = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe2-vi.html"

page = requests.get(url_tn)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_tn = soup.find("div", class_="job-found").find("p").get_text()[0:-9]


#Jobs executive
url_nv = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe3-vi.html"

page = requests.get(url_nv)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_nv = soup.find("div", class_="job-found").find("p").get_text()[0:-9]


#Jobs Senior
url_cv = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe4-vi.html"

page = requests.get(url_cv)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_cv = soup.find("div", class_="job-found").find("p").get_text()[0:-9]


#Jobs Manager
url_tp = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe5-vi.html"

page = requests.get(url_tp)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_tp = soup.find("div", class_="job-found").find("p").get_text()[0:-9]


#Jobs Director
url_gd = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe11-vi.html"

page = requests.get(url_gd)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_gd = soup.find("div", class_="job-found").find("p").get_text()[0:-9]


#Jobs BoD
url_bdh = "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-fe12-vi.html"

page = requests.get(url_bdh)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

total_jobs_bdh = soup.find("div", class_="job-found").find("p").get_text()[0:-9]

total_jobs_bdh


# In[21]:


#Candidate Number
url_candidate = "https://careerbuilder.vn/vi/resume-search.html"

page = requests.get(url_candidate)
soup = BeautifulSoup(page.text, 'html.parser')
soup.prettify()

full_can_ind_dict = {}
result_dict = {}

can_inds = soup.find('div', class_='HeaderLine CateEmp').find_all('li')

for inds in can_inds:
    can_ind = inds.find('a').get_text()
    no_of_can_ind = inds.find('span').get_text()
    no_of_can_ind = no_of_can_ind[1:-1]
    full_can_ind_dict[f'{can_ind}']=to_int(no_of_can_ind)

df1 = pd.DataFrame(full_can_ind_dict.items(), columns = ['Industry','Number of Candidates'])


# In[22]:


#Create DataFrame
careerbuilder_result_ind_dict = {
        'Industry': full_ind,
        'No. of Jobs': full_no_of_jobs}

careerbuilder_result_sen_dict = {
        'Total Jobs': to_int(total_jobs),
        'Intern': to_int(total_jobs_sv),
        'Junior': to_int(total_jobs_tn) + to_int(total_jobs_nv),
        'Senior': to_int(total_jobs_cv),
        'Manager/Director': to_int(total_jobs_tp) + to_int(total_jobs_gd) + to_int(total_jobs_bdh)
                                                           }

careerbuilder_result_ind = DataFrame(careerbuilder_result_ind_dict, columns=["Industry", "No. of Jobs" ])
careerbuilder_result_sen = DataFrame(careerbuilder_result_sen_dict, columns=["Total Jobs", "Intern","Junior","Senior","Manager/Director"], index=[0])


# In[23]:


careerbuilder_result_ind


# In[24]:


careerbuilder_result_sen


# In[23]:


from datetime import date
careerbuilder_result_ind.to_csv(f'careerbuilder-ind-{date.today()}.csv')
careerbuilder_result_sen.to_csv(f'careerbuilder-sen-{date.today()}.csv')


# In[ ]:




