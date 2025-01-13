import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def goodui_leaks_data_crawl():

    data_dict = []
    
    ### get all page links from the leaks page
    all_links = []
    sublinks_suffix = ['/', '/page2/', '/page3/', '/page4/', '/page5/', '/page6/']
    pages = [f'/leaks/{suffix}' for suffix in sublinks_suffix] + [f'/leaks{suffix}' for suffix in sublinks_suffix]

    for sublink_suffix in sublinks_suffix:
        url = f'https://goodui.org/leaks{sublink_suffix}'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # get all links on the page
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('/leaks/') and a['href'] not in pages:
                all_links.append(a['href'])
    
    all_links = list(set(all_links))
    assert len(all_links) == 111 # number can be changed, checked on 2025-01-01

    ### get all data from each link
    for link in tqdm(all_links):
        current_data = {}

        # url
        url = f'https://goodui.org{link}'
        # url = 'https://goodui.org/leaks/airbnb-retests-the-infamous-infinite-scroll/'
        current_data['analysis_url'] = url
        print('Url:', url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # title
        current_data['page_title'] = soup.find('h1', 'leak-title').text.strip()
        print('Title:', current_data['page_title'])

        # company
        current_data['company'] = {}
        current_data['company']['name'] = re.search(r'from\s+(.*?)\s*\|', soup.find('span', 'leak-url').text).group(1)
        print('Company:', current_data['company']['name'])

        # image
        current_data['image'] = {}
        current_data['image']['url_list'] = []
        img_tag = soup.find_all('div', 'leak-variant')
        print('Number of variants:', len(img_tag))

        implemented = False
        for variant in img_tag:
            variant_tag = variant.find('span', 'leak-variant-title').text.strip().replace(' ', '')
            if 'IMPLEMENTED' in variant_tag:
                implemented = True
                break

        for variant in img_tag:
            variant_img = 'https://goodui.org' + variant.find('img').get('src')
            variant_tag = variant.find('span', 'leak-variant-title').text.strip().replace(' ', '')
            if implemented:
                if 'IMPLEMENTED' in variant_tag:
                    variant_ox = 'O'
                else:
                    variant_ox = 'X'
            else:
                if 'REJECTED' in variant_tag:
                    variant_ox = 'X'
                else:
                    variant_ox = 'O'
            
            current_data['image']['url_list'].append({'tag': variant_tag, 'ox': variant_ox, 'url': variant_img})

        # description
        current_data['description'] = {}
        current_data['description']['main'] = soup.find('div', 'leak-body').text.strip()
        current_data['description']['ui_change'] = []
        ol_tag = soup.find('ol', 'numbered')
        for li_tag in ol_tag.find_all('li'):
            text_li = li_tag.find('span', 'numtitle').text.strip() + '\n' + li_tag.find('div', 'general-text').text.strip()
            current_data['description']['ui_change'].append(text_li)
            li_tag.extract()

        current_data['description']['sub'] = []
        all_text_tag = soup.find_all('div', 'general-text')
        for text_tag in all_text_tag:
            if text_tag.text.strip() != '':
                current_data['description']['sub'].append(text_tag.text.strip())
        
        # external comment blank
        current_data['external_comment'] = ['']
        
        
        # save to json
        data_dict.append(current_data)
        with open('../../goodui_leaks.json', 'w') as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False)
    
def goodui_image_download():
    with open('../../goodui_leaks.json', 'r') as f:
        data = json.load(f)
    
    for i, d in tqdm(enumerate(data)):
        os.makedirs(f'../../image/goodui/{i}', exist_ok=True)
        for j, img_dict in enumerate(d['image']['url_list']):
            response = requests.get(img_dict['url'])
            with open(f'../../image/goodui/{i}/{j}.png', 'wb') as f:
                f.write(response.content)

if __name__ == "__main__":
    goodui_leaks_data_crawl()
    goodui_image_download()