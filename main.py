import json
import time
import shutil
import os

import requests
from requests.structures import CaseInsensitiveDict
import re
import config

account_list = []


def load_account_list():
    with open(config.account_list_path, 'r') as accounts_list_file:
        for line in accounts_list_file:
            if line.endswith('\n'):
                account_list.append(line[:-1])
            else:
                account_list.append(line)


def get_dump(url):

    image_urls_list = []

    headers = CaseInsensitiveDict()
    headers["authority"] = "www.instagram.com"
    headers["method"] = "GET"
    headers["path"] = "/wizkhalifa/"
    headers["scheme"] = "https"
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["accept-language"] = "ru-RU,ru;q=0.9"
    headers["sec-ch-ua"] = '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"'
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-ch-ua-platform"] = '"Windows"'
    headers["sec-fetch-dest"] = "document"
    headers["sec-fetch-mode"] = "navigate"
    headers["sec-fetch-site"] = "none"
    headers["sec-fetch-user"] = "?1"
    headers["upgrade-insecure-requests"] = "1"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

    resp = requests.get(url, headers=headers)

    print(resp.status_code)

    if len(re.findall(r'[Войдите, чтобы увидеть снимки и записи]{39}', resp.text)) >= 1:
        print('dead proxy')
    else:
        example_private_auto = r'([{"config"]{9}.{0,999999})[;</script>]{10}'
        private_auto_list = re.findall(example_private_auto, resp.text)
        dict_results = json.loads(private_auto_list[0])

        image_urls_list.append(dict_results['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'])
        for node in dict_results['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            if 'edge_sidecar_to_children' in node['node'].keys():
                for children_node in node['node']['edge_sidecar_to_children']['edges']:
                    image_urls_list.append(children_node['node']['display_url'])
            image_urls_list.append(node['node']['display_url'])

    if len(image_urls_list) < 13:
        return False
    else:
        for paths in os.listdir(config.results_storage_path):
            if paths == str(account_list.index(url)):
                shutil.rmtree(f'{config.results_storage_path}/{str(account_list.index(url))}')
                print('такое имя директории уже было, она будет перезаписана')
        try:
            os.mkdir(f'{config.results_storage_path}/{str(account_list.index(url))}')
        except OSError:
            print('ошибка создания директории')
        else:
            for image_urls in image_urls_list:
                p = requests.get(image_urls)
                with open(f'{config.results_storage_path}/{str(account_list.index(url))}/{str(image_urls_list.index(image_urls))}.jpg', 'wb') as uploaded_image:
                    uploaded_image.write(p.content)
            return True


load_account_list()
print(f'{len(account_list)} аккаунтов загружено')

for accounts in account_list:
    start_time = time.time()
    get_dump(accounts)
    print(f'Аккаунт {accounts} был успешно выгружен за {round(time.time() - start_time)} секунд')


