import requests
import urllib.request
import time
from bs4 import BeautifulSoup

cookie = {'vlId': 'YOUR vlId HERE'}


url = input("Wat is de Videoland url?")
if "/films/" in url:
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    title = soup.select('h1')[0].text.strip()
    title = title.replace(" ",".")
    x = url.split("/")
    movie_info = []
    for link in soup.find_all("ul", {"class": "detail-title__overview"}):
        for info in link.find_all('li'):
            movie_info.append(info.text)
    year = movie_info[0]
    print(year)
    filename = f"{title}.({year}).vtt"
    link = f"https://www.videoland.com/api/v3/subtitles/{x[4]}"
    r = requests.get(link, cookies=cookie)
    if r.status_code == 404:
        print("Sorry, er is geen ondertiteling gevonden voor deze aflevering")
    else:
        print(f"{filename} aan het downloaden")
        open(filename, 'wb').write(r.content)

elif "/series/" in url:
    
    Season2 = input("Welk seizoen? (bv. 3)")
    Season = "{0:0=2d}".format(int(Season2))
    Ep = 0
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    title = soup.select('h1')[0].text.strip()
    title = title.replace(" ",".")
    for link in soup.find_all("a"):
        text= link.text
        text = text.replace("Seizoen ","")
        if text == Season2:
            url = "https://www.videoland.com/"+link.get('href')
            data = requests.get(url)
            soup = BeautifulSoup(data.text, "html.parser")
            for link in soup.find_all("div", {"class": "episode"}):  
                for link in link.find_all('a'):
                    link = link.get('href')
                    link = link.replace("/player/","")
                    link = link.split("/")
                    link = f"https://www.videoland.com/api/v3/subtitles/{link[0]}"
                    Ep+=1
                    Ep= "{0:0=2d}".format(Ep)
                    filename = f"{title}.S{Season}E{Ep}.vtt"
                    Ep= int(Ep)
                    r = requests.get(link, cookies=cookie)
                    if r.status_code == 404:
                        print("Sorry, er is geen ondertiteling gevonden voor deze aflevering")
                    else:
                        print(f"{filename} aan het downloaden")
                        open(filename, 'wb').write(r.content)
        else:
            pass

else:
    print("Fout in URL. Probeer het opnieuw.")
