import requests
from bs4 import BeautifulSoup as B
import pyperclip
from wox import Wox, WoxAPI


class Main(Wox):

    def request_jisho(self, key):
        html = requests.get(f'https://jisho.org/search/{key}').content
        b = B(html, 'lxml')
        return b

    def meaning(self, b):
        return '; '.join([d.text.strip() for d in b.find_all(class_='meaning-definition')])

    def title(self, b):
        return b.find(class_='text').text.strip()

    def parse_results(self, b):
        return [
            {
                "Title": self.title(item),
                "SubTitle": self.meaning(item),
                "IcoPath": "Images\\icon.png",
                "JsonRPCAction": {
                    "method": "copy",
                    "parameters": [self.title(item)],
                    "dontHideAfterAction": False
                }
            }
            for item in b.find_all(class_='concept_light')
            if item.find(class_='text')
        ]

    def query(self, key):
        if key:
            b = self.request_jisho(key)
            return self.parse_results(b)
        else:
            return []

    def copy(self, text):
        pyperclip.copy(text)


if __name__ == "__main__":
    Main()
