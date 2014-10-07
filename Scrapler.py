'''
Created on 06/ott/2014

@author: Enrico Tedeschi
'''
import requests


from bs4 import BeautifulSoup   #using BeautifulSoup4

url = "http://www.paginegialle.it/pgol/4-idraulico/3-Milano%20%28MI%29"   #given url
r = requests.get(url)


soup = BeautifulSoup(r.content)   #object soup in soup variable

    
g_data = soup.findAll("div", {"class": "item_sx"})    #here is where I have all the informations I need

name = range(10000)     #high random number, not relevant
address = range(10000)
i = 0
for item in g_data:
    #print item.contents[1].text
    name[i] = item.find("h2", {"class":"rgs"}).text     #the names are in <h2 class="rgs">
    
    #the address is a composed string from two <span> HTML tags
    address[i] = item.find("span", {"class":"street-address"}).text + " " + item.find("span", {"class":"locality"}).text
    print name[i]
    print address[i]
    print"\n\n"
