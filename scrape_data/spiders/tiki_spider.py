import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

import time
from selenium.webdriver.common.by import By


class ScrapingClubSpider(scrapy.Spider):
        name = "tiki"

        cnt = 1

        def start_requests(self):
            url = "https://tiki.vn/payback-time-ngay-doi-no-p3608625.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.294590_Y.1876910_Z.3959479_CN.Product-Ads-21%2F06%2F2024-%2F-NGAY-%C4%90OI-NO&itm_medium=CPC&itm_source=tiki-ads&spid=3679503"
            yield SeleniumRequest(url=url, callback=self.parseProduct)
            
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

            while True:
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
                time.sleep(1)
                yield SeleniumRequest(url=url_product, callback=self.parseProduct)

        def parseProduct(self, response):
            driver = response.request.meta["driver"]
            product={}


            driver.set_window_position(0,0)
            driver.set_window_size(1920,1080)
            driver.save_screenshot("tiki1.png")
            ActionChains(driver).scroll_by_amount(0,1000).perform()

            try:
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.SellerName__SellerNameStyled-sc-5d1cxl-0")))
                product["seller_name"] = driver.find_element(By.CSS_SELECTOR,"div.SellerName__SellerNameStyled-sc-5d1cxl-0").text
                product["seller_url"] = driver.find_element(By.CSS_SELECTOR,"div.SellerName__SellerNameStyled-sc-5d1cxl-0 a").get_attribute("href")

            except:
                pass
            
            driver.save_screenshot("tiki2.png")
            ActionChains(driver).scroll_by_amount(0,1000).perform()
            try:
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".HighlightInfo__HighlightInfoContentStyled-sc-1pr13u3-0")))
            except: 
                pass
    
            driver.save_screenshot("tiki3.png")
            ActionChains(driver).scroll_by_amount(0,1000).perform()

            try: 
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".ToggleContent__Wrapper-sc-fbuwol-1")))
            except:
                pass
            
            driver.save_screenshot("tiki4.png")
            ActionChains(driver).scroll_by_amount(0,1000).perform()
            
          
            code_lines=[
                "product[\"product_name\"] = driver.find_element(By.CSS_SELECTOR,\".Title__TitledStyled-sc-c64ni5-0\").text",
                "product[\"product_url\"] = driver.current_url",

                "product[\"current_price\"] = driver.find_element(By.CSS_SELECTOR,\".product-price__current-price\").text",
                "product[\"discount_rate\"] = driver.find_element(By.CSS_SELECTOR,\".product-price__discount-rate\").text",
                "product[\"original_price\"] = driver.find_element(By.CSS_SELECTOR,\".product-price__original-price\").text",
                
                "product[\"avg_rating\"] = driver.find_element(By.CSS_SELECTOR,\".styles__RatingStyled-sc-1onuk2l-0 div[style=\"margin-right:4px;font-size:14px;line-height:150%;font-weight:500\"]\").text",
                "product[\"number_solds\"] = driver.find_element(By.CSS_SELECTOR,\".styles__RatingStyled-sc-1onuk2l-0 .styles__StyledQuantitySold-sc-1onuk2l-3\").text",
                "product[\"number_reviews\"] = driver.find_element(By.CSS_SELECTOR,\".styles__RatingStyled-sc-1onuk2l-0 .number\").text",
            
                "product[\"brand_name\"] = driver.find_element(By.CSS_SELECTOR,\"h6 a\").text",
                "product[\"brand_url\"] = driver.find_element(By.CSS_SELECTOR,\"h6 a\").get_attribute(\"href\")",
                
                "product[\"detail\"] = driver.find_element(By.CSS_SELECTOR,\".WidgetTitle__WidgetContentRowStyled-sc-12sadap-3\").text",
            ]
            
            for line in code_lines:
                try:
                    exec(line)
                except Exception as e:
                    print("error"+line)
                    print(e)
                    
            product["product_imgs"]=[]
            try:
                product_imgs=driver.find_elements(By.CSS_SELECTOR,".thumbnail-list div.content span.slider picture.webpimg-container img")
                
                for img in product_imgs:
                     product["product_imgs"].append(img.get_attribute("src"))
            
            except:
                pass
                 
           
            product["feature"] = []
            try: 
                hightlights=driver.find_elements(By.CSS_SELECTOR,".HighlightInfo__HighlightInfoContentStyled-sc-1pr13u3-0")
            
                for hightlight in hightlights:
                    product["feature"].append(hightlight.text)
            except:
                pass
            
            product["category"]= []
            try:    
                categories=driver.find_elements(By.CSS_SELECTOR,".breadcrumb-item")
        
                for category in categories:
                    product["category"].append(category.text)
            except:
                pass
            
            try:
                button_more = driver.find_element(By.CSS_SELECTOR,".btn-more")
                button_more.click()
            except:
                pass
            
            try:
                descripts = driver.find_element(By.CSS_SELECTOR,".ToggleContent__View-sc-fbuwol-0")
                product["description"]=descripts.text
                print(descripts.text)
            except:
                pass
            
            product["detail"]=[]
            try:
                details=driver.find_elements(By.CSS_SELECTOR,"div[style=\"display: grid; grid-template-columns: 55% 45%; gap: 4px;\"].WidgetTitle__WidgetContentRowStyled-sc-12sadap-3")
                for detail in details:
                    product["detail"].append(detail.text)
            except:
                pass
                
            driver.save_screenshot("tiki5.png")
            ActionChains(driver).scroll_by_amount(0,1000).perform()
            try:
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".customer-reviews__pagination li a.next")))
            except:
                pass
            driver.save_screenshot("tiki6.png")



            review_list_table=[]
            while True:
                
                try:
                    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".customer-reviews__pagination li a.next")))
                except:
                    pass
                
                try:
                    review_list = driver.find_elements(By.CSS_SELECTOR,".review-comment")
                    
                    for review in review_list:
                        review_table=[]
                        try:
                            show_more_button = review.find_element(By.CSS_SELECTOR,".show-more-content")
                            show_more_button.click()
                        except Exception as e:
                            print(e)
                        
                        try:
                            review_table.append(review.find_element(By.CSS_SELECTOR,".review-comment__rating").get_attribute("innerHTML"))
                        except Exception as e :
                            print(e)
                            review_table.append("")
                        
                        try:
                            review_table.append(review.find_element(By.CSS_SELECTOR,".review-comment__content").text)
                        except Exception as e :
                            print(e)
                            review_table.append("")
                        
                        review_img=[]
                        try:
                            imgs = review.find_elements(By.CSS_SELECTOR,".review-comment__image")
                            for img in imgs:
                                review_img.append(img.get_attribute("style"))
                            review_table.append(review_img)
                        except :
                            review_table.append([])
                        
                        review_list_table.append(review_table)
                        
                except:
                    pass 
                
                
                try:
                    next_comment_button = driver.find_element(By.CSS_SELECTOR,".customer-reviews__pagination li a.next")
                    next_comment_button.click()
                except Exception as e:
                    print("button err")
                    print(e)
                    # product["review"]=review_list_table
                    break 
            yield{
                "product_name":product.get("product_name",""),
                "product_url":product.get("product_url",""),
                
                "avg_rating":product.get("avg_rating"),
                "number_sold":product.get("number_solds"),
                "number_reviews":product.get("number_reviews"),
                
                "product_imgs":product.get("product_imgs"),
                
                "current_price":product.get("current_price",""),
                "discount_rate":product.get("discount_rate",""),
                "original_price":product.get("original_price",""),
                
                "brand_name":product.get("brand_name",""),
                "brand_url":product.get("brand_url",""),
                
                "seller_name":product.get("seller_name",""),
                "seller_url":product.get("seller_url",""),
                
                "review":len(review_list_table),
                
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
                
            
