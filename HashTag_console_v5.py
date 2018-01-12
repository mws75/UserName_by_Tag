#Version 5 - Full Working Version - For Console - See v6 for Flask


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
        driver = webdriver.Chrome()
        driver.get(url)
        print("successfully requested site")
    except:
        print("Unable to reach site")
        quit()
    
    '''Loading Page untile we have enough posts'''
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        posts = soup.find_all("div", class_ = ["_mck9w","_gvoze","_f2mse"])
    except:
        print("No links found")
        quit()

    post_count = len(posts)
    
    while post_count < user_count:
        try:
            '''first tab down the page 22 tabs at a time
            This causes it to hit the load button'''
            
            actions = ActionChains(driver)
            for i in range(22):
                actions = actions.send_keys(Keys.TAB)
                #time.sleep(0.5)
            actions.perform()
            time.sleep(3)

            load_button = driver.find_element_by_link_text("Load more")
            load_button.send_keys(Keys.ENTER)
            time.sleep(3)

        except: 
            print("User asks for more posts than currently found")
            return posts
            
        soup = BeautifulSoup(driver.page_source, 'lxml')
        posts = soup.find_all("div", class_ = ["_mck9w","_gvoze","_f2mse"])
        post_count = len(posts)
        print("len of posts: ", post_count)
        time.sleep(3)

    print("Length of posts: ",(len(posts)))
    
    print(len(posts))
    print(type(posts))
    print("All Done")
    driver.close()
    return posts



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


def get_username(href_from_posts, set_count=5):
    '''looping through list to get usersname'''
    username_list = list()
    counts = 0
    for ref in href_from_posts:
        if counts < set_count:
            ref_link = ref.split('?tagged')
            user_link = ref_link[0]
            full_link = 'https://www.instagram.com' + user_link
            print('Searching full_link')
           
            try:
                driver = webdriver.Chrome()
                driver.get(full_link)
            except:
                print("Link does not work")
                continue
           
            soup = BeautifulSoup(driver.page_source, 'lxml')            
            try:
                username = soup.find('a', class_=['_2g7d5','notranslate','_iadoq']).getText()
                driver.close()
                print(username)
                username_list.append(username)
                counts += 1
            except:
                print("Username not found")
                driver.close()
                counts += 1
                continue

        else:
            usernames_final = pd.unique(username_list).tolist()
            print(usernames_final)
            return usernames_final
'''
def count_users(page):
    #count the number of posts on the page
    #if < counts requested, scroll, else, move on
'''


def save_to_file(my_list, tag):
    now = datetime.datetime.now()
    current_date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    with open(current_date + "_" + tag + ".txt", "w") as fname:
        for item in my_list:
            fname.write(item + '\n')
        fname.close()

		
def main():
		
	print("This is version 5")
	user_tag = input("Input Tag (exclude the #):" )
	user_count = input("How many users would you like (count < 21): ")
	try:
		user_count = int(user_count)
	except:
		print("Count input must be a numeric value")
		quit()

	posts = get_posts(user_tag, user_count)
	href_posts = get_href(posts)
	users = get_username(href_posts, user_count)
	save_to_file(users, user_tag)
	print("All done, check you folder for the .csv")

if __name__=="__main__":
	main()
