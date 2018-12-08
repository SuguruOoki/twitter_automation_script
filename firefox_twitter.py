from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://twitter.com/login')

username = driver.find_element_by_css_selector(".js-username-field.email-input.js-initial-focus")
username.send_keys("yuu.work.network@gmail.com")

password = driver.find_element_by_class_name("js-password-field")
password.send_keys("admw8745@")

password.send_keys(Keys.RETURN)

# ツイートの処理
from datetime import datetime
Thread.sleep(5000);
post_body = driver.find_element_by_id("tweet-box-home-timeline")
print("post_body")
post_body.send_keys("test: "+datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
print("send_keys")
try:
    post_button = driver.find_element_by_css_selector(".button-text.tweeting-text")
    post_button.click()
    print("ツイート成功")
    # この時点で、他の操作をするとなんだか失敗するみたい。
except:
    print("ツイート失敗")

driver.quit()
