# encoding:utf-8

from time import time
from itertools import chain

from download import setup_download_dir, get_links, download_link

def download_all_imgs(links):
    ts = time()
    download_dir = setup_download_dir('single_imgs')
    for link in links:
        download_link(download_dir, link)
    print('一共下载了 {} 张图片'.format(len(links)))
    print('Took {}s'.format(time() - ts))



