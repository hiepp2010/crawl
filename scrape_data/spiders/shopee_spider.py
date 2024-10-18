import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

import time
from selenium.webdriver.common.by import By
    
class ScrapingClubSpider(scrapy.Spider):
        name = "shopee"
    
        def start_requests(self):
            url = "https://shopee.vn/%E1%BB%90p-%C4%91i%E1%BB%87n-tho%E1%BA%A1i-m%E1%BB%9D-titan-Gold-AG-%C4%91%C6%B0%E1%BB%A3c-n%C3%A2ng-c%E1%BA%A5p-cho-IPhone-15-14-13-12-11-Pro-Max-Plus-V%E1%BB%8F-c%E1%BB%A9ng-V%E1%BB%8F-%E1%BB%91ng-k%C3%ADnh-th%E1%BB%A7y-tinh-Nano-vi%E1%BB%81n-m%E1%BA%A1-%C4%91i%E1%BB%87n-c%C3%B3-v%E1%BB%8F-%C4%91%C3%B3ng-g%C3%B3i-i.189448037.18686609371?sp_atk=2e3c04ef-b35a-4b05-8788-3d6a53e6ab4a&xptdk=2e3c04ef-b35a-4b05-8788-3d6a53e6ab4a"
            yield SeleniumRequest(url=url, callback=self.parse,wait_time=20)
    
        def parse(self, response):
            driver = response.request.meta["driver"]
            driver.set_window_size(1920,1080)
            driver.save_screenshot("screenshot_10.png")
            
            time.sleep(5)
            
            ActionChains(driver) \
                    .scroll_by_amount(0, 10000) \
                    .perform()
            
            driver.save_screenshot("screenshot_20.png")
            # driver = response.request.meta["driver"]
            # wait = WebDriverWait(driver)
            # scroll to the end of the page 10 times
            # for x in range(0, 10):
            #     # scroll down by 10000 pixels
            #     # ActionChains(driver) \
            #     #     .scroll_by_amount(0, 10000) \
            #     #     .perform()
    
            #     # waiting 2 seconds for the products to load
            #     time.sleep(2)
                
            #     # driver.find_element(By.CSS_SELECTOR,".image-carousel__item").click()
                
            #     time.sleep(2)
            
    
            # select all product elements and iterate over them
            # for product in driver.find_elements(By.CSS_SELECTOR, ".image-carousel__item"):
            #     # scrape the desired data from each product
            #     # url = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            #     # image = product.find_element(By.CSS_SELECTOR, ".card-img-top").get_attribute("src")
            #     # name = product.find_element(By.CSS_SELECTOR, "h4 a").text
            #     # price = product.find_element(By.CSS_SELECTOR, "h5").text
    
            #     # add the data to the list of scraped items
            #     yield {
            #         # "url": url,
            #         # "image": image,
            #         # "name": name,
            #         # "price": price
            #         "price":product.text
            #     }
