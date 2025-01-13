import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def vwo_success_stories_data_crawl(reuse_links=False):

    ### get all page links from the leaks page
    data_dict = []

    url = 'https://vwo.com/success-stories/'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    if reuse_links:
        with open('vwo_links.txt', 'r') as f:
            all_links = f.read().split('\n')
    else:
        driver.get(url)
        time.sleep(3)

        print('clicking button')
        while True:
            try:
                element = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/div[2]/div[2]/button')
                element.click()
                time.sleep(3)
            except:
                break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('https://vwo.com/success-stories/') and link['href'] not in ['https://vwo.com/success-stories/','https://vwo.com/success-stories/#locale_lang']]
        all_links = list(set(all_links))
    
    assert len(all_links) == 225 # number can be changed, checked on 2025-01-01

    ### get all data from each link
    for link in tqdm(all_links):
        current_data = {}

        # url
        # link = 'https://vwo.com/success-stories/convert-better/'
        current_data['analysis_url'] = link
        print('Url:', link)
        driver.get(link)

        # title
        current_data['page_title'] = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/div/h1').text
        print('Title:', current_data['page_title'])

        # company
        current_data['company'] = {}
        current_data['company']['name'] = link.split('/')[-2]
        company = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div/div[2]/div/div/div[2]')
        company_info = company.find_elements(By.TAG_NAME, 'div')
        for info in company_info:
            title = info.find_element(By.TAG_NAME, 'h4').text
            content = info.find_element(By.TAG_NAME, 'p').text
            current_data['company'][title] = content
        print('Company:', current_data['company'])
        
        # raw contents
        current_data['raw_contents'] = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div/div[1]').text

        # raw images
        main_part = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div/div[1]')
        image_links = [img.get_attribute('src') for img in main_part.find_elements(By.TAG_NAME, 'img') if img.get_attribute('src').startswith('https://static.wingify.com/gcp/')]
        current_data['raw_images'] = image_links
        
        # external comment blank
        current_data['external_comment'] = ['']
        
        
        # save to json
        data_dict.append(current_data)
        with open('../../vwo_success_stories.json', 'w') as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False)
    
def vwo_image_download():
    with open('../../vwo_success_stories.json', 'r') as f:
        data = json.load(f)
    
    for i, d in tqdm(enumerate(data)):
        os.makedirs(f'../../image/vwo/{i}', exist_ok=True)
        for j, img_link in enumerate(d['raw_images']):
            response = requests.get(img_link)
            with open(f'../../image/vwo/{i}/{j}.png', 'wb') as f:
                f.write(response.content)

if __name__ == '__main__':
    vwo_success_stories_data_crawl(reuse_links=True)
    vwo_image_download()