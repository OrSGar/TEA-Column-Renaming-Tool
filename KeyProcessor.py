from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path


class KeyWebsite:
    """
        Key website class that represents a TEA website containing the key:value mappings for columns.

        Attributes
        ----------
        default_replacements : dict
            Default word replacements for a generated dict
        url : str
            URL of the target website
        _filename : str
            Filename of the saved JSON file (pre-processing)
        _file_save_path : str
            Save path of file
        _cleaned_filename : str
            Filename of the cleaned JSON file (post-processing)
        _cleaned_file_save_path : str
            Save path of cleaned file
        _key_dict : dict
            Dictionary of keys scraped from the website (pre-processing)
        _cleaned_dict : dict
            Cleaned (post-processed) dictionary of key_dict


        Methods
        -------
        scrape()
            Scrapes the URL of the website and generates a dictionary, sets the filename, returns a copy of the dictionary
        save_json(mode='scraped')
            Saves the original dictionary to the Generated Keys directory
        save_json(mode='cleaned')
            Saves the cleaned dictionary to the Processed Keys directory
        clean(replacement_dict=None, override_default=False)
            Cleans the key_dict dictionary using the defaults in the class
        clean(replacement_dict=dict, override_default=True)
            Cleans the key_dict dictionary using replacement_dict parameter, will not use defaults
        create_required_dirs()
            Checks for required directories present, creates them otherwise


    """

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
        self._file_save_path = ''
        self._cleaned_filename = ''
        self._cleaned_file_save_path = ''
        self._key_dict = {}
        self._cleaned_dict = {}

    @property
    def url(self):
        """ Get url """
        return self._url

    @property
    def filename(self):
        """ Get filename """
        return self._filename

    @property
    def cleaned_filename(self):
        """ Get cleaned filename """
        return self._cleaned_filename

    @property
    def key_dict(self):
        """ Get key_dict"""
        return self._key_dict

    @property
    def cleaned_dict(self):
        """Get cleaned_dict"""
        return self._cleaned_dict

    def scrape(self):
        """
        Scrapes the website and creates a dict, sets the filename, returns copy of the dict
        :returns: A copy of the created dictionary
        """

        # Create request to url, get a soup of the website
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create filename based on website title
        self._file_save_path = 'Generated_Keys/' + soup.find('strong').get_text().strip() + '.json'
        self._filename = self._file_save_path.split("/")[1]

        # Iterate through the table on the website and get the needed data
        for row in soup.find('table').find_all('tr')[2:]:
            # Create a pair of each row, only getting the key code and the description
            row = (row.find_all('td')[0].get_text().strip(), row.find_all('td')[3].get_text().strip())
            # Add to the dictionary
            self.key_dict[row[0]] = row[1]

        # Return a copy of the dictionary
        return self._key_dict.copy()

    def save_json(self, file='scraped'):
        """
        Saves a a key_dict to the Generated Keys directory or cleaned_dict to the Processed Keys directory
        For cleaned_dict, set file='cleaned'
        :param file: 'scraped' or 'cleaned', default 'scraped'
        :type file: str
        """
        # Save key_dict as json in ./Generated_Keys
        try:
            if file == 'scraped':
                if not self.filename:
                    raise FileNotFoundError

                with open(self._file_save_path, 'w') as destination:
                    json.dump(self._key_dict, destination, indent=2)
                    print(f'JSON file stored at: ./{self._file_save_path}')
            # Save cleaned_dict as json in ./Processed_Keys
            elif file == 'cleaned':
                if not self._cleaned_filename:
                    raise FileNotFoundError

                with open(self._cleaned_file_save_path, 'w') as destination:
                    json.dump(self._cleaned_dict, destination, indent=2)
                    print(f'JSON file stored at: ./{self._cleaned_file_save_path}')

        except FileNotFoundError:
            print(f"No files saved, please make sure you have run the scrape() or clean() functions.")

    def clean(self, replacement_dict=None, override_default=False):
        """
        Saves a a key_dict to the Generated Keys directory or cleaned_dict to the Processed Keys directory
        For cleaned_dict, set mode='cleaned'
        :param replacement_dict: A user defined dict with words to be replaced in key_dict, default None
        :type replacement_dict: dict
        :param override_default:
        :type override_default: bool
        :return: Copy of the cleaned dict
        """
        # Replace words in key_dict with words in default dictionary or replacement dict
        # Return a copy of the cleaned dict
        try:
            if not self._filename:
                raise FileNotFoundError

            for column_key, value in self._key_dict.items():
                if not override_default:
                    for target_word in KeyWebsite.default_replacements.keys():
                        value = value.replace(target_word, KeyWebsite.default_replacements[target_word]).strip()

                if replacement_dict:
                    for target_word in replacement_dict.keys():
                        value = value.replace(target_word, replacement_dict[target_word]).strip()

                self._cleaned_dict[column_key] = value

            self._cleaned_file_save_path = 'Processed_Keys/' + \
                                           Path(self._filename).name.replace('.json', '').strip() + \
                                           ' Processed Keys' + '.json '

            self._cleaned_filename = self._cleaned_file_save_path.split("/")[1]

        except FileNotFoundError:
            print('Please scrape the website before cleaning')

        return self._cleaned_dict.copy()

    @staticmethod
    def create_required_dirs():
        """ Check for and create required directories"""
        if not Path('./Generated_Keys/').is_dir():
            Path('./Generated_Keys/').mkdir(parents=True, exist_ok=True)
            Path('./Processed_Keys/').mkdir(parents=True, exist_ok=True)
            print('Required directories created')
        else:
            print('Required directories present')

    @classmethod
    def check_url(cls, url):
        """ Checks url to for correct typing """
        try:
            if not url:
                raise ValueError

            if not isinstance(url, str):
                raise TypeError

        except (ValueError, TypeError):
            return "Please make sure you have defined the required variables"
        else:
            return 'Variable checks passed'
