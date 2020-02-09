from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

driver = webdriver.Chrome()
url = 'https://www.indeed.co.in/'
q = input('please input the query: \n')#.replace(' ','+')
l = input('Location: \n')

# Codes to be executed:......................................................................
code =\
'''
title = job.find_element_by_class_name('title')
job_title = title.text

location = job.find_element_by_class_name('location').text

try:
    reviews = int(job.find_element_by_class_name('slNoUnderline').text.rstrip('reviews').rstrip().replace(',','')) 
except:
    reviews = 0
    
company = job.find_element_by_class_name('company').text

try:
    ratings = float(job.find_element_by_class_name('ratings').get_attribute('aria-label').split()[0] ) 
except:
    ratings = 0.0

summary = job.find_element_by_class_name('summary').text.strip()
job_link = title.find_element_by_tag_name('a').get_attribute('href')
try:
    date = job.find_element_by_class_name('date').text
except:
    date = ''

try:
    sponsoredby = job.find_element_by_class_name('sponsoredGray').find_element_by_tag_name('b').text
except:
    sponsoredby = None

jobs_dict[ID] = (job_title, location, company, reviews, ratings, date, sponsoredby, summary, job_link)
'''
page_code =\
'''
jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
for job in jobs:
    ID += 1
    exec(code)
print('Page {} completed'.format(driver.current_url))
'''

driver.get(url)
driver.find_element_by_name('q').send_keys(Keys.CONTROL + 'a')
driver.find_element_by_name('q').send_keys(q)
driver.find_element_by_name('l').send_keys(Keys.CONTROL + 'a')
driver.find_element_by_name('l').send_keys(l)
driver.find_element_by_name('l').send_keys(Keys.ENTER)
ID = 0
jobs_dict = {}


exec(page_code)

while True:
    if driver.find_element_by_class_name('pagination').find_elements_by_tag_name('a')[-1].text == 'Next »':
        next_url = driver.find_element_by_class_name('pagination').find_elements_by_tag_name('a')[-1].get_attribute('href')
        driver.get(next_url)
        exec(page_code)
        #print(driver.current_url)
    else:
        break

df = pd.DataFrame.from_dict(jobs_dict, orient='index', columns=['job_title', 'location', 'company', 'reviews',
                                                           'ratings', 'date', 'sponsoredby', 'summary', 'job_link'])
df.head()

df.to_csv('{}.csv'.format(input('Filesname')), index=False)

driver.close()


print(100*'*)
print('Successful Scraping : {} Jobs found'.format(df.shape[0]))
print(100*'=')

print(df.head())

