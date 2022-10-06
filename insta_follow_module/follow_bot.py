from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import getpass


from time import sleep
from random import randint, choice
import logging

from .constants import max_delay, login_button_xpath, \
    not_now_xpath, instagram_url, follow_xpath, \
    unfollow_xpath, unfollow_button_xpath, unrequest_xpath, fl_daily_user

from .file_handler import FileHandler
from .gui import Gui

class FollowBot():
    def __init__(self):
        self.post = []
        self.logger_init()
        self.file_handler = FileHandler()
        self.credentials = self.file_handler.get_credentials()
        # self.gui = Gui()
        # self.gui.enter_user_pw()
        if not self.credentials:
            user = input("Username:")
            passwd = getpass.getpass("Password for " + user + ":")
            self.file_handler.enter_credentials(user, passwd)
            self.credentials = self.file_handler.get_credentials()

        self.start_selenium()
        self.login()

    @staticmethod
    def rand_sleep(min=1, max=5):
        time = randint(min, max)
        sleep(time)

    def check_exists_by_xpath(self, xpath):
        elem = self.driver.find_elements_by_xpath(xpath)
        if len(elem) > 0:
            return True
        return False

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
        
    def type_in(self, element_name, value):
        WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.NAME, element_name)))
        box = self.driver.find_element_by_name(element_name)
        self.logger.info(f"Found {element_name} box, typing...")
        box.send_keys(value)
        WebDriverWait(self.driver, max_delay).until(lambda browser: box.get_attribute('value') == value)

    def click(self, xpath):
        if not self.check_exists_by_xpath(xpath):
            return
        WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.logger.info(f"Clicking {xpath}")
        self.driver.find_element_by_xpath(xpath).click()
        self.rand_sleep()

    def login(self):
        self.type_in("username", self.credentials['username'])
        self.type_in("password", self.credentials['password'])
        self.click(login_button_xpath)
        self.click(not_now_xpath)
        self.click(not_now_xpath)   

    def scroll_down(self, n_scrolls = 20):
        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        n = 0
        while n < n_scrolls:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            n += 1

    def go_to_profile(self, user = fl_daily_user):
        self.driver.get(instagram_url+fl_daily_user)
        self.rand_sleep()

    def update_posts(self):
        self.go_to_profile()
        self.rand_sleep(5,8)
        self.scroll_down()
        self.posts = self.file_handler.load('posts')
        posts = dict()
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            post = link.get_attribute('href')
            if '/p/' in post:
                if 'liked_by' not in post:
                    posts[post] = 0 # not visited
        updated_posts = posts.keys() - self.posts.keys()
        for post in updated_posts:
            self.posts[post] = 0
        self.file_handler.dump('posts', self.posts)
        self.rand_sleep()

    def get_post(self):
        if all(value != 0 for value in self.posts.values()):
            self.update_posts()
        for post, read in self.posts.items():
            self.post = post
            if not read:
                self.driver.get(self.post)
                self.rand_sleep()
                self.posts[self.post] += 1
                self.file_handler.dump('posts', self.posts)
                break

    def update_likers(self):
        if not self.post:
            self.get_post()
        self.likers = self.file_handler.load('likers')
        self.driver.get(self.driver.current_url + "liked_by")
        self.rand_sleep()
        self.scroll_down()
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            attr = link.get_attribute('href')
            if attr.startswith(instagram_url):
                attr = attr.replace(instagram_url, '')[:-1]
                if ('/' not in attr) and ('explore' not in attr) and (attr != ''):
                    if attr not in self.likers:
                        self.likers[attr] = 0
        self.file_handler.dump('likers', self.likers)

    def go_to_liker(self, follow_check = 0):
        if all(value != follow_check for value in self.likers.values()):
            self.update_likers()
        for user, followed in self.likers.items():
            if followed==follow_check:
                self.driver.get(instagram_url + user)
                self.rand_sleep()
                self.likers[user] = follow_check+1
                self.file_handler.dump('likers', self.likers)
                break
    
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
            self.rand_sleep()
            return True
        else:
            return False
      
    def follow_loop(self, max_per_hour = 10):
        # loop counter of number of users followed, max_daily_limit < 149

        self.update_likers()
        counter = 0
        while counter <= max_per_hour:
            self.go_to_liker()
            # self.like_user_posts()
            self.click(follow_xpath)
            self.rand_sleep()
            counter+=1
                
    def unfollow_loop(self, max_per_hour = 10):
        self.likers = self.file_handler.load('likers')
        counter = 0
        while counter <= max_per_hour:
            self.go_to_liker(follow_check=1)
            self.click(unfollow_xpath)
            self.click(unrequest_xpath)
            self.rand_sleep()
            self.click(unfollow_button_xpath)
            self.rand_sleep()
            counter+=1

    def start_loop(self, n_hours=24):
        self.update_posts() # update daily?
        for i in range(n_hours):
            self.follow_loop()
            sleep(30*60)
            self.unfollow_loop()
            sleep(30*60)