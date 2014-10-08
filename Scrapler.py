'''
Created on 06/ott/2014

@author: Enrico Tedeschi
'''
import requests
import pymysql  

import sqlite3  #to create the database where to put all the data
from bs4 import BeautifulSoup

url = "http://www.paginegialle.it/pgol/4-idraulico/3-Milano%20%28MI%29"
r = requests.get(url)

#creating the db
db = sqlite3.connect("PagineGialle.sqlite")

cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS PagineGialle
     (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
     name TEXT NOT NULL,
     address TEXT,
     tel  TEXT)""" )    #create a new table only if it doesnt exists yet
db.commit()


#print r.content

soup = BeautifulSoup(r.content)
#print soup.prettify()

    
g_data = soup.findAll("div", {"class": "item_sx"}) #here is where I have all the informations I need

#high number range to avoid overflow, to improve with dynamic structure
name = range(10000)
address = range(10000)
telephone = range(10000)

i = 0
for item in g_data:
    name[i] = item.find("h2", {"class":"rgs"}).text
    address[i] = item.find("span", {"class":"street-address"}).text + " " + item.find("span", {"class":"locality"}).text
    telephone[i] = item.find("div", {"class":"tel"}).text
    
    cursor.execute("""INSERT INTO PagineGialle (name, address, tel) VALUES
                  (?, ?, ?)""", (name[i], address[i], telephone[i]) )
    
    db.commit()
    
    #just for test
    print name[i]
    print address[i]
    print telephone[i]
    print"\n\n"
    
    
    
db.close()  #close the connection to the database
