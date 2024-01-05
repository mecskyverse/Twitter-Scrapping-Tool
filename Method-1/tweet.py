from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from time import sleep


class Tweet:
    def __init__(self,
            driver: webdriver.Chrome,
            Ad: list
    ):
        self.driver = driver
        self.Ad = Ad

        while True:
            try:
                self.tweet = self.__get_first_tweet()
                if self.tweet == "stop":
                    return None
                self.__remove_pinned()

                self.tweet_url, self.retweet = self.__get_tweet_url()
                self.tweet_date = self.__get_tweet_date()
                self.tweet_text = self.__get_tweet_text()
                self.tweet_lang = self.__get_tweet_lang()
            
            except TypeError:
                Ad[0] += 1
                sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", self.tweet)
                continue
            
            break

        self.__delete_tweet()

    
    def get_url(self) -> str:
        return self.tweet_url
    
    def get_date(self) -> str:
        return self.tweet_date
    
    def get_text(self) -> str:
        return self.tweet_text
    
    def get_lang(self) -> str:
        return self.tweet_lang
    
    

    def __get_first_tweet(self) -> WebElement:
        max_consecutive_errors = 15
        consecutive_error_count = 0
        while True:
            try:
                tweet = self.driver.find_elements(
                    By.CSS_SELECTOR, "article[data-testid='tweet']")[self.Ad[0]]
                consecutive_error_count = 0
                
            except IndexError:
                consecutive_error_count += 1
                if consecutive_error_count > max_consecutive_errors:
                    return "stop"  
                sleep(0.5)
                continue
            return tweet
    
    
    def __remove_pinned(self):
        try:
            if self.tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="socialContext"]').get_attribute("innerText") == "Pinned":
                print("Skipping pinned...")
                raise TypeError
            
        except NoSuchElementException:
            pass


    def __get_tweet_url(self) -> (str, bool):
        urls_obj = self.tweet.find_elements(By.CSS_SELECTOR, "a")
        urls_list = [i.get_attribute("href") for i in urls_obj]
        if urls_list[1] != self.driver.current_url:
            url = urls_list[4]
            re_tweet = True
        else:
            url = urls_list[3]
            re_tweet = False

        return url, re_tweet


    def __get_tweet_date(self) -> str:
        # 2023-07-11T12:59:22.000Z
        try:
            date = self.tweet.find_element(
                By.CSS_SELECTOR, "time").get_attribute("datetime")[:10]
            date = datetime.strptime(date, '%Y-%m-%d')
        except NoSuchElementException:
            raise TypeError

        return date.strftime('%d/%m/%Y')


    def __get_tweet_text(self) -> str:
        try:
            element = self.tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")

            return element.get_attribute("innerText")
        except NoSuchElementException:
            return ""


    def __get_tweet_lang(self) -> str:
        try:
            element = self.tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")
            return element.get_attribute("lang")
        except NoSuchElementException:
            return ""
        
    # def check_media(self):
    #     try:
    #         self.tweet.find_element(By.XPATH, "./div/div/div[2]/div[2]/div[4]")
    #         media = True
    #     except NoSuchElementException:
    #         media = False

    #     return media
    
 

    def __delete_tweet(self):
        self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, self.tweet)
