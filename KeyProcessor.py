from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup
from pandas import read_csv


class KeyWebsite:
    """
        Key website class that represents a TEA website containing the key:value mappings for columns.

        Attributes
        ----------
        KeyWebsite.DEFAULTS : dict
            Default word replacements for a generated dict
        url : str
            URL of the target website
        _filename : str
            Filename of the saved JSON file (pre-processing)
        _dataset_path : str
            Absolute path of the location of the dataset corresponding to the TEA reference website
        _dataset_name : str
            Name of the dataset file
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
            Scrapes the URL of the website and generates a dictionary, sets the filename, returns a copy of the dict
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
        remap(mapping='cleaned')
            Remaps columns in original dataset to the dict generated from the original website dict or the cleaned dict


    """

    DEFAULTS = {
        'Average': 'Avg',
        ' Students': '',
        'Male': 'M',
        'Female': 'F',
        '  ': ' ',
    }

    def __init__(self, url: str):
        self._url = url
        self._filename = ''
        self._dataset_path = ''
        self._dataset_name = ''
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

    @property
    def dataset_path(self):
        return self._dataset_path

    @dataset_path.setter
    def dataset_path(self, path):
        if isinstance(path, str):
            self._dataset_path = path
            self._dataset_name = Path(path).stem

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
        :param replacement_dict: A user defined dict with words to be replaced in key_dict, default None
        :type replacement_dict: dict
        :param override_default: Override using the default replacement dictionary to replace words, default False
        :type override_default: bool
        :return: Copy of the cleaned dict
        """
        # Replace words in key_dict with words in default dictionary or replacement dict
        # Return a copy of the cleaned dict
        try:
            if not self._filename:
                raise FileNotFoundError

            # Iterate through keys
            for column_key, value in self._key_dict.items():
                # Replace using defaults if override_defaults False
                if not override_default:
                    for target_word in KeyWebsite.DEFAULTS.keys():
                        value = value.replace(target_word, KeyWebsite.DEFAULTS[target_word]).strip()

                # Replace words using user defined dict param
                if replacement_dict:
                    for target_word in replacement_dict.keys():
                        value = value.replace(target_word, replacement_dict[target_word]).strip()

                # Add results to new dict
                self._cleaned_dict[column_key] = value

            # Create save path
            self._cleaned_file_save_path = 'Processed_Keys/' + \
                                           Path(self._filename).name.replace('.json', '').strip() + \
                                           ' Processed Keys' + '.json '

            # Create file name
            self._cleaned_filename = self._cleaned_file_save_path.split("/")[1]

        except FileNotFoundError:
            print('Please scrape the website before cleaning')

        return self._cleaned_dict.copy()

    def remap(self, mapping='cleaned'):
        """
        Remaps the columns of original dataset found at location self._dataset_path and store in ./Processed_Datasets
        Can use cleaned dict or original to be used to remap the columns
        :param mapping: 'cleaned' for cleaned dictionary; 'scraped' for the original, default 'cleaned'
        :type mapping: str
        """
        try:
            if not self.dataset_path:
                raise AttributeError

            if mapping == 'cleaned':
                if not self._cleaned_filename:
                    raise FileNotFoundError

                new_file_name = f'./Processed_Datasets/{self._dataset_name}_cleaned_mappings.csv'
                read_csv(self._dataset_path).rename(columns=self._cleaned_dict).to_csv(new_file_name)
                print(f'CSV file stored at: {new_file_name}')

            elif mapping == 'scraped':
                if not self._filename:
                    raise FileNotFoundError

                new_file_name = f'./Processed_Datasets/{self._dataset_name}_scraped_mappings.csv'
                read_csv(self.dataset_path).rename(columns=self._key_dict).to_csv(new_file_name)
                print(f'CSV file stored at: {new_file_name}')

        except AttributeError as error:
            print(f'Please define a dataset path and scrape/clean before remapping.')
            print(error)
        except FileNotFoundError:
            print(f'Please scrape the website or clean the results, cleaned or scraped dicts are missing')

    @staticmethod
    def create_required_dirs():
        """ Check for and create required directories"""
        # Check for directories
        if not Path('./Generated_Keys/').is_dir() or not Path('./Generated_Keys/').is_dir() or not Path(
                './Processed_Datasets/').is_dir():
            Path('./Generated_Keys/').mkdir(parents=True, exist_ok=True)
            Path('./Processed_Keys/').mkdir(parents=True, exist_ok=True)
            Path('./Processed_Datasets/').mkdir(parents=True, exist_ok=True)
            print('Required directories created')
        else:
            print('Required directories present')


# site = 'https://rptsvr1.tea.texas.gov/perfreport/tapr/2019/xplore/dapib.html'
#
# testsite = KeyWebsite(site)
#
# testsite.dataset_path = 'A://DS4A/Project/TEA/data/DAPIB.csv'
#
# testsite.remap()