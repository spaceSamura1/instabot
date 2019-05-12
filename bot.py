from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import time
from random import randint
import pandas as pd 
from keys import insta_user, insta_pw


chromedriver_path = '/Users/tylerceja/Downloads/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path)

class Bot:
    prev_user_list = [] #users followed
    new_followed = []
    followed = 0
    likes = 0
    comments = 0

    def __init__(self, handle, password):
        self.handle = handle
        self.password = password

    def login(self):
        driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        sleep(3)

        username = driver.find_element_by_name('username')
        username.send_keys(self.handle)
        password = driver.find_element_by_name('password')
        password.send_keys(self.password)
        sleep(3)
                
        button_login = driver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div')
        button_login.click()
        sleep(6)

        #exits pop up notification
        not_now = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]')
        not_now.click()

    
    def run_bot(self, num_posts):
        prev_user_list = self.prev_user_list
        new_followed = self.new_followed
        followed = self.followed
        likes = self.likes
        comments = self.comments
        tag = 0
        hashtag_list = ['digitalmarketing', 'contentmarketing', 'experiential', 'influencer', 'marketingdigital']
        text = ['This is great, nice work!', 'This looks so cool! Really well done and very artistic', 'Nice! This is epic.', 
                'Well this definitely made me stopped scrolling! haha', 'This is art!', 'Really cool, I love this idea' ]
                        

        for hashtag in hashtag_list:
            driver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
            sleep(5)
            first_thumbnail = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
            first_thumbnail.click()
            sleep(4)
            
            for x in range(1, num_posts):
                sleep(5) 
                #sleep necessary b/c it is searching for username before the page is rendered

                username = driver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a').text
                #follow user if not already following
                if username not in prev_user_list:
                    if driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                                                            
                        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                        new_followed.append(username)
                        followed += 1

                        #like the image
                        heart_button = driver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span')
                        heart_button.click()
                        likes += 1
                        sleep(randint(1,5))

                        #comment
                        driver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form').click()
                        comment_box = driver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                        comm_prob = randint(1, len(text)) - 1
                        
                        print(f'{hashtag}_{x}: {comm_prob}')

                        #choose a random comment from text list
                        comment_box.send_keys(text[comm_prob])
                        sleep(2)
                        comment_box.send_keys(Keys.ENTER)
                        comments += 1
                        sleep(randint(5,8))


                driver.find_element_by_link_text('Next').click()
            tag += 1
        
    def create_csv_log(self):
        new_followed = self.new_followed
        prev_user_list = self.prev_user_list
        likes = self.likes
        comments = self.comments
        for n in range(0, len(new_followed)):
            prev_user_list.append(new_followed[n])

        updated_user_df = pd.DataFrame(prev_user_list)
        updated_user_df.to_csv(f'{strftime("%Y-%m-%d-%H:%M")}_users_followed_list.csv')
        print(f'Liked {likes} photos')
        print(f'Commented on {comments} images')
        print(f'Followed {new_followed} new users')



new_bot = Bot(insta_user, insta_pw)
new_bot.login()

if __name__ == '__main__':
    new_bot.run_bot(30)
    new_bot.create_csv_log()

#====================================
#Create hashtag list and CSV for user log
#====================================


# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])

