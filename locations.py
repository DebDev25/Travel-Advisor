import requests


class Locations:
    def __init__(self):
        self.url = "https://api.geoapify.com/v2/places"

    def get_locations(self, latitude, longitude, api):
        """
        :param longitude:
        :param latitude:
        :param api:
        :return: List containing the tourist spots in the city
        """
        loc_params = {
            'categories': 'tourism.attraction',
            'filter': f'circle:{longitude},{latitude},{3000}',
            'limit': 7,
            'lang': 'en',
            'apiKey': api,
        }

        loc_res = requests.get(self.url, params=loc_params)
        loc_res.raise_for_status()
        loc_data = loc_res.json()

        locations = [_["properties"].get("name", "Unnamed") for _ in loc_data["features"]]

        return locations
