from bs4 import BeautifulSoup
import requests as r
from os import path, mkdir
import random
from time import sleep

# wait time between calls
WAIT = 10
IPS = [{"http": 'http://178.62.54.68:3128', "https": 'http://178.62.54.68:3128'},
       {"http": 'http://1.10.189.7:34596', "https": 'http://1.10.189.7:34596'},
       {"http": 'https://36.89.181.183:61051', "https": 'https://36.89.181.183:61051'},
       {"http": 'https://70.28.36.37:49290', "https": 'https://70.28.36.37:49290'},
       {"http": 'http://112.175.62.24:8080', "https": 'http://112.175.62.24:8080'},
       {"http": 'http://51.75.109.93:3128', "https": 'http://51.75.109.93:3128'},
       {"http": 'http://128.199.157.124:8080', "https": 'http://128.199.157.124:8080'},
       {"http": 'http://46.101.60.198:3128', "https": 'http://46.101.60.198:3128'},
       {"http": 'http://145.239.94.145:54321', "https": 'http://145.239.94.145:54321'},
       {"http": 'http://128.199.249.22:8080', "https": 'http://128.199.249.22:8080'},
       {"http": '178.62.79.200:3128', "https": 'http://178.62.79.200:3128'}]


def getNextPage(link, songName, artistName):
    baseLink = "https://www.azlyrics.com"
    path = baseLink + link
    site = getsite(path)
    soup = BeautifulSoup(site.content, "lxml")
    overallDiv = soup.find("div", class_="col-xs-12 col-lg-8 text-center")
    if type(overallDiv) is None:
        raise AttributeError
    div = overallDiv.find_all("div", recursive=False)
    lyrics = div[4].get_text()
    f = open("artists/" + artistName + "/" + songName + ".txt", "a")
    try:
        f.write(lyrics)
    except UnicodeEncodeError as e:
        if '\x80' in lyrics:
            lyrics = lyrics.replace('\x80', '')
        elif '\u2032' in lyrics:
            lyrics = lyrics.replace('\u2032', '')
        else:
            character = (e.split('\''))[3]
            if character in lyrics:
                lyrics = lyrics.replace(character, '')
        f.write(lyrics)
    f.close()


def getalbums(fullLink, secondlink):
    site = getsite(fullLink)
    soup = BeautifulSoup(site.content, "lxml")
    try:
        albumArea = soup.find(id="listAlbum")
        links = albumArea.find_all("a", href=True)
    except AttributeError:
        site = getsite(secondlink)
        soup = BeautifulSoup(site.content, "lxml")
        albumArea = soup.find(id="listAlbum")
        links = albumArea.find_all("a", href=True)
    return links


def getAll(artistName):
    print("Getting all songs now! ")
    secondName = ""
    if " " in artistName:
        secondName = artistName[(artistName.index(" ") + 1):]
    artistName = (artistName.replace(" ", "")).lower()
    artistLink = artistName + ".html"
    artistSecond = secondName + ".html"
    artistletter = artistName[0:1]
    secondLetter = (secondName.lower())[0:1]
    baseLink = "https://www.azlyrics.com"
    fullLink = baseLink + "/" + artistletter + "/" + artistLink
    secondLink = baseLink + "/" + secondLetter + "/" + artistSecond
    if not path.exists("artists/" + artistName):
        mkdir("artists/" + artistName)
    links = getalbums(fullLink, secondLink)

    for i in links:
        dirty = i['href']
        cleanedLink = dirty[2:]
        songName = path.basename(cleanedLink)[:-5]
        sleep(random.randint(0, WAIT))
        getNextPage(cleanedLink, songName, artistName)
    print("Done!")

def randomindex():
    length = len(IPS)
    randomInt = random.randint(0, length - 1)
    return randomInt


def getsite(path):
    while True:
        try:
            whichBlocked = IPS[randomindex()]
            response = r.get(path, proxies=whichBlocked)
            break
        except r.exceptions.ProxyError as e:
            print("Proxy blocked, but retrying!")
        except r.exceptions.SSLError as e:
            print("Some other error, but retrying!")
    return response


getAll(input("Type in an artist's full name to get all of their lyrics! "));