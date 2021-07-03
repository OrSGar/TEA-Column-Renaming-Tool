from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path


class Processor:
    default_replacements = {
        'Average': 'Avg',
        ' Students': '',
        'Male': 'M',
        'Female': 'F',
        '  ': ' ',
    }

    def __init__(self, url):
        self._url = url
        self._filename = ''
        self._cleaned_filename = ''
        self._key_dict = {}
        self._cleaned_dict = {}

    @property
    def url(self):
        return self._url

    @property
    def filename(self):
        return self._filename

    @property
    def cleaned_filename(self):
        return self._cleaned_filename

    @property
    def key_dict(self):
        return self._key_dict

    @property
    def cleaned_dict(self):
        return self._cleaned_dict

    def scrape(self):
        response = requests.get(self.url)

        soup = BeautifulSoup(response.text, 'html.parser')

        self._filename = 'Generated_Keys/' + soup.find('strong').get_text().strip() + '.json'

        for row in soup.find('table').find_all('tr')[2:]:
            row = (row.find_all('td')[0].get_text().strip(), row.find_all('td')[3].get_text().strip())
            self.key_dict[row[0]] = row[1]

        return self._key_dict.copy()

    def save_json(self, mode='scraped'):
        if mode == 'scraped' and self._filename != '':
            with open(self._filename, 'w') as destination:
                json.dump(self._key_dict, destination)

        elif mode == 'cleaned' and self._filename != '':
            self._cleaned_filename = 'Processed_Keys/' + \
                                     Path(self._filename).name.replace('.json', '').strip() + \
                               ' Processed Keys' + '.json '

            with open(self._cleaned_filename, 'w') as destination:
                json.dump(self._cleaned_dict, destination)

    def clean(self, replacement_dict=None, override_default=False):
        for column_key, value in self._key_dict.items():
            if not override_default:
                for target_word in Processor.default_replacements.keys():
                    value = value.replace(target_word, Processor.default_replacements[target_word]).strip()

            if replacement_dict:
                for target_word in replacement_dict.keys():
                    value = value.replace(target_word, replacement_dict[target_word]).strip()

            self._cleaned_dict[column_key] = value

        return self._cleaned_dict.copy()

    @staticmethod
    def create_required_dirs():
        if not Path('./Generated_Keys/').is_dir():
            Path('./Generated_Keys/').mkdir(parents=True, exist_ok=True)
            Path('./Processed_Keys/').mkdir(parents=True, exist_ok=True)
            print('Required directories created')
        else:
            print('Required directories present')


# tea_website_url = 'https://rptsvr1.tea.texas.gov/perfreport/tapr/2020/xplore/ccad.html'
#
# test_site = Processor(tea_website_url)
# scraped_dict = test_site.scrape()
#
# custom_dict = {
#     'Hispanic': 'Fucking beaners'
# }
#
# cleaned_dict = test_site.clean(override_default=True)
#
# test_site.save_json()
# test_site.save_json(mode='cleaned')
#
# print(test_site.filename)
# print(test_site.filename_cleaned)
#
# # print(scraped_dict)
# # print(cleaned_dict)
#
#
# # for column_key, value in test_dict.items():
# #     for target_word in default_replacements.keys():
# #         value = value.replace(target_word, default_replacements[target_word]).strip()
# #
# #     test_dict[column_key] = value
# #     print(value)
# #
# # print(json.dumps(test_dict, indent=4))
