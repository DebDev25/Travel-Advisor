import requests


class Coordinates:
    def __init__(self, city, country):
        self.city = city
        self.country = country
        self.url = "http://api.openweathermap.org/geo/1.0/direct"

    def get_coordinates(self, api):
        """
        :param api:
        :return: Coordinates of latitude and longitude respectively
        """
        coord_params = {
            'q': f'{self.city}, {self.country}',
            'appid': api,
            'limit': 1,
        }

        # Handling API response
        try:
            coord_res = requests.get(self.url, params=coord_params)
            coord_res.raise_for_status()
            coord_data = coord_res.json()
        except requests.exceptions.RequestException:
            raise RuntimeError("Openweathermap API request failed")
        except (KeyError, ValueError):
            raise RuntimeError("Openweathermap API returned unexpected data format")

        return coord_data[0]["lat"], coord_data[0]["lon"]
