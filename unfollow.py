from csv import reader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bot import Bot, driver
from keys import insta_user, insta_pw
from time import sleep


unfollow_bot = Bot(insta_user, insta_pw)

driver.get(f'https://www.instagram.com/{insta_user}')

following = driver.find_element_by_css_selector('#react-root > section > main > div > header > section > ul > li:nth-child(3) > a')
following.click()
sleep(3)

with open('2019-05-10-22:58_users_followed_list.csv') as file:
    csv_reader = reader(file)
    followed_list = []
    for user in csv_reader:
        followed_list.append(user[1])
    
    unfollowed = 0

    for x in range(1, len(followed_list)):
        username = driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div.isgrP > ul > div > li:nth-child(1) > div > div.t2ksc > div.enpQJ > div.d7ByH > a').text
        if username in followed_list:
            unfollow = driver.find_element_by_css_selector(f'body > div.RnEpo.Yx5HN > div > div.isgrP > ul > div > li:nth-child({x}) > div > div.Pkbci > button')
            unfollow.click()
            sleep(2)
            confirm = driver.find_element_by_css_selector('body > div:nth-child(16) > div > div > div.mt3GC > button.aOOlW.-Cab_')
            confirm.click()
            sleep(4)
            unfollowed += 1
    
    close = driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div:nth-child(1) > div > div:nth-child(3) > button > span')
    close.click()
    
    print(f'unfollowed {unfollowed} users')


        