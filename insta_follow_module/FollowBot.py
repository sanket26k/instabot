from lib2to3.pgen2.token import NEWLINE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys


from time import sleep
from random import randint, choice
import logging

from .credentials import username, password
from .constants import max_delay, login_button_xpath, hashtags, \
    not_now_xpath, instagram_url, search_class_name, follow_xpath, \
    unfollow_xpath, unfollow_button_xpath, unrequest_xpath, fl_daily_user

class FollowBot():
    def __init__(self):
        self.counter = 0
        self.posts = []
        self.commenters = []
        self.logger_init()
        self.start_selenium()

    @staticmethod
    def rand_sleep(min=1, max=5):
        time = randint(min, max)
        sleep(time)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def logger_init(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        logging.info('\n')

    def start_selenium(self):
        self.logger.debug("Starting")
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(max_delay)
        self.driver.maximize_window()
        self.driver.get(instagram_url)
        self.rand_sleep(2,3)
        try:
            self.logger.info("Waiting for page to load")
            myElem = WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.ID, 'react-root')))
        except TimeoutException:
            self.logger.error("Couldn't load instagram home page")
        finally:
            self.logger.info("Instagram Homepage loaded")
        
    def type(self, element_name, value):
        WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.NAME, element_name)))
        box = self.driver.find_element_by_name(element_name)
        self.logger.info(f"Found {element_name} box, typing...")
        box.send_keys(value)
        WebDriverWait(self.driver, max_delay).until(lambda browser: box.get_attribute('value') == value)

    def click(self, xpath):
        WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.logger.info(f"Clicking {xpath}")
        self.driver.find_element_by_xpath(xpath).click()
        self.rand_sleep()

    def login(self):
        self.type("username", username)
        self.type("password", password)
        self.click(login_button_xpath)
        self.click(not_now_xpath)
        self.click(not_now_xpath)   


    def search(self):
        box = self.driver.find_element_by_class_name(search_class_name)
        search_term = "#" + choice(hashtags)
        self.logger.info(f"Searhing for {search_term}")
        box.send_keys(search_term)
        WebDriverWait(self.driver, max_delay).until(lambda browser: box.get_attribute('value') == search_term)
        self.rand_sleep()
        box.send_keys(Keys.ENTER)
        self.rand_sleep()
        box.send_keys(Keys.ENTER)
        self.rand_sleep(4,7)

    def go_to_profile(self, user = fl_daily_user):
        self.driver.get(instagram_url+fl_daily_user)
        self.rand_sleep()


    def get_all_posts(self):
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            post = link.get_attribute('href')
            if '/p/' in post:
                self.posts.append(post)

    def get_random_post(self):
        self.post = choice(self.posts)
        self.posts.remove(self.post)
        with open('posts.log', 'r') as f:
            all_posts = f.readlines()
        if self.post+'\n' not in all_posts:
            with open('posts.log','a') as f:
                f.write(self.post+'\n')
        else:
            self.get_random_post()
        self.driver.get(self.post)
        self.rand_sleep()
        
        # check if post has already been visited
        # otherwise add it to a new log file of visited links

    def get_all_likers(self):
        self.likers = []
        self.driver.get(self.driver.current_url + "liked_by")
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            attr = link.get_attribute('href')
            if attr.startswith(instagram_url):
                attr = attr.replace(instagram_url, '')[:-1]
                if ('/' not in attr) and ('explore' not in attr) and (attr != ''):
                    self.likers.append(attr)
        self.likers = list(set(self.likers))
        self.number_of_likers = len(self.likers)

    
    def get_all_commenters(self):
        self.commenters = []
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            attr = link.get_attribute('href')
            if attr.startswith(instagram_url):
                attr = attr.replace(instagram_url, '')[:-1]
                if ('/' not in attr) and ('explore' not in attr) and (attr != ''):
                    self.commenters.append(attr)
        self.commenters = list(set(self.commenters))
        self.number_of_comments = len(self.commenters)
        
        # store number of comments in a variable
        # make sure number of comments is at least 3
        # if not call get_random post again until posts is empty
        
    def get_random_liker(self):
        user = choice(self.likers)
        self.likers.remove(user)
        with open('users.log', 'r') as f:
            all_followed_users = f.readlines()
        if user+'\n' not in all_followed_users:
            with open('users.log','a') as f:
                f.write(user+'\n')
            user_link = instagram_url + user 
            self.driver.get(user_link)
            return True
        else:
            return False

    def get_random_commenter(self):
        # if not self.commenters:
        #     self.get_all_commenters()
        user = choice(self.commenters)
        self.commenters.remove(user)
        with open('users.log', 'r') as f:
            all_followed_users = f.readlines()
        if user+'\n' not in all_followed_users:
            with open('users.log','a') as f:
                f.write(user+'\n')
            user_link = instagram_url + user 
            self.driver.get(user_link)
            return True
        else:
            return False
        # store follower names in new file
        # check if commentor name if in the list, if not click
        # and add it to list
        # remove infinite lop from here
    
    # def follow_user(self):
    #     self.click(follow_xpath)
        # press follow button, if it already says following, do nothing
        # update follower counter


    def follow_loop(self, likers=True):
        # loop counter of number of users followed, max_daily_limit < 149
        self.get_all_posts()
        self.get_random_post()
        if likers:
            self.get_all_likers()
        else:
            self.get_all_commenters()

        while self.counter < 10:
            if likers:
                while not self.get_random_liker():
                    pass
            else:
                while self.get_random_commenter():
                    pass
            
            try:
                self.click(follow_xpath)
                self.counter += 1
            except:
                self.logger.warning("Couldn't follow, something went wrong")
                
            # if not self.posts:
            #     print(self.counter)
            #     break
            # if self.counter > 50:
            #     break


    def unfollow_loop(self):
        with open('users.log', 'r') as f:
            all_followed_users = f.readlines()
        for user in all_followed_users:
            user_url = instagram_url + user[:-1]
            self.counter += 1
            try:
                self.driver.get(user_url)
                self.rand_sleep()
                if self.check_exists_by_xpath(unfollow_xpath):
                    self.click(unfollow_xpath)
                else:
                    self.click(unrequest_xpath)
                self.rand_sleep()
                self.click(unfollow_button_xpath)
                self.logger.debug(f"Unfollowed {user}")
            except:
                self.logger.warning(f"Couldn't unfollow user {user}")
            finally:
                with open("users.log", "r+") as f:
                    d = f.readlines()
                    f.seek(0)
                    for i in d:
                        if i != user:
                            f.write(i)
                    f.truncate()
            # all_followed_users.remove(user)
            # if not all_followed_users:
            #     break
            if self.counter > 10:
                break


        
        
                