from  bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import csv
import os 
import time
from selenium import webdriver
"""try connecting to the site in a different way"""
def get_url_html_myWay(my_tag):
    print("myWay")
    url = create_url(my_tag)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    print("Connecting to site...")
    html = urllib.request.urlopen(url, context=ctx).read()
    print(html)
    return(html)


def get_url_html_DBWay(my_tag):
     import bs4
     from bs4 import BeautifulSoup as soup
     from urllib.request import urlopen as uReq
     
     print("DBWay")

     url = create_url(my_tag)

     uClient = uReq(url)
     page_html = uClient.read()
     uClient.close()

     page_soup = soup(page_html, 'html.parser')
     span_content = page_soup.find_all("span", {'class':'_mck9w'})
     print(span_content)
     return str(span_content)

def get_url_html_SWay(my_tag):
    import requests
    from bs4 import BeautifulSoup

    print("SWay")

    url = create_url(my_tag)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    span = soup.find_all("div", class_ = ["_mck9w","_gvoze","_f2mse"])
    print(span)
    return str(span).encode(encoding='utf-8', errors='ignore')

def get_url_webDriverWay(my_tag):
    print('WebDriverWay')
    '''Getting html of page to be scrape for
    hrefs that will get me the user names'''

    print("getting page")
    url = create_url(my_tag)
    print(url)
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        print("successfully requested site")
    except:
        print("Unable to reach site")
        time.sleep(500)
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
    print(posts)
    return str(posts)

def prettyfy(html, tag, test):
    
    soup = BeautifulSoup(html, 'html.parser')
    pretty_html = BeautifulSoup.prettify(soup)
    #print(pretty_html)
    pretty_html_by_line = pretty_html.split('\n')
    with open(os.path.abspath(os.path.dirname(__file__)) + "\\Users_" + tag + '_'+ test + ".txt", "w") as file: 
        for line in pretty_html_by_line:
            try:
                file.write(line + '\n')
            except:
                continue
        file.close()

def create_url(hashTag):
    create_url = url = "https://www.instagram.com/explore/tags/" + hashTag + "/"
    return create_url

myWay = get_url_html_myWay('nycwinter')
prettyfy(myWay, 'nycwinter' ,'myWay')
print("myWay success")
DBWay = get_url_html_DBWay('nycwinter')
prettyfy(DBWay, 'nycwinter', 'DBWay')
print("DBWay Success")
SWay = get_url_html_SWay('nycwinter')
prettyfy(SWay, 'nycwinter', 'SWay')
print("SWay Success")
WebDriverWay = get_url_webDriverWay('nycwinter')
prettyfy(WebDriverWay, 'nycwinter', 'WebDriverWay')
print('WebDriverWay Success')