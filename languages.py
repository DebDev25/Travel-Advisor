import requests


class Languages:
    def __init__(self, country):
        self.country = country
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

        # Handling API response
        try:
            country_res = requests.get(self.url, params=country_params)
            country_res.raise_for_status()
            country_data = country_res.json()
        except requests.exceptions.RequestException:
            raise RuntimeError("Geonames API request failed")
        except (KeyError, ValueError):
            raise RuntimeError("Geonames API returned unexpected data format")

        if country_data["geonames"]:
            languages = country_data["geonames"][0]["languages"].split(',')

        return languages
