import requests
import urllib.request
import time
from bs4 import BeautifulSoup

cookie = {'vlId': 'HERE_YOUR_VLID'}
url = input("What is the Videoland url?")
Season = input("Which season? (e.g. 3)")
Season = "{0:0=2d}".format(int(Season))
test = 0
Ep = 0
data = requests.get(url)
soup = BeautifulSoup(data.text, "html.parser")
title = soup.select('h1')[0].text.strip()
title = title.replace(" ",".")
print(title)
for link in soup.find_all("div", {"class": "episode"}):
    for link in link.find_all('a'):
        link = link.get('href')
        link = link.replace("/player/","")
        link = link.split("/")
        link = f"https://www.videoland.com/api/v3/subtitles/{link[0]}"
        print(link)
        Ep+=1
        Ep= "{0:0=2d}".format(Ep)
        filename = f"{title}.S{Season}E{Ep}.vtt"
        Ep= int(Ep)
        r = requests.get(link, cookies=cookie)
        open(filename, 'wb').write(r.content)


