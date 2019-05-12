from csv import reader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bot import Bot, driver
from keys import insta_user, insta_pw

with open('2019-05-09-16:13_users_followed_list.csv') as file:
    csv_reader = reader(file)
    followed_list = []
    for user in csv_reader:
        followed_list.append(user)

unfollow_bot = Bot(insta_user, insta_pw)
unfollow_bot.login()

driver.get(f'https://www.instagram.com/{insta_user}')

        