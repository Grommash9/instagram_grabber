import json
import re

import requests
from requests.structures import CaseInsensitiveDict

import config
parsing_data = ''

accounts_list_urls = []


with open(f"{config.results_storage_path}/parsers.txt", 'rb') as file_parsing_data:
    for line in file_parsing_data:
        parsing_data = line

example_private_auto = r'[{href="/]{7}(.{0,30})[/]{1}'
private_auto_list = re.findall(example_private_auto, str(parsing_data))
for accounts in set(private_auto_list):
    accounts_list_urls.append(f'https://www.instagram.com/{accounts}/')


for accounts in accounts_list_urls:
    with open(f'{config.account_list_path}', 'a') as accounts_file:
        accounts_file.write(f'{accounts}\n')
