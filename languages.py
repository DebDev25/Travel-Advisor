import requests

from ISO_Codes import country_to_iso


class Languages:
    def __init__(self, country):
        self.country = country_to_iso[country]
        self.url = "http://api.geonames.org/countryInfoJSON"

    def get_languages(self, username):
        """
        :param username:
        :return: List containing the languages spoken in the city
        """
        languages = []

        country_params = {
            'country': self.country,
            'username': username
        }

        country_res = requests.get(self.url, params=country_params)
        country_res.raise_for_status()
        country_data = country_res.json()

        if country_data["geonames"]:
            languages = country_data["geonames"][0]["languages"].split(',')

        return languages
