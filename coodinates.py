import requests

from ISO_Codes import country_to_iso


class Coordinates:
    def __init__(self, city, country):
        self.city = city
        self.country = country_to_iso[country]
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

        coord_res = requests.get(self.url, coord_params)
        coord_res.raise_for_status()
        coord_data = coord_res.json()

        return coord_data[0]["lat"], coord_data[0]["lon"]
