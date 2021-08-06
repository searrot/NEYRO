from selenium.webdriver import Chrome, Firefox
from getpass import getpass
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import urllib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory
import time
import uuid
import os, requests, logging
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import cv2
import pytesseract 
from selenium.webdriver.support.ui import WebDriverWait
logging.basicConfig(level=logging.DEBUG)

batch_size = 32
image_size = (254, 254)
model = load_model('crypto_checking_network.h5')

options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
'''driver.get('https://twitter.com/login')
time.sleep(2)
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys("@IKudryavtzeff")
time.sleep(2)
my_password = 'Persik228'
time.sleep(2)
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)'''
time.sleep(3)
driver.get('https://twitter.com/IKudryavtzeff')
time.sleep(5)
card = driver.find_element_by_xpath('//div[@data-testid="tweet"]')
time.sleep(5)
time_post = card.find_element_by_xpath('.//time').get_attribute('datetime')
last_time = time_post
trigger = False


def get_image(container):
    try:
        time.sleep(2)
        WebDriverWait(driver, 15).until(lambda container: container.find_element_by_xpath('.//img'))
        images:List[WebElement] = container.find_elements_by_xpath('.//img')
        del images[0]
        if len(images) < 2:
            imname = uuid.uuid4()
            src = images[0].get_attribute('src')
            urllib.request.urlretrieve(src, f'/projects/im/ims/{imname}.jpg')
            print('IMAGE SAVE SUCCESsS')
        else:
            for element in images:
                imname = uuid.uuid4()
                src = element.get_attribute('src')
                urllib.request.urlretrieve(src, f'/projects/im/ims/{imname}.jpg')
                print('IMAGE SAVE SUCCESsS')
    except:
        print('ERROR SAVE IMAGE')
        

def get_text(card):
    global trigger
    try:
        text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        if 'doge' in text or 'shib' in text:
            trigger = True
            print('DOUG')
            r = requests.get('http://45.137.64.175:2000/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
        print(text)
    except:
        pass

def check_image_text():
    global trigger
    try:
        images = os.listdir('/projects/im/ims/')
        for img in images:
            if not trigger:
                img = cv2.imread(f'/projects/im/ims/{img}')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                res = pytesseract.image_to_string(img)
                res = res.lower()
                print(res)
                if 'doge' in res or 'shib' in res:
                    trigger = True
                    print('DOUG')
                    r = requests.get('http://45.137.64.175:2000/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
    except:
        print('text_img_ERROR')

def check_image():
    global trigger
    try:
        test_dataset = image_dataset_from_directory('/projects/im/',
                                                batch_size=batch_size,
                                                image_size=image_size)
        res = model.predict(test_dataset)
        for pic in res:
            if not trigger:
                if pic[3] > 0.5 or pic[5] > 0.5:
                    print('DOUG')
                    r = requests.get('http://45.137.64.175:2000/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
                    trigger = True
    except:
        pass
#//div[2]/div[2]

def check_tweets(l_t):
    last_time = l_t
    global trigger
    while True:
        driver.implicitly_wait(10)
        container:WebElement = driver.find_element_by_xpath('//div[@data-testid="tweet"]')

        #time.sleep(3)
        #card = cards[0]
        time_post = container.find_element_by_xpath('.//time').get_attribute('datetime')

        if time_post != last_time:
            get_text(container)
            if not trigger:
                get_image(container)

                time.sleep(1)
                check_image()
                check_image_text()
            trigger = False
            for elem in os.listdir('/projects/im/ims/'):
                os.remove(f'/projects/im/ims/{elem}')
        last_time = time_post
        driver.refresh()
        driver.implicitly_wait(5)

check_tweets(last_time)
'''while True:
    card = driver.find_element_by_xpath('//div[@data-testid="tweet"]')
    time_post = card.find_element_by_xpath('.//time').get_attribute('datetime')

    if time_post != last_time:
        print(get_text())
        get_image()

    last_time = time_post'''