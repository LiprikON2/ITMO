import requests


def fetch_coords(address):
    r = requests.get('https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/geocodeAddresses?', params=address)
    print(r.content)


fetch_coords('Saint-Petersburg, Marshala Zhukova, 45')