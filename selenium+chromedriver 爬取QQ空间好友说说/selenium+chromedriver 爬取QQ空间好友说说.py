#!/usr/bin/env python
# coding: utf-8

# In[11]:


#导入库
from selenium import webdriver
import time
import csv
import pymongo

#连接数据库
client=pymongo.MongoClient('localhost',27017)
mydb=client['mydb']
qq_shuo=mydb['qq_shuo']

#选择浏览器
driver=webdriver.Chrome()
driver.maximize_window()

#定义获取信息的函数
def get_info(qq):
    driver.get('https://user.qzone.qq.com/{}/311'.format(qq))
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_id('login_div')
        a=True
    except:
        a=False
    if a==True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys('2025330976')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('lujuntong520')
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b=True
    except:
        b=False
        
    if b==True:
        driver.switch_to.frame('app_canvas_frame')
        contents=driver.find_elements_by_css_selector('.content')
        times=driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for content,tim in zip(contents,times):
            data={
                'time':tim.text,
                'content':content.text
            }
            qq_shuo.insert_one(data)
if __name__=='__main__':
    qq_lists=[]
    fp=open('F:\qq\QQmail.csv')
    reader=csv.DictReader(fp)
    for row in reader:
        qq_lists.append(row['电子邮件'].split('@')[0])
    fp.close()
    
    for item in qq_lists:
        get_info(item)


# In[ ]:




