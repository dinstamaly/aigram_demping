__author__ = 'Dinmukhamed Stamaliev'

import requests
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import PROF_INFO, driver


def make_request():
    s = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    data = {
        'action': 'login',
        'username': PROF_INFO.get('username'),
        'password': PROF_INFO.get('password')
    }
    login_url = 'https://kaspi.kz/mc/api/login'

    s.post(
        url=login_url,
        headers=headers,
        data=data
    )
    return s


def get_difference(url):
    driver.get(url + '?c=750000000#!/item')
    print('asdasdasdasdasdasd')
    try:
        a1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, ".//tr[1]//td[@class='sellers-table__cell']//a"))
        )
        a2 = driver.find_element("xpath",
            ".//tr[1]//td[@class='sellers-table__cell']//div[@class='sellers-table__price-cell-text']")

        rows = driver.find_elements("xpath",
            "//table[@class='sellers-table__self']/tbody/tr")
        print(rows)

        if len(rows) >= 2:
            if 'eco iherbkz' in a1.text:
                a3 = driver.find_element("xpath",
                    ".//tr[2]//td[@class='sellers-table__cell']//a")
                a4 = driver.find_element("xpath",
                    ".//tr[2]//td[@class='sellers-table__cell']//div[@class='sellers-table__price-cell-text']")
                a4 = a4.text.replace(' ', '')
                return a3.text, float(a4[:-1])
        a2 = a2.text.replace(' ', '')
        return a1.text, float(a2[:-1])
    except TimeoutException:
        print('time out')


def get_min_value(url, price):
    print('+++++++++++++++++++++++++')
    print(url)
    print('+++++++++++++++++++++++++')
    name, _price = get_difference(url)
    data_dict = {}
    diff = _price - price
    if 'eco iherbkz' in name or diff in [0, 1]:
        return data_dict
    data_dict['name'] = name
    data_dict['price'] = _price
    data_dict['difference'] = diff

    return data_dict
