from bs4 import BeautifulSoup
import requests

def scrapeTabroom(url):
    soup = returnSoup(url)
    entries = []
    for tr in soup.find_all('tr'):
        parts = tr.find_all('td')
        if len(parts) > 0:
            entry = {}
            entry['wins'] = int(parts[0].text.strip())
            entry['name'] = parts[2].text.strip()
            url = parts[2].find("a").get('href')
            speaksPage = returnSoup('http://tabroom.com' + url)
            speaksList = returnSpeaks(speaksPage, entry['name'])
            entry['speaks'] = sum(speaksList)
            hiloSpeaks = speaksList[1:-1]
            entry['hilo'] = sum(hiloSpeaks)
            entries.append(entry)
    entries = list(reversed(sorted(entries, key=lambda k: (k['wins'], k['hilo'], k['speaks']))))
    returnlist = []
    i = 1
    for entry in entries:
        returnlist.append("%s" % (entry['name']))
        i += 1
    return returnlist

def returnSpeaks(speaksPage, name):
    speaks = []
    trs = speaksPage.find_all('tr')
    for tr in trs:
        parts = tr.find_all('td')
        if "Round" in parts[0].text.strip():
            try:
                speaks.append(parts[5].text.strip())
            except:
                speaks.append("No Speak")
    for i in range(len(speaks)):
        try:
            speaks[i] = float(speaks[i])
        except: 
            speaks[i] = "No Speak"
    try:
        average = sum(filter(lambda a: a != "No Speak", speaks))/len(filter(lambda a: a != "No Speak", speaks))
    except:
        average = 0
    for i in range(len(speaks)):
        if speaks[i] == "No Speak":
            speaks[i] = average
    return sorted(speaks)

def returnSoup(url):
    if url[0:7] == "http://":
        r = requests.get(url)
    elif url[0:8] == "https://":
        r = requests.get("http://" + url[9:])
    else:
        r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data)
    return soup

if __name__ == '__main__':
    var = raw_input("Enter the URL of the prelim records page after all results have been posted: ")
    scrapeTabroom(var)