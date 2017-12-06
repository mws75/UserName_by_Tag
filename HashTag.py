from  bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import csv
import os 
import requests 
import urllib
import pandas as pd
from selenium import webdriver


def get_posts(tag):
    
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

    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        posts = soup.find_all("div", class_ = ["_mck9w","_gvoze","_f2mse"])
    except:
        print("No links found")
        quit()
    
    print(len(posts))
    print(type(posts))
    print("All Done")
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
            print('Full link: ', full_link)
           
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
print("This is version 3")
user_tag = input("Input Tag (exclude the #):" )
user_count = input("How many users would you like (count < 21): ")
try:
    user_count = int(user_count)
except:
    print("Count input must be a numeric value")
    quit()
posts = get_posts(user_tag)
href_posts = get_href(posts)
get_username(href_posts, user_count)

