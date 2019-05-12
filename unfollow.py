from csv import reader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bot import Bot, driver
from keys import insta_user, insta_pw
from time import sleep

with open('2019-05-09-16:13_users_followed_list.csv') as file:
    csv_reader = reader(file)
    followed_list = []
    for user in csv_reader:
        followed_list.append(user)

unfollow_bot = Bot(insta_user, insta_pw)

driver.get(f'https://www.instagram.com/{insta_user}')

following = driver.find_element_by_css_selector('#react-root > section > main > div > header > section > ul > li:nth-child(3) > a')
following.click()
sleep(3)

for x in range(1, 10):
    unfollow = driver.find_element_by_css_selector(f'body > div.RnEpo.Yx5HN > div > div.isgrP > ul > div > li:nth-child({x}) > div > div.Pkbci > button')
    unfollow.click()
    sleep(2)
    confirm = driver.find_element_by_css_selector('body > div:nth-child(16) > div > div > div.mt3GC > button.aOOlW.-Cab_')
    confirm.click()
    sleep(2)


        