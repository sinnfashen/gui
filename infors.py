# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:28:22 2017

@author: Administrator
"""
import time
import os
import urllib.parse as parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests


def get_titlehtml(title):
    # search newspaper title and get html
    url = 'http://kns.cnki.net'
    chmdriver = os.path.join(os.getcwd(), 'phantomjs.exe')
    driver = webdriver.PhantomJS(chmdriver)
    driver.get(url)
    elem = driver.find_element_by_name("txt_1_value1")
    elem.send_keys(title)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    driver.switch_to.frame('iframeResult')
    html = driver.page_source
    # parse html
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_newspaper(soup):
    # get newspaper from html
    newslist = soup.find('tr', attrs={'bgcolor':'#ffffff'})
    tdlist = newslist.find_all('td')
    newspaper = tdlist[3].text.replace('\n','')
    return newspaper
    
def get_banhao(soup):
    # get article_url from html
    a = 'http://kns.cnki.net/KCMS/detail/detail.aspx?'
    newsurl = soup.find('a', attrs={'class':'fz14'})['href']
    b = parse.urlparse(newsurl).query
    paperurl = a+b
    # get banmian from new url
    html_ban = requests.get(paperurl).content
    soup = BeautifulSoup(html_ban ,'html.parser')
    bh = soup.find('div', attrs={'class':"wxBaseinfo"})
    banlist = bh.find_all('p')
    banhao = None
    for i in banlist:
        if "版号" in i.text:
            banhao = i.text
            break
    return banhao
    
    









