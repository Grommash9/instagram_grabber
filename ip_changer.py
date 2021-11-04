import asyncio
import random
import threading
import time

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, ElementNotSelectableException, \
    NoSuchElementException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import config

try_count = [0]


def isntConnected():
    import urllib
    from urllib import request
    try:
        try_count[0] += 1
        urllib.request.urlopen('http://google.com', timeout=5)
        print('\nинтернет есть')
        time.sleep(7)
        return False
    except:
        print(f'-{try_count[0]}-', end='')
        return True


def ipchange():
        ischanged = True
        try_count[0] = 0
        start_time = time.time()
        print('Начинаю менять айпи')
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        browser_ip_change = webdriver.Chrome(options=options, executable_path=config.chrome)
        browser_ip_change.get('http://192.168.8.1/')
        browser_ip_change.set_page_load_timeout(15)

        elem = WebDriverWait(browser_ip_change, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#tbarouter_username')))
        login_input = browser_ip_change.find_element_by_css_selector('#tbarouter_username')
        login_input.send_keys('admin')

        password_input = browser_ip_change.find_element_by_css_selector('#tbarouter_password')
        password_input.send_keys('admin')

        confirm_button = browser_ip_change.find_element_by_css_selector('#btnSignIn')
        confirm_button.click()

        internet_settings_waiter = WebDriverWait(browser_ip_change, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#tInternet')))
        internet_settings = browser_ip_change.find_element_by_css_selector('#tInternet')
        internet_settings.click()

        network_selectModeType = WebDriverWait(browser_ip_change, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#network_selectModeType')))
        select = Select(browser_ip_change.find_element_by_css_selector('#network_selectModeType'))
        time.sleep(3)
        select.select_by_value('5')


        btn_network_mode_waiter = WebDriverWait(browser_ip_change, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_network_mode_apply')))
        btn_network_mode = browser_ip_change.find_element_by_css_selector('#btn_network_mode_apply')
        btn_network_mode.click()
        time.sleep(10)

        network_selectModeType = WebDriverWait(browser_ip_change, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#network_selectModeType')))
        select = Select(browser_ip_change.find_element_by_css_selector('#network_selectModeType'))
        select.select_by_value('2')

        time.sleep(2)
        btn_network_mode_waiter = WebDriverWait(browser_ip_change, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_network_mode_apply')))
        btn_network_mode = browser_ip_change.find_element_by_css_selector('#btn_network_mode_apply')
        btn_network_mode.click()
        time.sleep(10)

        while isntConnected():
            if try_count[0] < 8:
                time.sleep(5)
            else:
                browser_ip_change.quit()
                print(f'что-то пошло не так с айпи, пробую менять ещё раз')
                ischanged = False
                ipchange()
                break
        if ischanged:
            browser_ip_change.quit()
            print(f'айпи адрес успешно изменен за {(time.time() - start_time)} секунд')