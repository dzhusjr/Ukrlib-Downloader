import requests
from os.path import exists
from os import makedirs
from bs4 import BeautifulSoup as BS

N = 30
path = input('Path: ')
if not exists(fr'{path}\cr'):
    makedirs(fr'{path}\cr')
if not exists(fr'{path}\no_cr'):
    makedirs(fr'{path}\no_cr')
path_cr = fr'{path}\cr'
path_no_cr = fr'{path}\no_cr'

for id in range(1,N+1):
    html = requests.get(f'https://www.ukrlib.com.ua/books/getfile.php?tid={id}&type=6')
    if html.status_code != 200:continue
    soup = BS(html.content, 'html.parser')

    name = soup.select('div[class="page-title"] > h1')[0].text
    author = soup.select('div[class="page-title"] > h2')[0].text

    if not exists(fr'{path_cr}\{name}.html'):
        author_info = BS(requests.get(f'https://uk.wikipedia.org/wiki/{author}').text, 'html.parser')
        try:
            death = int(author_info.select('span[data-wikidata-property-id="P570"] > span > span > a')[1].contents[0])
            copyrights = death > 1972
        except Exception:
            #if death not found
            copyrights = True

        with open(f'{path_cr if copyrights else path_no_cr}\{name}.html', 'wb') as f:
            f.write(html.content)

    print(f'{round(id/N*100,1)}%',end = '\r')