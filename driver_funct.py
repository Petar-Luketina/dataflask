from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
from time import sleep
import random
import base64

def type_word(word, element):
    for letter in word:
        sleep(random.uniform(.1, .4))
        element.send_keys(letter)


def type_credentials(driver, data):
    sign_in = driver.find_element(by='link text', value='Sign in')
    sign_in.click(); sleep(1)
    email_entry = driver.find_element(by='css selector', value='#username')
    password_entry = driver.find_element(by='css selector', value='#password')
    type_word(data['username'], email_entry)
    type_word(data['password'], password_entry)
    password_entry.send_keys(Keys.RETURN)


def start_crawling(driver, entries=10):
    text_set = set()
    for i in range(entries):
        css = '.occludable-update:nth-child({}) > div > div:nth-child(3)'.format(i)
        scroll = "window.scrollTo(0, {})".format(i * 500)
        try:
            ele = driver.find_element(by='css selector', value=css)
            driver.execute_script(scroll)
            text = ele.text.replace('hashtag', '')\
                           .replace('\n', '')\
                           .replace('…see more', '')\
                           .replace('#', '')
            text_set.add(text)
            sleep(.4)
        except: pass
        s = ' '.join(text_set)
        stopwords = set(STOPWORDS)
        my_stopwords = {'see', 'help', 'will'}
        stopwords = stopwords.union(my_stopwords)
        cloud = WordCloud(
            background_color='white',
            max_words=5000,
            stopwords=stopwords,
            width=800,
            height=400
        )
    cloud.generate(s)
    return cloud.to_image()
    # cloud.to_file('./static/media/temp/wordcloud.jpg')


def serve_pil_image(pil_img):
    return base64.b64encode(pil_img.tobytes())
