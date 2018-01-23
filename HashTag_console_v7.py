#V8 - Fullworking Verions if there are enough posts
#V9 - This will not break if the user asks for more posts than available. 
#Still need to test v9


import ssl
import csv
import os 
import requests 
import urllib
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from  bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import time

def get_posts(tag, user_count):
	
	'''Getting html of page to be scrape for
	hrefs that will get me the user names'''

	print("getting page")
	url = "https://www.instagram.com/explore/tags/" + tag + "/"
	try:
		driver = webdriver.PhantomJS()
		driver.get(url)
		print("successfully requested site")
	except:
		print("Unable to reach site")
		quit()
	
	'''Loading Page until we have enough posts'''
	soup = BeautifulSoup(driver.page_source, 'lxml')
	try:
		posts = soup.find_all("div", class_ = ["_mck9w","_gvoze","_f2mse"])
	except:
		#print("No links found")
		quit()

	post_count = len(posts)
	tabdown(driver, 22) #This is the number of tabs needed to hit the load more button
	SCROLL_PAUSE_TIME = 2
	
	#Get Scroll Height
	last_height = driver.execute_script("return document.body.scrollHeight")
	
	while post_count < user_count:
		print("going to scroll")
		try:
			#Scroll to bottom of page
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			#Wait to load page
			time.sleep(SCROLL_PAUSE_TIME)

		except: 
			print("User asks for more posts than currently found, only retrieve: ", len(posts))
			return [posts, len(posts)]
			
		soup = BeautifulSoup(driver.page_source, 'lxml')
		posts = soup.find_all("div", class_ = ["_mck9w","_gvoze","_f2mse"])
		post_count = len(posts)
		print("len of posts: ", post_count)
		time.sleep(5)

	print("Length of posts: ",(len(posts)))
	
	#print(len(posts))
	#print(type(posts))
	print("All Done")
	driver.close()
	return [posts, user_count]

def tabdown(driver, num):
	actions = ActionChains(driver)
	for i in range(num):
		actions = actions.send_keys(Keys.TAB)
	actions.perform()
	time.sleep(3)
	load_button = driver.find_element_by_link_text("Load more")
	load_button.send_keys(Keys.ENTER)
	time.sleep(3)
		

def get_href(html_posts):
	'''Creating list of hrefs from html retrieved from the tags page'''
	
	print('Getting hrefs from the posts')
	href_list = list()
	soup = BeautifulSoup(str(html_posts), 'html.parser')
	try:
		hrefs = soup.find_all('a', href=True)
	except:
		print("No hyperlinks found")
		quit()

	for a in hrefs:
		href_list.append(a['href'])
	
	print(len(href_list))
	print(type(href_list))
	print("Done getting posts")
	return(href_list)


def get_user_info(href_from_posts, set_count, hash_tag):
	'''looping through list to get usersname'''
	
	user_list = list()

	counts = 0
	for ref in href_from_posts:
		user_account = list()
		if counts < set_count:
			#Connecting to photo's page
			ref_link = ref.split('?tagged')
			user_link = ref_link[0]
			full_link = 'https://www.instagram.com' + user_link
			print('Searching full_link')
			print("Current Count: ", counts)
			try:
				driver = webdriver.PhantomJS()
				driver.get(full_link)
			except:
				print("Link does not work")
				continue

			#Get username
			try:
				username = get_username(driver)
				print("username: ", username)
				user_account.append(username)				 
			except:
				username = "No user name found"
				user_account.append(username)
				print("Could not find username")
				pass
			
			#Get postDate
			try: 
				postDate = get_postDate(driver)
				print("PostDate: ", postDate)
				user_account.append(postDate)
			except:
				postDate = "No post date found"
				user_account.append(postDate)
				print("Could not find post date")
				pass

			#Get number of followers
			try:
				followers = get_followers(username)
				print("Followers: ", followers)
				user_account.append(followers)
			except:
				followers = "No followers found"
				user_account.append(followers)
				print("Could not find followers")
				pass

			user_account.append(hash_tag)
			
			user_list.append(user_account)
			driver.close()
			counts += 1
		else:
			print(user_list)
			return user_list


def save_to_file(my_list, tag):
	print(my_list)
	now = datetime.datetime.now()
	current_date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
	with open(current_date + "_" + tag + ".txt", "w+") as fname:
		for account in my_list:
			print("account: ", account)
			for i in account:
				fname.write('"' + i + '"' + ',')
			fname.write('\n')
		fname.close()

def get_username(driver):
	'''Get username from html'''
	soup = BeautifulSoup(driver.page_source, 'lxml')
	username = soup.find('a', class_=['_2g7d5', 'notranslate', '_iadoq']).getText()
	#print(username)
	return username

def get_postDate(driver):
	'''Get Post Date from html'''
	soup = BeautifulSoup(driver.page_source, 'lxml')
	#print(soup.prettify)
	postDate = soup.find('time', class_=['_p29ma','_6g6t5'])
	postDate = postDate.get('title')
	#print(postDate)
	return postDate

def get_followers(username):
	'''Getting the number of followers from the user's page'''

	#Connecting to user's page
	user_page = "https://www.instagram.com/"+username+"/"
	try:
		driver = webdriver.PhantomJS()
		driver.get(user_page)
		print("successfully requested site")
	except:
		print("Unable to reach site")
		followers = "No followers found"
		return followers

	#Find User Stats
	soup = BeautifulSoup(driver.page_source, 'lxml')  
	user_stats = soup.find_all('span', class_=["_fd86t", "_he56w"])
	driver.close()
	
	#Get Followers from user stats
	followers_info = str(user_stats[1])

	soup = BeautifulSoup(followers_info, "lxml")
	followers = soup.find('span', class_=['_fd86t', '_he56w']).getText()
	return followers
	
def HashTag():
		
	print("This is version 9")
	user_tag = input("Input Tag (exclude the #):" )
	user_count = input("How many users would you like: ")
	try:
		user_count = int(user_count)
	except:
		print("Count input must be a numeric value")
		quit()

	get_posts_returnValue = get_posts(user_tag, user_count)
	posts = get_posts_returnValue[0]
	user_count = get_posts_returnValue[1] - 1 #because the function count starts at 0
	print("user_count in HashTag function: ", user_count)
	href_posts = get_href(posts)
	users = get_user_info(href_posts, user_count, user_tag)
	save_to_file(users, user_tag)
	print("All done, check you folder for the .csv")

if __name__=="__main__":
	HashTag()
	#get_followers("mws575") 

