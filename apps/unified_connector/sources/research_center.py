import requests
import datetime
from bs4 import BeautifulSoup as Soup

from .base import Source
from connector.utils import ConnectorWrapper
from lead.models import Lead


COUNTRIES_OPTIONS = [
    {'key': 'AF', 'label': 'Afghanistan'},
    {'key': 'BD', 'label': 'Bangladesh'},
    {'key': 'BW', 'label': 'Botswana'},
    {'key': 'BR', 'label': 'Brazil'},
    {'key': 'CF', 'label': 'Central African Republic'},
    {'key': 'TD', 'label': 'Chad'},
    {'key': 'HR', 'label': 'Croatia'},
    {'key': 'CD', 'label': 'Democratic Republic of the Congo'},
    {'key': 'GR', 'label': 'Greece'},
    {'key': 'HT', 'label': 'Haiti'},
    {'key': 'HU', 'label': 'Hungary'},
    {'key': 'IN', 'label': 'India'},
    {'key': 'IQ', 'label': 'Iraq'},
    {'key': 'IT', 'label': 'Italy'},
    {'key': 'JO', 'label': 'Jordan'},
    {'key': 'KE', 'label': 'Kenya'},
    {'key': 'KG', 'label': 'Kyrgyzstan'},
    {'key': 'LB', 'label': 'Lebanon'},
    {'key': 'LY', 'label': 'Libya'},
    {'key': 'MK', 'label': 'Macedonia'},
    {'key': 'ML', 'label': 'Mali'},
    {'key': 'MM', 'label': 'Myanmar'},
    {'key': 'NP', 'label': 'Nepal'},
    {'key': 'NE', 'label': 'Niger'},
    {'key': 'NG', 'label': 'Nigeria'},
    {'key': 'PS', 'label': 'Palestinian Territory'},
    {'key': 'PE', 'label': 'Peru'},
    {'key': 'PH', 'label': 'Philippines'},
    {'key': 'RS', 'label': 'Serbia'},
    {'key': 'SI', 'label': 'Slovenia'},
    {'key': 'SO', 'label': 'Somalia'},
    {'key': 'SS', 'label': 'South Sudan'},
    {'key': 'ES', 'label': 'Spain'},
    {'key': 'SD', 'label': 'Sudan'},
    {'key': 'SY', 'label': 'Syria'},
    {'key': 'CG', 'label': 'The Republic of the Congo'},
    {'key': 'TL', 'label': 'Timor-Leste'},
    {'key': 'TR', 'label': 'Turkey'},
    {'key': 'UG', 'label': 'Uganda'},
    {'key': 'UA', 'label': 'Ukraine'},
    {'key': 'VU', 'label': 'Vanuatu'},
    {'key': 'YE', 'label': 'Yemen'}
]


@ConnectorWrapper
class ResearchResourceCenter(Source):
    URL = 'http://www.reachresourcecentre.info/advanced-search'
    title = 'Research Resource Center'
    key = 'research-resource-center'

    options = [
        {
            'key': 'name_list[]',
            'field_type': 'select',
            'title': 'Country',
            'options': COUNTRIES_OPTIONS
        }
    ]

    def get_content(self, url, params):
        resp = requests.get(self.URL, params=params)
        return resp.text

    def fetch(self, params):
        results = []
        content = self.get_content(self.URL, params)
        soup = Soup(content, 'html.parser')
        contents = soup.find('table').find('tbody').findAll('tr')

        total_count = len(contents)
        limited_contents = contents
        for row in limited_contents:
            tds = row.findAll('td')
            title = tds[0].get_text().replace('_', ' ')
            date = tds[1].find('span').attrs['content'][:10]  # just date str  # noqa
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            url = tds[0].find('a').attrs['href']
            data = {
                'title': title.strip(),
                'published_on': date.date(),
                'url': url,
                'source': "Research Resource Center",
                'author': "Research Resource Center",
                'source_type': Lead.SourceType.WEBSITE,
            }
            results.append(data)
        return results, total_count
