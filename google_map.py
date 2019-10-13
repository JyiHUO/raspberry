import geocoder
import requests

def find_my_location():
    g = geocoder.ip('me')
    return g

response = requests.get('http://120.55.167.195:4999')
print(response.content)