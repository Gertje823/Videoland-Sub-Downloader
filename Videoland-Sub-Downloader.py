import requests, re, json, time, os
import urllib.request
from bs4 import BeautifulSoup
from vtt_to_srt import vtt_to_srt

cookie = {'vlId': 'YOUR_vlId_HERE'}
invalid = '<>:"/\|?* '
url = input("Wat is de Videoland url?")
url_pattern = "(https?:\/\/(?:www\.|(?!www)))videoland.com\/series\/(.*?)\/(.*?)\/\\\?(.*)"
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
    for char in invalid:
        filename = filename.replace(char, '')
    link = f"https://www.videoland.com/api/v3/subtitles/{x[4]}"
    r = requests.get(link, cookies=cookie)
    if r.status_code == 404:
        print("Sorry, er is geen ondertiteling gevonden voor deze film")
    else:
        print(f"{filename} aan het downloaden")
        open(filename, 'wb').write(r.content)
        print("Converting to srt")
        vtt_to_srt.vtt_to_srt(filename)
        os.remove(filename)

elif "/series/" in url:
    try:
        link = re.search(url_pattern, url).group(4)
        url= url.replace(link,"")
    except:
        pass
    wanted_season = input("Welk seizoen? (bv. 3)")
    Season = "{0:0=2d}".format(int(wanted_season))
    Ep = 0
    data = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(data.text, "html.parser")
    title = soup.select('h1')[0].text.strip()
    title = title.replace(" ", ".")
    x = url.split("/")
    # Get json with serie data
    pattern = "window.__INITIAL_STATE__ =(.*?);</script><script>"
    json_data = re.search(pattern, data.text).group(1)
    data = json.loads(json_data)
    season_num = 0
    # Check for wanted season
    for item in data["videos"]["details"]:
        try:
            if data["videos"]["details"][item]['type'] == "season" and data["videos"]["details"][item]['title'] == wanted_season:
                season = data["videos"]["details"][item]['ref'].replace("SN", "")
                path = data["application"]["path"]["current"]
                link = f"https://www.videoland.com{path}/{season}"
                data = requests.get(link, cookies=cookie)
                soup = BeautifulSoup(data.text, "html.parser")
                pattern = "window.__INITIAL_STATE__ =(.*?);</script><script>"
                json_data = re.search(pattern, data.text).group(1)
                data = json.loads(json_data)
                # Get ids of episodes in season
                for episodes in data["videos"]["details"].items():
                    if episodes[1]["type"] == "episode":
                        id = episodes[1]["id"]
                        link = f"https://www.videoland.com/api/v3/subtitles/{id}"
                        print(link)
                        Ep = episodes[1]["position"]
                        Ep = "{0:0=2d}".format(Ep)
                        filename = f"{title}.S{Season}E{Ep}.vtt"
                        for char in invalid:
                            filename = filename.replace(char, '')
                        Ep = int(Ep)
                        r = requests.get(link, cookies=cookie)
                        # Check if sub is available
                        if r.status_code == 404:
                            print("Sorry, er is geen ondertiteling gevonden voor deze aflevering")
                        else:
                            # Download sub
                            print(f"{filename} aan het downloaden")
                            open(filename, 'wb').write(r.content)
                            print("Converting to srt")
                            vtt_to_srt.vtt_to_srt(filename)
                            os.remove(filename)
        except KeyError:
            pass
        season_num +=1

else:
    print("Fout in URL. Probeer het opnieuw.")
