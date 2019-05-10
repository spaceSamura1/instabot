from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import time
from random import randint
import pandas as pd 
from keys import insta_user, insta_pw



#====================================
#Login to instagram
#====================================
chromedriver_path = '/Users/tylerceja/Downloads/chromedriver'
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys(insta_user)
password = webdriver.find_element_by_name('password')
password.send_keys(insta_pw)
sleep(2)

button_login = webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div')
button_login.click()
sleep(3)

#exits pop up notification
not_now = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
not_now.click()

#====================================
#Create hashtag list and CSV for user log
#====================================

hashtag_list = ['brandmarketing', 'experientialdesign', 'experiential', 'experientialart', 'experientialevents']

prev_user_list = [] #users followed

# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])


#====================================
#Loop through hashtags - follow, comment, like posts
#====================================

new_followed = []
tag = 0
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    first_thumbnail.click()
    sleep(randint(1,2))
    
    for x in range(1,20):
        sleep(3) 
        #sleep necessary b/c it is searching for username before the page is rendered

        username = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a').text
        #follow user if not already following
        if username not in prev_user_list:
            if webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                                                       
                webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                new_followed.append(username)
                followed += 1

                #like the image
                heart_button = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span')
                heart_button.click()
                likes += 1
                sleep(randint(1,5))

                #comment
                webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form').click()
                comment_box = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                text = ['The colors in this are amazing!', 'This looks so cool! Really well done and very artistic', 'Nice! This is epic. Great work', 
                        'Well this definitely made me stopped scrolling! haha', 'This is art!' ]
                
                comm_prob = randint(1, len(text)) - 1
                
                print(f'{hashtag}_{x}: {comm_prob}')

                comment_box.send_keys(text[comm_prob])

                comment_box.send_keys(Keys.ENTER)
                comments += 1
                sleep(randint(5,10))


        webdriver.find_element_by_link_text('Next').click()
    tag += 1


for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv(f'{strftime("%Y-%m-%d-%H:%M")}_users_followed_list.csv')
print(f'Liked {likes} photos')
print(f'Commented on {comments} images')
print(f'Followed {new_followed} new users')
