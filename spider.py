# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2017-08-15 11:00:39
# @Last Modified by:   Marte
# @Last Modified time: 2017-08-15 11:52:35

import os
import sys
import urllib2
import requests
import re
from lxml import etree
from download_multi_thread import download_file
from download_single import download_all_imgs
from download_multi_thread import download_threads

def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))

# 获取分页链接
def Real_Page_Urls(myPage):
    '''Regex'''
    real_page_urls = []
    mypage_Info = re.findall(r'<div class=\"NewPages\">.*?<\/div>', myPage, re.S)
    print('div', mypage_Info[0], len(mypage_Info), type(mypage_Info))
    page_ul_content = re.findall(r'<a [^>]*>.*?<\/a>', str(mypage_Info[0]), re.S)
    print('a list', page_ul_content, len(page_ul_content))
    for url_temp in page_ul_content:
        real_page_url = re.search(r'[http]+://[^\s|"]*', url_temp, re.S)
        # print(real_page_url.group(), '\n')
        real_page_urls.append(real_page_url.group())
    print('real_page_urls', real_page_urls[0], len(real_page_urls))

    #real_page_urls = re.findall(r'[http]+://[^\s]*', mypage_Info[0], re.S)
    #print("页面链接集合为", real_page_urls, len(real_page_urls))
    return real_page_urls

# 获取当前页面图片链接
def Now_Page_Pic_Urls(now_page):
    '''Regex(slowly) or Xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(now_page)
    # xml解析规则，获取图片链接
#    new_urls = dom.xpath("//div[@class='MeinvTuPianBox']/li[@class='wenshen']/a/img[@class='lazy kk']/@src")
    new_urls = dom.xpath('//div[@class="MeinvTuPianBox"]/ul/li[@class="wenshen"]/a/img/@src')
    print("dddd : ", new_urls[0])
    # print("new_urls:::", type(new_urls), etree.tostring(new_urls[0]))

    #new_urls = dom.xpath('//tr/td/a/@href')
    #assert(len(new_items) == len(new_urls))
    return new_urls

# 保存图片
def Save_File(d, filename, img_url):
    download_file(img_url, filename)

def Spider(url):
    i = 0
    print("downloading ", url)
    # 页面内容抓取
    myPage = requests.get(url).content.decode("utf-8")
    # myPage = urllib2.urlopen(url).read().decode("gbk")

    # print(myPage)

    # 获取分页内容
    myPageUrls = Real_Page_Urls(myPage)
    save_path = u"PageUrls"
    # 设置链接保存文件名称，并保存
    filename = str(i)+"_"+u"mz"
    StringListSave(save_path, filename, myPageUrls)

    # 遍历页面上的图片链接，并下载
    i += 1
    j = 1
    for url in myPageUrls:
        print("downloading page:", url, ":::current_page:", i)
        new_page = requests.get(url).content.decode("utf-8")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        picUrls = Now_Page_Pic_Urls(new_page)
        # 下载全部图片
        #download_all_imgs(picUrls)
        download_threads(picUrls)


        # 保存分页链接
#        pic_url_page_name = "page_"+str(j)+"_"+u"mdzz"
#        StringListSave(save_path, pic_url_page_name, picUrls)
        # 遍历下载
#        for img_url in picUrls:
#            filename = "mdzz_"+str(j)
            # 图片下载保存
#            Save_File('./imgs', filename, img_url)
#            j += 1
        # StringListSave(save_path, filename, newPageResults)
        i += 1


if __name__ == '__main__':
    print("start")
    start_url = "http://www.iaweg.com/tupian/g1votskkno"
    Spider(start_url)
    print("end")
