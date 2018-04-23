from bs4 import BeautifulSoup
import requests
import json
import re
import sys
import io
image_list = []
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
# url_b = 'http://tieba.baidu.com/p/4984931915?pn=%d'
for i in range(1,7):
    url = 'http://tieba.baidu.com/p/4984931915?pn=%d'%i
    response = requests.get(url, headers = head)
    response.encoding = 'utf-8'
    # print response.text
    soup = BeautifulSoup(response.text.encode('utf-8'),"lxml")
    with open('soup.txt','w') as f:
        f.write(soup.prettify().encode('utf-8'))
    image_blocks = soup.find_all('div',attrs = {'class':'l_post j_l_post l_post_bright '})
    # print(image_blocks)
    for block in image_blocks:
        images = block.find('div',attrs = {'class':'d_post_content j_d_post_content clearfix'}).find_all('img')
        for image in images :
            image_list.append(image.get('src')) 
            # with open('image_list.txt','a') as f:
            #     f.write(image.get('src'))
for k,imge in enumerate(image_list):
    response = requests.get(imge,stream = True)
    with open(str(k)+'.jpg', 'wb') as f :
        f.write(response.content)
