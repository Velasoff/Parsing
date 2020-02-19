from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget
import time
from pymongo import MongoClient

driver = webdriver.Firefox()
driver.get("https://music.yandex.ru/genre/%D0%BC%D0%B5%D1%82%D0%B0%D0%BB/albums/new")
client = MongoClient('localhost', 27017)
mongo_base = client.yandex_music
time.sleep(5)
# ads = driver.find_element_by_class_name('local-icon-theme-black')
# ads.click()
collection = mongo_base['metal']
albums = driver.find_elements_by_class_name('album')
driver.find_element_by_tag_name('body').send_keys(Keys.END)
i = 0
s = {}
for album in albums:
    if i % 3 == 0:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
    album.click()
    time.sleep(1)
    album_name = driver.find_elements_by_xpath('//div[@class="sidebar__title sidebar-album__title typo-h2"]'
                                               '//a[@class="d-link deco-link"]')[-1].text
    album_href = driver.find_elements_by_xpath('//div[@class="sidebar__title sidebar-album__title typo-h2"]'
                                               '//a[@class="d-link deco-link"]')[-1].get_attribute("href")
    band_name = driver.find_elements_by_xpath('//span[@class="d-artists"]'
                                              '//a[@class="d-link deco-link"]')[-1].text
    genre = driver.find_element_by_xpath('//a[@class="d-link deco-link deco-link_mimic typo"]').text
    year = driver.find_element_by_xpath('//span[@class="typo deco-typo-secondary"]').text
    songs = driver.find_elements_by_xpath(
        '//div[@class="lightlist__cont"]//div[@class="d-track typo-track d-track_inline-meta d-track__sidebar"]//a[@class="d-track__title deco-link deco-link_stronger"]')
    song_list = []
    img = driver.find_element_by_class_name('album_selected').find_element_by_tag_name('img').get_attribute('src')
    for song in songs:
        if song.get_attribute("href")[:-15] == album_href:
            song_list.append(song.text)
    wget.download(img, f"./images/{album_name}.jpeg")
    s[i] = {'album_name': album_name,
            'album_href': album_href,
            'band_name': band_name,
            'genre': genre,
            'year': year,
            'songs': song_list}
    # print(img)
    collection.insert_one({'album_name': album_name,
                           'album_href': album_href,
                           'band_name': band_name,
                           'genre': genre,
                           'year': year,
                           'img_src': img,
                           'songs': song_list})
    i += 1
    if i == 20:
        driver.quit()
        print(s)
