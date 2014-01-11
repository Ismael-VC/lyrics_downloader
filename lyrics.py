#!/usr/bin/env python
import codecs
import json
import sys
import urllib
import urllib2

try:
    import bs4  # pip install beautifulsoup4
except ImportError:
    print "BeautifulSoup is not installed!"
    print "BeautifulSoup is necessary for this script\n Try to install it and try again"
    
def extract_lyrics(page):
    """Extract lyrics text from given lyrics.wikia.com html page."""
    soup = bs4.BeautifulSoup(page)
    result = []
    for tag in soup.find('div', 'lyricbox'):
        if isinstance(tag, bs4.NavigableString):
            if not isinstance(tag, bs4.element.Comment):
                result.append(tag)
        elif tag.name == 'br':
            result.append('\n')
    return "".join(result)

# get artist, song to search
artist = raw_input("Enter artist : ")
song = raw_input("Enter song : ")

# make request
query = urllib.urlencode(dict(artist=artist, song=song, fmt="realjson"))
response = urllib2.urlopen("http://lyrics.wikia.com/api.php?" + query)
data = json.load(response)

if data['lyrics'] != 'Not found':
    # print short lyrics
    print(data['lyrics'])
    # get full lyrics
    lyrics = extract_lyrics(urllib2.urlopen(data['url']))
    # save to file
    filename = "[%s] [%s] lyrics.txt" % (data['artist'], data['song'])
    with codecs.open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(lyrics)
    print("written '%s'" % filename)
else:
    sys.exit('not found')
