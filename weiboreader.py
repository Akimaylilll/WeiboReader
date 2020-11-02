# -*- coding: utf-8 -*-
import requests
import re
import time
import datetime
import random
import json
import sys
import urllib
from bs4 import BeautifulSoup
import tkinter
import tkinter.messagebox
# ------------------------
id = "3668829440"
url = 'https://weibo.com/u/' + id
#headers

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'cache-control': 'max-age=0',
        'Connection':'Keep-Alive',
        'Referer': url,
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/73.0.3683.86Safari/537.36'}
def getTime(t):
        startTime = datetime.datetime.strptime(t,"%Y-%m-%d %H:%M")
        now = datetime.datetime.now()
        day=(now-startTime).days
        return day
def getUrl(url2,cookies):
        data = requests.get(url=url2,headers=headers,cookies=cookies)
        #data_text = data.text
        #print(data_text)
        time.sleep(3)

        flag = 0
        html = re.findall(r'<script>FM.view(.*)</script>',data.text)     #将script标签内容提取出
        #print(html)
        if(len(html) == 0):                
                return 2
        global data_jason
        for i in html:
                if re.search(r'WB_detail',i) != None: #取出有文字的段落   已经有观察出 含有微博文字的特徵
                        i = i.strip('(').strip(')') #字串去掉括号
                        data_jason = json.loads(i)  #将字串载入成字典档
        if 'data_jason' in locals().keys():                
                return 2

        soup = BeautifulSoup(data_jason['html'],'lxml')    #字典档当中只提取html对应的代码
        tags = soup.find_all('div',attrs={"class":"WB_from S_txt2"})
        if(len(tags) == 0):                
                return 2
        num = 0
        for tag in tags:                
                if(tag.parent.attrs['class']==['WB_detail']):
                        if(getTime(tag.a.get('title'))<31):
                                print('----正在阅读-----')
                                response1 = requests.get(url= url + tag.a.get('href'),headers=headers,cookies=cookies)
                                #response1 = urllib.request.urlopen(r)
                                time.sleep(20)
                                #response1.read()
                                num = num + 1
                                print(num)  #去掉空格 第一个分号内有一个空格
                                print(tag.a.get('title'))  #去掉空格 第一个分号内有一个空格
                                time.sleep(random.randint(8,15))
                        else : 
                                if(tags.index(tag) != 0):
                                        flag = 1
                                        break
        if(flag == 1):
                return 1
        return 0

def insert_insert(text1):
        cookie=text1.get('0.0','end') #获取文本框内容
        cookie=cookie[:-1]
        if(len(cookie) == 0): 
                tkinter.messagebox.showwarning('警告','Cookie is None!')
                return
        cookies = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}   #cookies处理格式
        ff = 0
        for page in range(0,15):
                print('----正在阅读-----')
                url2 = url + '?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='+str(page+1)+'#feedtop'
                ff=getUrl(url2,cookies)
                if(ff == 1 or ff == 2): break
                print('---bar---')
                for bar in range(0,2):
                        url3 = url+'?topnav=1&topnav=1&wvr=6&wvr=6&topsug=1&topsug=1&is_all=1&domain=100505&pagebar='+str(bar)+'&pl_name=Pl_Official_MyProfileFeed__20&id=100505'+str(id)+'&script_uri=/u/'+str(id)+'&feed_type=0&page='+str(page+1)+'&pre_page='+str(page+1)+'&domain_op=100505'
                        ff=getUrl(url3,cookies)
                        if(ff == 1 or ff == 2): break
                if(ff == 1 or ff == 2): break
        if(ff == 1): tkinter.messagebox.showinfo('提示','Run Successfully!')
        if(ff == 2): tkinter.messagebox.showwarning('警告','Run Unsuccessfully!')
        return

root = tkinter.Tk()
text1 = tkinter.Text(root)
text1.pack()
button1 = tkinter.Button(root, text="Run", command=lambda : insert_insert(text1))
button1.pack()
# 进入消息循环
root.mainloop()
