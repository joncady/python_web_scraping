import requests as r
from bs4 import BeautifulSoup
import random


def randomIndex(length):
    return random.randint(0, length - 1)


def nextPage (link):
    newPage = r.get(link)
    soup = BeautifulSoup(newPage.content, "lxml")
    body = soup.find(id="bodyContent")
    content = ""
    allLinks = body.find_all("a", href=True)
    while not "wiki" in content:
        link = allLinks[randomIndex(len(allLinks))]
        content = link["href"]
    return(cleanLink(content))

def cleanLink(clean):
    if not "https://" in clean:
        clean = "https://en.wikipedia.org" + clean
    return clean

print("Ready to find a random page?")
wikipedia = r.get("https://en.wikipedia.org/wiki/Main_Page")
soup = BeautifulSoup(wikipedia.content, "lxml")
infoDiv = soup.find("div", id="mp-dyk")
newsDiv = soup.find("div", id="mp-itn")
dayDiv = soup.find("div", id="mp-otd")
infoLinks = infoDiv.find_all("a", href=True)
newsLinks = newsDiv.find_all("a", href=True)
dayLinks = dayDiv.find_all("a", href=True)
allLinks = infoLinks + newsLinks + dayLinks
link = allLinks[randomIndex(len(allLinks))]
link = link["href"]
lastPage = ""
for var in range(50):
    # if var == 12:
    #     print("25%", end="", flush=True)
    # elif var == 25:
    #     print("50%", end="", flush=True)
    # elif var == 37:
    #     print("75%", end="", flush=True)
    # else:
    #     print(".", end="", flush=True)
    lastPage = nextPage(cleanLink(link))
print("Done!")
print(lastPage)
