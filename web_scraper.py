import requests
import json
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States'

president_ls = []
website = requests.get(url)
soup = BeautifulSoup(website.content, 'html.parser')
#print(soup)

president_table = soup.find('table')
#print(president_table.text)

president_table = president_table.find_all('tr')

president_table.pop(0)

#print(president_table[0].find_all('a')[1]['href'])

for president in president_table:
    link_info = url[:24] + president.find_all('a')[0]['href']
    link_picture = url[:24] + president.find_all('a')[1]['href']
    name = president.find_all('td')[1].text
    birth_year = ''
    death_year = ''
    still_name = True
    is_birth = True
    for i,char in enumerate(name):
        if still_name and char != ' ' and char != '.' and not char.isalpha():
            still_name = False
        elif not still_name and char == 'b':
            birth_year = name[i+3:len(name) - 6]
            death_year = 'n/a'
            name = name[:-12]
            break
        elif char == '–':
            is_birth = False
        elif is_birth and not still_name:
            birth_year += char
        elif not is_birth and char.isdigit():
            death_year += char
        elif not is_birth and not char.isdigit():
            name = name[:-16]
            break
    party = president.find_all('td')[4].text
    # print(president.find_all('td'))
    # print('end')
    if name[-2:] == '(b':
        name = name[:-2]
    
    dc = {'name' : name, 'birth year': birth_year, 'death year': death_year,
          'picture source': link_picture, 'information source': link_info}
    president_ls.append(dc)
    
with open('output.json', 'w') as k:
    json.dump(president_ls, k, indent=4, ensure_ascii=False)

print('created json file')
