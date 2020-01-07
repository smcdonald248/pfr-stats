'''
getstats.py

scrapes tables from pro-football-reference.com

12/11/2019 -- Progress so far:
url scraping and BS4 parsing in place -- can find headers, data and commit them to python lists for simpler manipulation.

1/7/2020
Database loading for 'Advanced Passing' table complete
Data sanity checks to allow for sqlite data loading (header rows cleaned out, etc.)
Analysis moved to statsbasic.py to finish out UofM coursework

Roadmap / Ideas:
Config file -- list of urls to scrape with table name tuple (e.g. url, table_name) 
    - More testing required to ensure that dynamic table creation will not barf when using different tables
Class/Def creation -- make this more usable


'''

import urllib.request, urllib.parse, urllib.response
import sqlite3
import ssl
from bs4 import BeautifulSoup
from time import sleep

conn = sqlite3.connect('stats.sqlite')
cur = conn.cursor()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter URL: ")
if len(url) < 1:
    url = "https://www.pro-football-reference.com/years/2019/passing_advanced.htm"

table = input("Enter Table Name: ")
if len(table) < 1:
    table = "Passing"

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

cur.execute('DROP TABLE IF EXISTS ' + table + ';')

x = 0
col = ''
for i in column_headers:
    if x == 0:
        cur.execute('CREATE TABLE ' + table + '( id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE );')
        try:
            cur.execute('ALTER TABLE ' + table + ' ADD COLUMN ' + i + ' REAL;')
        except:
            cur.execute('ALTER TABLE ' + table + ' ADD COLUMN ' + i + ';')
        col = col + i + ','
        x =+ 1
    else:
        if i.find('/') != -1:
            i = i.replace('/', '')
        try:
            cur.execute('ALTER TABLE ' + table + ' ADD COLUMN ' + i + ' REAL;')
        except:
            cur.execute('ALTER TABLE ' + table + ' ADD COLUMN ' + i + ';')
        col = col + i + ','

col = col[:-1]
conn.commit()

x = 0
fields = ''
while x < len(data[x]): 
    fields = fields + '?,' 
    x += 1
fields = fields[:-1]

y = 0
for i in data:    
    x = 0
    values = ''
    while x < len(data[y]): 
        values = values + '\'' + data[y][x] + '\'' + ','
        x += 1
    values = values[:-1]
    
    check = values.split(',')
    if len(check) < len(data[0]):
        y += 1
        continue
    else:        
        cur.execute('INSERT INTO ' + table + '(' + col + ') Values ( ' + fields + ')', ( eval(values) ))
        y += 1

print('Done! ' + str(y) + ' records poplated into ' + table)

conn.commit()
cur.close()
