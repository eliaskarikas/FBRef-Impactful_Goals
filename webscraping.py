from bs4 import BeautifulSoup
import urllib.request as urllib
import pandas as pd
import ssl
from random import randint
from time import sleep

def find_urls(initial_url):
    """
    :param initial_url:
    :return: web scrapes a table to find a list of urls, specialized for fbref.com,
    maybe think about adding this as a parser
    """
    urls = []
    ssl._create_default_https_context = ssl._create_unverified_context
    #html = urllib.urlopen(initial_url)
    soup = BeautifulSoup((urllib.urlopen(initial_url)).read())
    table = soup.find('tbody')
    rows = table.find_all('tr')
    for row in rows:
        #date1 = row.find('td', {'class':"left", "data-stat":"date"})
        #team1 = row.find('td', {'class':"right", "data-stat": "squad_a"})
        #team2 = row.find('td', {'class':"right", "data-stat": "squad_b"})
        link = row.find('td', {'class':'center', 'data-stat': 'score'})
        #dates.append(date1.get_text())
        if link.find('a') == None:
            pass
        elif link.find('a').get('href') != None:
            urls.append('https://fbref.com'+ str(link.find('a').get('href')))

    #urls = [if row.find('td', {'class':'center', 'data-stat': 'score'}).find('a') == None for row in rows]

    return urls[0:5]


def scrape_data(intialurl):
    """
    :param intialurl:
    :return: Maybe considering just taking list of urls? Project is specialized for fb ref.
    Feel like not going to be scalable.
    """
    playerstats = {}

    urls = find_urls(intialurl)

    for url in urls:
        teams = {}
        score = 0
        html = urllib.urlopen(url)
        soup = BeautifulSoup(html.read())
        table = soup.find('table', {'id': 'shots_all'})
        rows = table.find_all('tr', {'style': 'background-color:rgb(210,240,210)'})
        print(url)
        for row in rows:
            player = row.find('td', {'class': 'left', 'data-stat':'player'})
            player = player.find('a').get_text()
            team = row.find('td',{'class':'left','data-stat':'squad'}).get_text()
            print(team)
            if team not in teams:
                teams[team] = 1
            if player not in playerstats:
                playerstats[player] = {'clutch goals': 0, 'non-clutch goals': 0}
                if team not in teams or team != teams[-1]:
                    print('yaos')
                    score -= 1
                    teams.append(team)
                    playerstats[player]['clutch goals'] += 1
                elif team == teams[-1]:
                    score += 1
                    print('yup')
                    teams.append(team)
                    playerstats[player]['non-clutch goals'] += 1
            else:
                if team not in teams or team != teams[-1] or scores == 0:
                    print('yaos')
                    teams.append(team)
                    playerstats[player]['clutch goals'] += 1
                    score += 1
                elif team == teams[-1]:
                    print('yup')
                    teams.append(team)
                    playerstats[player]['non-clutch goals'] += 1
            # Sleep a random number of seconds (between 1 and 5)
            print(playerstats)

        sleep(randint(1, 5))
    print(playerstats)
    # creating dataframe with data, indexvals and columns
    df = pd.DataFrame.from_dict(playerstats, orient='index')
    #df.to_csv('trying.csv')
    df = df.fillna(0)
    # converting to float to alter later
    return df

# cumulative score through one metric

def main():
    intial_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    #find_urls(intial_url)
    scrape_data(intial_url)

#
# Essentially this: 1. Get all possible links for premier league stats from fbref.
# 2. Enter link and gather all goal data, and times?
    # generate metric that creates dictionary of stats, when it is a goal that is purposeful.
    # This meaning that the goal either a. Sends team ahead in score, or equalizes scores.
    # could maybe put this in df?
# 3. Then can conduct analysis. Possibly give a score per 90.
if __name__ == '__main__':
    main()
