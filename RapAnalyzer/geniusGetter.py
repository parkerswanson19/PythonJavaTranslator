from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

my_url = "https://genius.com/Meek-mill-rico-lyrics"

req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")


lyrics = page_soup.find("div", {"class": "lyrics"})
a_tags = lyrics.findAll("a")

for tag in a_tags:
    print(tag.contents)
    for line in tag.contents:
        if isinstance(line, str) == True:
            line.replace("\n", "")
            print(line)

# print(a_tags[0].contents)