import os
# bot father
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


dir_path = os.path.dirname(os.path.realpath(__file__))
DRIVER_PATH = os.path.join(dir_path, 'chromedriver')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

PROF_INFO = {
    'username': "alevtinanur89@gmail.com",
    'password': "Dmitrii19891989!"
}