from bs4 import BeautifulSoup
from re import sub

class Kata:
    def __init__(self, soup):
        self.soup = soup

    @property
    def source_codes(self):
        codes = self.soup.find_all('div', {'class': 'markdown'})
        return [''.join(code.findAll(text=True)) for code in codes]

    @property
    def languages(self):
        languages = self.soup.find_all('h6')
        return [language.text.rstrip(':').lower() for language in languages]

    @property
    def difficulty(self):
        difficulty = self.soup.find('div', {'class': 'item-title'}).find('span').text
        return difficulty.replace(' ', '-').lower()

    @property
    def title(self):
        title = sub('[^a-zA-Z\d ]', '', self.soup.find('div', {'class': 'item-title'}).find('a').text.strip())
        return title.replace(' ', '-').lower()

    @property
    def kata_id(self):
        href = self.soup.find('div', {'class': 'item-title'}).find('a')['href']
        return href.split('/')[-1]


class KataParser:
    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.elems = soup.find_all('div', {'class': 'list-item solutions'})

    def parse_katas(self):
        return [Kata(elem) for elem in self.elems]
