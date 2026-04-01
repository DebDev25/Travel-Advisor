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
            if country_data.get("geonames"):
                languages = country_data["geonames"][0]["languages"].split(',')
            else:
                languages = ["Current data unavailable"]
            return languages
        except requests.exceptions.RequestException as e:
            print(f"Warning: Geonames API request failed - {e}")
            return ["Current data unavailable"]
        except (KeyError, ValueError, IndexError, TypeError) as e:
            print(f"Warning: Geonames API returned unexpected data format - {e}")
            return ["Current data unavailable"]
