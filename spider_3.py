from bs4 import BeautifulSoup
import requests
import json
import re
cookie = {"Cookie": "_T_WM=be7eb781a65b0ca8c2badd99ec45a4e6; H5_INDEX=3; H5_INDEX_TITLE=BigRaingod_Michael; ALF=1524304849; SCF=At4cZ9HM5H3ddSWXBbv_Opb6TR2F9kgs3ZzF3gZmiMKNFh1ZY5njj16PR9zFSJutRxRxagWedxwGcTc-FpGQKKA.; SUB=_2A253tw_1DeRhGeNG71EY-C3PyjmIHXVVW5G9rDV6PUJbktANLRbBkW1NS0d8AEHbQBtiTBm3AKLTyTff285eTjKV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whq4dxVNk-Newo6iDe4zl5n5JpX5K-hUgL.Fo-RShe41he0eK-2dJLoIpiFIgUCqgLV9cv.PXfDqcyy9g7t; SUHB=0V5lBU_7bPPWM_; SSOLoginState=1521713062"}
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
content = {}
soup_list = list()
urllist = list()
class People(object):
    def __init__(self,name,in_num,out_num,wb_num,sex,location):
        self.name = name
        self.in_num = in_num
        self.out_num = out_num
        self.wb_num = wb_num
        self.sex = sex
        self.location =location
    def tostring(self):
        string = ""
        string +='姓名：'+self.name +'      '
        string +='粉丝：'+self.in_num +'      '
        string +='关注：'+self.out_num +'      '
        string +='微博：'+self.wb_num +'      '
        string +='性别：'+self.sex +'      '
        string +='地区: '+self.location +'      '
        return string

    
def Getpages(url):
    response = requests.get(url, headers = head,cookies = cookie)
    soup = BeautifulSoup(response.text,"lxml")
    result = soup.find("input",attrs={'name':'mp'})
    page = result.attrs['value']
    return page

def GetContent(url):
    response = requests.get(url, headers = head,cookies = cookie)
    soup = BeautifulSoup(response.text,"lxml")
    return soup

page = Getpages('https://weibo.cn/2938851024/follow')
# 获取关注的url
for i in range(1,int(page)+1):
        soup = GetContent('https://weibo.cn/2938851024/follow?page=%d'%i)
        # content['https://weibo.cn/u/2938851024?filter=0&page=%d'%i] = soup.prettify()
        soup_list.append(soup)
        with open("spider3.txt",'a') as f:
            f.write(soup.prettify())

for soup in soup_list:
    tables = soup.find_all('table')
    for table in tables:
        href = table.find('a').get('href')
        urllist.append(href)
        with open("urlList.txt",'a') as f:
            f.write(href+'\n')
#========================================
for url in urllist:
    soup = GetContent(url)
    div = soup.find('div',attrs = {'class':'tip2'})
    in_num = re.findall("[0-9]+",div.find_all('a')[0].string)[0]
    out_num = re.findall("[0-9]+",div.find_all('a')[1].string)[0]
    wb_num = re.findall("[0-9]+",div.find_all('span')[0].string)[0]
    # 找到资料的url
    ziliao_div = soup.find('div',attrs = {'class':'ut'})
    temps = ziliao_div.find_all('a')
    for a in temps:
        if(a.string == "资料"):
            ziliao_url = "https://weibo.cn/"+a.get('href')
            break
    ziliao_soup = GetContent(ziliao_url)
    name = re.findall("昵称:.*",ziliao_soup.prettify())[0][2:]
    sex = re.findall("性别:.",ziliao_soup.prettify())[0][3]
    location = re.findall("地区:.*",ziliao_soup.prettify())[0][3:]
    newfans = People(name = name,in_num = in_num, out_num = out_num, wb_num = wb_num, sex = sex, location = location)
    with open("spider3_2.txt","a") as f:
        f.write(newfans.tostring()+"\n")
    



