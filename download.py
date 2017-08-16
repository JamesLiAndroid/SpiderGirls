import json
import os
import requests

from itertools import chain
from pathlib import Path

from bs4 import BeautifulSoup


def get_links(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return [img.attrs.get('data-src') for img in
            soup.find_all('div', class_='img-wrap')
            if img.attrs.get('data-src') is not None]


def download_link(directory, link):
    img_name = '{}'.format(os.path.basename(link))
    download_path = directory / img_name
    print("before:", link)
    try:
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        r = requests.get(link, headers=headers)
        with download_path.open('wb') as fd:
            # print(r.content)
            fd.write(r.content)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e
    # except (requests.ConnectionError, IndexError, UnicodeEncodeError, requests.exceptions.TimeoutError) as e:
    #    print(e.args)
    except requests.HTTPError as f:
        print('The server couldn\'t fulfill the request.', f.args)
#    with download_path.open('wb') as fd:
#        fd.write(r.content)


def setup_download_dir(directory):
    download_dir = Path(directory)
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir
