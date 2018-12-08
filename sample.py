# coding: utf-8
# Twitter Webにログインしてツイートしてみる
# seleniumの練習
from selenium import webdriver

def post_twitter( user_name, password):
	browser = webdriver.Firefox()
	browser.get("https://twitter.com/")

	# ログイン処理
	mail = browser.find_element_by_class('js-username-field email-input js-initial-focus')
	pass_wd = browser.find_element_by_class('js-password-field')
	mail.send_keys(user_name)
	pass_wd.send_keys(password)
	pass_wd.submit()

	# ツイートの処理
	from datetime import datetime
	post_body = browser.find_element_by_id("tweet-box-home-timeline")
	post_body.send_keys("test: "+datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	try:
		post_button = browser.find_element_by_css_selector("button.tweet-action")
		post_button.click()
		print("ツイート成功")
		# この時点で、他の操作をするとなんだか失敗するみたい。
	except:
		print("ツイート失敗")

	browser.close()

if __name__ == "__main__":
	from getpass import getpass
	name = input("user name : ")
	pw = getpass("password  : ")
	post_twitter( name, pw)
