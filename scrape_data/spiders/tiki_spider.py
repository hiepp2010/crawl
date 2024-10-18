import scrapy
import random
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By

class ScrapingClubSpider(scrapy.Spider):
        name = "tiki"

        cnt = 1

        def start_requests(self):
            url = "https://tiki.vn/chuot-khong-day-hxsj-m107-wireless-2-4ghz-sac-pin-chong-on-dip1600-chuyen-dung-cho-may-tinh-laptop-tivi-hang-chinh-hang-p116566083.html?spid=116566087"
            yield SeleniumRequest(url=url, callback=self.parseProduct,wait_time=2)

        def parse(self, response):
            driver = response.request.meta["driver"]

            category_list = driver.find_elements(
                By.CSS_SELECTOR, ".styles__StyledItemV2-sc-oho8ay-1")

            url_categories = []
            for category in category_list:
                url_categories.append(category.find_element(
                    By.CSS_SELECTOR, "a").get_attribute("href"))

            for url_category in url_categories:
                time.sleep(2)
                yield SeleniumRequest(url=url_category, callback=self.parseCategory)

        def parseCategory(self, response):
            driver = response.request.meta["driver"]


            # continue to show more product until the button is not displayed
            while True:
                # scroll down by 10000 pixels
                # ActionChains(driver) \
                #     .scroll_by_amount(0, 10000) \
                #     .perform()

                time.sleep(1)

                try:
                    show_button = driver.find_element(By.CSS_SELECTOR,".styles__Button-sc-143954l-1")
                except NoSuchElementException:
                    break
                    
                show_button.click()
            
            url_products = []
            
            product_list = driver.find_elements(By.CSS_SELECTOR,".styles__ProductItemContainerStyled-sc-bszvl7-0 ")
            
            for product in product_list:
                url_products.append(product.find_element(By.CSS_SELECTOR,"a").get_attribute("href"))
                
            for url_product in url_products:
                time.sleep(0.5)
                yield SeleniumRequest(url=url_product, callback=self.parseProduct)

            # # select all product elements and iterate over them
            # for product in driver.find_elements(By.CSS_SELECTOR, ".price-discount__price"):
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
            #         "price": product.text
            #     }
        def parseProduct(self,response):
            driver = response.request.meta["driver"]
            time.sleep(2)
            ActionChains(driver).scroll_by_amount(0, 10000).perform()
            product={}
            driver.save_screenshot("tiki.png")
            code_lines=[
                "product[\"product_name\"] = driver.find_element(By.CSS_SELECTOR,\".Title__TitledStyled-sc-c64ni5-0\").text",
                "product[\"product_url\"] = driver.current_url",

                "product[\"current_price\"] = driver.find_element(By.CSS_SELECTOR,\".product-price__current-price\").text",
                "product[\"discount_rate\"] = driver.find_element(By.CSS_SELECTOR,\".product-price__discount-rate\").text",
                "product[\"original_price\"] = driver.find_element(By.CSS_SELECTOR,\".product-price__original-price\").text",
            
                "product[\"brand_name\"] = driver.find_element(By.CSS_SELECTOR,\"h6 a\").text",
                "product[\"brand_url\"] = driver.find_element(By.CSS_SELECTOR,\"h6 a\").get_attribute(\"href\")",
            
                "product[\"seller_name\"] = driver.find_element(By.CSS_SELECTOR,\"div.SellerName__SellerNameStyled-sc-5d1cxl-0 a span\").text",
                "product[\"seller_url\"] = driver.find_element(By.CSS_SELECTOR,\"div.SellerName__SellerNameStyled-sc-5d1cxl-0 a\").get_attribute(\"href\")",
                
                "product[\"feature\"] = driver.find_elements(By.CSS_SELECTOR,\".HighlightInfo__HighlightInfoContentStyled-sc-1pr13u3-0\")",
                "product[\"category\"] = driver.find_elements(By.CSS_SELECTOR,\".breadcrumb-item\")",
                "product[\"detail\"] = driver.find_elements(By.CSS_SELECTOR,\".WidgetTitle__WidgetContentRowStyled-sc-12sadap-3\")",
                "product[\"description\"] = driver.find_element(By.CSS_SELECTOR,\".ToggleContent__View-sc-fbuwol-0\")"
                
            ]
            
            for line in code_lines:
                try:
                    exec(line)
                except Exception as e:
                    print("error"+line)
                    print(e)
            
            while True:
                review_list_table=[]
                try:
                    review_table=[]
                    review_list = driver.find_elements(By.CSS_SELECTOR,".review-comment")
                    for review in review_list:
                        review_table=[]
                        try:
                            review_table.append(review.find_element(".review-comment__rating"))
                        except NoSuchElementException:
                            review_table.append("")
                        
                        try:
                            review_table.append(review.find_element(".review-comment__content"))
                        except NoSuchElementException:
                            review_table.append("")
                        
                        try:
                            review_table.append(review.find_elements(".review-comment_images").get_attribute("style"))
                        except NoSuchElementException:
                            review_table.append("")
                        
                        review_list_table.append(review_table)
                               
                except:
                    pass 
                
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR,"a.next svg[color=\"#38383D\"]")
                    next_comment_button = driver.find_element(By.CSS_SELECTOR,"a.next")
                except NoSuchElementException:
                    product["review"]=review_list_table
                    break 
                next_comment_button.click()
            yield{
                # "price":response.css(".product-price__current-price").get()
                "product_name":product.get("product_name",""),
                "product_url":product.get("product_url",""),
                
                "current_price":product.get("current_price",""),
                "discount_rate":product.get("discount_rate",""),
                "original_price":product.get("original_price",""),
                
                "brand_name":product.get("brand_name",""),
                "brand_url":product.get("brand_url",""),
                
                "seller_name":product.get("seller_name",""),
                "seller_url":product.get("seller_url",""),
                
                "review":product.get("review",""),
                
                "feature":product.get("feature",""),
                "category":product.get("category",""),
                "detail":product.get("detail",""),
                "description":product.get("description","")
               
            }
            # try:
            #     brand = driver.find_element(By.CSS_SELECTOR,".brand-and-author ")
            # try:
            #     product_name = driver.find_element(By.CSS_SELECTOR,".styles__Button-sc-143954l-1").text
            #     product["product_name"] = product_name 
            # except: 
            #     logging.info("No product name")
                
            # try:
            #     product_
                
            
