# -*- coding=utf-8 -*-
# 在python3下测试
import os
import sys
import requests
import threading
from threading import Thread
import datetime
from Queue import Queue

import time
from download import setup_download_dir, get_links, download_link

# 传入的命令行参数，要下载文件的url
#url = sys.argv[1]

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            if item is None:
                break

            directory, link = item
            download_link(directory, link)
            self.queue.task_done()

def download_threads(links):
    download_dir = setup_download_dir('thread_imgs')
    queue = Queue()

    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the
        # workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    for link in links:
        print(u"添加到队列：", link, u"。。。存储路径：", download_dir)
        queue.put((download_dir, link))

    # Causes the main thread to wait for the queue to finish processing all
    # the tasks
    queue.join()
    print(u'一共下载了 {} 张图片'.format(len(links)))
    # print(u'Took {}s'.format(time() - ts))


def Handler(start, end, url, filename):

    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url, headers=headers, stream=True)

    # 写入文件对应位置
    with open(filename, "r+b") as fp:
        fp.seek(start)
        var = fp.tell()
        # print("position: ", var)
        fp.write(r.content)


def download_file(url, filename, num_thread = 10):

    r = requests.head(url)
    print('url:', url, str(r))
    try:
        file_name = url.split('/')[-1]
        file_size = int(r.headers['content-length'])   # Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
        print('...', file_name, file_size, '....')
    except:
        print("检查URL，或不支持对线程下载")
        return

    #  创建一个和要下载文件一样大小的文件
    save_path = "./imgs"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".jpg"

    fp = open(path, "wb")
    fp.truncate(file_size)
    fp.close()

    # 启动多线程写文件
    part = file_size // num_thread  # 如果不能整除，最后一块应该多几个字节
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1:   # 最后一块
            end = file_size
        else:
            end = start + part

        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': path})
        t.setDaemon(True)
        t.start()

    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % path)

#if __name__ == '__main__':
#    start = datetime.datetime.now().replace(microsecond=0)
#    download_file(url)
#    end = datetime.datetime.now().replace(microsecond=0)
#    print(u"用时: ", str(end-start))
#    print(str(end-start))
