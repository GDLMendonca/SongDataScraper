#Import libraries
import fileinput
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from langdetect import detect

#Add proxies, if desired
'''
proxies = {
    'https': 'http://200.0.47.89:44295',
}
pageResult = requests.get(url,headers=headers,proxies=proxies)
'''
#Default vars
defaulturl = "https://tunebat.com/Search?q=" #aka quotepage
#Write to file method
def writeToFile(songData):
    #Write to CSV
    with open('C:/Users/Gabe/Documents/LearningAI/SongNamer/dataset.csv', 'a', encoding='utf-8', errors='surrogateescape', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([songData])
       
    csv_file.close()

#Pick search term from dictionary (100,000 most comomn english words)
for line in fileinput.input("C:/Users/Gabe/Documents/LearningAI/SongNamer/src/100k.txt"):
    #Decode to Utf
    searchterm = line
    print(searchterm) #For testing

    #Get html from url
    headers = {'User-Agent':'Mozilla/5.0'}
    url = defaulturl+searchterm
    #Get page
    pageResult = requests.get(url,headers=headers)
    page = pageResult.content
    #Parse with soup
    soup = BeautifulSoup(page, 'html.parser')
    #Scrape search results list
    searchResultsList = soup.find('div', {'class': 'searchResultList'})

    #Get all songs as list
    SongResults = searchResultsList.find_all('div', {'class': 'searchResultNode'})

    #Iterate through all results
    for i in range(len(SongResults)):
        #Get Song Name & remove feature artists from it
        thisSongName = (SongResults[i].find('div', {'class': 'search-track-name'})).text

        if "(feat." in thisSongName:
            thisSongName = thisSongName[0:thisSongName.find("(feat.")]
        elif "(with " in thisSongName:
            thisSongName = thisSongName[0:thisSongName.find("(with ")]

        #Scrape song info
        dataColumns = SongResults[i].find_all('div', {'class' : 'col-md-4 col-sm-4 col-xs-4'})
        #Get Key of this song (replaces'♭' with "-flat" & '#' with "-sharp")
        thisSongKey = str(((dataColumns[0].find('div', {'class': 'search-attribute-value'})).text).replace(u"\u266D","-flat").replace("#","-sharp"))
        #Get tempo of this song
        thisSongTempo = (dataColumns[2].find('div', {'class': 'search-attribute-value'})).text

        #Save values as list & call append
        try:
            detect(thisSongName)
            if detect(thisSongName) == 'en':
                thisSongData = [[thisSongName], [thisSongKey], [str(thisSongTempo)]]
                writeToFile(thisSongData)
        except:
            print("Song not saved: Not legible")
        

    #for testing
        print(thisSongName + thisSongKey + thisSongTempo)
    #break
