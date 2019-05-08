from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import time
from random import randint
import pandas as pd 
from keys import insta_user, insta_pw

#====================================
#Log in to instagram
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

button_login = webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div')
button_login.click()
sleep(3)

not_now = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
not_now.click()

#====================================
#Create hashtag list and CSV for user log
#====================================

hashtag_list = ['brandadvertising', 'experiential', 'experientialdesign', 'marketing' 'experientialart', 'experientialevents']

prev_user_list = [] #users followed

# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])


#====================================
#Loop through hashtags - follow, comment, like posts
#====================================

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    first_thumbnail.click()
    sleep(randint(1,2))
   
    try:
        for x in range(1,10):
            username = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a').text

            #follow user
            if username not in prev_user_list:
                if webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.bY2yH > button').text == 'Follow':
                    webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.bY2yH > button').click()

                    new_followed.append(username)
                    followed += 1

                #like the image
                heart_button = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span')
                heart_button.click()
                likes += 1
                sleep(randint(1,10))

                #Comments
                comm_prob = randint(1,10)
                print(f'{hashtag}_{x}:{comm_prob}')
                if comm_prob > 7:
                    comments += 1
                    webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form').click()
                    comment_box = webdriver.find_element_by_xpath('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                    if(comm_prob < 7):
                        comment_box.send_keys('This is beautiful, really well done!')
                        sleep(1)
                    elif(comm_prob > 6) and (comm_prob < 9):
                        comment_box.send_keys('I love this! Definitely stopped me on my scroll haha')
                        sleep(1)
                    elif comm_prob == 9:
                        comment_box.send_keys('Very nicely done, great execution!')
                    elif comm_prob == 10:
                        comment_box.send_keys('Very artisic! The colors here are so beautiful')
                    
                    comment_box.send_keys(Keys.ENTER)
                    sleep(randint(22,28))
            
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(25,29))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(20,26))
    except:
        continue

for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv(f'{strftime("%Y%m%d-%H%M%S")}_users_followed_list.csv')
print(f'Liked {likes} photos')
print(f'Commented on {comments} images')
print(f'Followed {new_followed} new users')
