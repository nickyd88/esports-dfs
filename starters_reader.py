
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getStarters():
    url = 'https://www.rotowire.com/daily/esports/lol-lineups.php'

    html = urlopen(url)

    soup = BeautifulSoup(html, 'html.parser')

    players = soup.find_all('li', {'class': 'lineup__player'})

    starters = []
    for player in players:
        starters.append(player.a.text)

    return starters