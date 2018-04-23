# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import requests
import json
import re
import logging
import time
image_list = []
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
cookie = {"Cookie": "_T_WM=d0d9202272a5911188177e55a0c3628f; SUB=_2A2532fbxDeRhGeNG71EY-C3PyjmIHXVVJZq5rDV6PUJbkdANLRXmkW1NS0d8AFAq_O-D-rJy0NlO-diqf5Wcfgjn; SUHB=0sqBRtVzeNpsSK; SCF=Aq6mM4T8McbCQyTVujPuphjgzwCkNGjARtUu7QO8WSjSk_UKIrH_S5jSUyGfRhggKkKQ7ipfkCEILktoPQa3sbE.; SSOLoginState=1524467361"}
proxies = { "https": "183.159.92.64" ,"http": "183.159.92.64" }
for i in range(1,100):
    url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%83%85%E4%BE%A3%E5%A4%B4%E5%83%8F&page='+str(i)
    response = requests.get(url, headers = head,cookies = cookie)
    soup = BeautifulSoup(response.text,"lxml")
    images_link = soup.find_all('a')
    for image in images_link:
        if image.string:
            if re.findall('组图',image.string.encode('utf-8')):
                img_link_url = image.get('href')
                images_response = requests.get(img_link_url,headers = head,cookies = cookie)
                images_soup = BeautifulSoup(images_response.text.encode('utf-8'),"lxml")
                images = images_soup.find_all('img')
                for img in images:
                    img_url = img.get('src')
                    image_list.append(img_url)
                logging.warning('one complete')
                time.sleep(0.1)



for k,imge in enumerate(image_list):
    response = requests.get(imge,stream = True)
    with open(str(k)+'.jpg', 'wb') as f :
        f.write(response.content)
    time.sleep(0.1)

