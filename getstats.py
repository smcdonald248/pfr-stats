'''
getstats.py

scrapes tables from pro-football-reference.com

12/11/2019 -- Progress so far:
url scraping and BS4 parsing in place -- can find headers, data and commit them to python lists for simpler manipulation.

High Level things To Do:
list of urls to scrape... more testing...
database loading
analysis

'''

import urllib.request, urllib.parse, urllib.response
import sqlite3
import ssl
from bs4 import BeautifulSoup
from time import sleep

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter URL: ")
if len(url) < 1:
    url = "https://www.pro-football-reference.com/years/2019/opp.htm"

html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

tr_soup = soup.findAll('tr')
tbody_soup = soup.findAll('tbody')

column_headers = list() 
data = list()

for th in tr_soup[1].findAll('th'):
    column_headers.append(th.getText())

for tr in tbody_soup[0].findAll('tr'):
    temp = list()
    temp.append(tr.find('th').getText())
    for td in tr.findAll('td'):
        temp.append(td.getText())
    data.append(temp)

print(column_headers)
for i in data:
    print(i)    