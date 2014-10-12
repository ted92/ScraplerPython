'''
Created on 06/ott/2014

@author: Enrico Tedeschi
'''
import requests
import pymysql  
import urlparse

import sqlite3  #to create the database where to put all the data
from bs4 import BeautifulSoup


#TODO:
    #put in urls variable all the link pages, took from <a class = "num active"> or "num"
    #create a visited variable for the web pages already visited
    #both variables, urls and visited have to be a stack variable

url = "http://www.paginegialle.it/pgol/4-idraulico/3-Milano%20(MI)" #START URL
r = requests.get(url)
soup = BeautifulSoup(r.content)

#creating the db
db = sqlite3.connect("PagineGialle.sqlite")
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS PagineGialle
                        (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        address TEXT,
                        tel  TEXT)""" )    #create a new table only if it doesnt exists yet
db.commit()

all_pages = []  #all the links to all the pages
for tag in soup.findAll("a", {"class":"num"}, href=True):
    tag['href'] = urlparse.urljoin(url,tag['href'])     #get the entire URL
    all_pages.append(tag['href'])   #I have here all the pages to visit
    print tag['href']

while len(all_pages)>0:
    try:
        url=all_pages.pop()
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        
        g_data = soup.findAll("div", {"class": "item_sx"}) #here is where I have all the informations I need
        for item in g_data:
            name = item.find("h2", {"class":"rgs"}).text
            if (item.find("span", {"class":"street-address"}) !=  None or (item.find("span", {"class":"locality"})) != None):
                address = item.find("span", {"class":"street-address"}).text + " " + item.find("span", {"class":"locality"}).text
            else:
                address = None
  
            if (item.find("div", {"class":"tel"}) != None):
                telephone = item.find("div", {"class":"tel"}).text
            else:
                telephone = None
           
            cursor.execute("""INSERT INTO PagineGialle (name, address, tel) VALUES
                  (?, ?, ?)""", (name, address, telephone) )
            db.commit()
    
            #test
            #print name
            #print address
            #print telephone
            #print"\n\n"
    except:
        print 'find None exception'

db.close()  #close the connection to the database
#print all_pages
