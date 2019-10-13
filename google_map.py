import geocoder
import requests

def find_my_location():
    g = geocoder.ip('me')
    return g

# response = requests.get('http://120.55.167.195:4999')
# print(response.content)

def send_data(vals):
    username = vals[0]
    lon = str(vals[1])
    lat = str(vals[2])
    risk = str(vals[3])
    tmp = username+"&"+lon+"&"+lat+"&"+risk
    response = requests.get('http://120.55.167.195:4999/save_data/{}'.format(tmp))
    print(response)

vals = ["1", 2,3,4]
send_data(vals)