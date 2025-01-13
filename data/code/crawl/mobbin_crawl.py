import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def abtest_design_data_crawl():

    data_dict = []

    url = 'https://abtest.design/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_links = []
    # get all links on the page
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('./tests'):
            all_links.append(a['href'])
    
    all_links = list(set(all_links))
    assert len(all_links) == 47 # number can be changed, checked on 2025-01-01

    for link in tqdm(all_links):
        current_data = {}

        # url
        url = f'https://abtest.design{link.strip(".")}'
        current_data['analysis_url'] = url
        print('Url:', url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # title
        current_data['page_title'] = soup.find('div', 'framer-10vjlxc').text.strip()
        print('Title:', current_data['page_title'])

        # company
        current_data['company'] = soup.find('div', 'framer-8oyt90').text.strip()
        print('Company:', current_data['company'])

        # type
        current_data['type'] = soup.find('div', 'framer-1dh5tig').text.strip()
        print('Type:', current_data['type'])

        # image
        current_data['image_url'] = soup.find('div', 'framer-16lvn8g').find('img')['src']
        print('Image:', current_data['image_url'])

        # text
        current_data['text'] = {}
        current_data['text']['description'] = soup.find('div', 'framer-2jib1b').text.strip()
        current_data['text']['results'] = soup.find('div', 'framer-r084lh').text.strip()

        data_dict.append(current_data)
        with open('../../mobbin.json', 'w') as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False)

def abtest_design_image_download():
    with open('../../mobbin.json', 'r') as f:
        data = json.load(f)
    
    for i, d in tqdm(enumerate(data)):
        os.makedirs(f'../../image/mobbin/{i}', exist_ok=True)
        response = requests.get(d['image_url'])
        with open(f'../../image/mobbin/{i}/0.png', 'wb') as f:
            f.write(response.content)

if __name__ == '__main__':
    abtest_design_data_crawl()
    abtest_design_image_download()