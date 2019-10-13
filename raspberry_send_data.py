import time
import numpy as np
from smbus import SMBus
from bme280 import BME280
import geocoder
import requests

tracked_days = lambda start: (time.time() - start) / (24 * 60 * 60)
day2secs = lambda x: x * 24 * 60 * 60
init_day = float(open('track_day').read().split('\n')[0])


def find_my_location():
    g = geocoder.ip('me')
    return g


def tempmf(cT):
    return 1 / (1 + np.e ** -10 * (cT - 25.0))


def pressmf(cP):
    return 1 - np.max([np.min([(cP - 74.5) / (101.3 - 74.5), (115.0 - cP) / (115.0 - 101.3)]), 0])


def trapmf(x):
    lb, hb, he, le = [1, 7, 7 * 4 * 2, 7 * 4 * 10]
    return np.max([np.min([(x - lb) / (hb - lb), 1, (le - x) / (le - he)]), 0])


def send_data(vals):
    risk = vals[3]
    if risk == 1:
        username = vals[0]
        localtion = str(vals[1]) + "," + str(vals[2])
        response = requests.get('http://120.55.167.195:4999/send/{}-{}'.format(username, localtion))

def send_data(vals):
    username = vals[0]
    lon = str(vals[1])
    lat = str(vals[2])
    risk = str(vals[3])
    tmp = username+"-"+lon+"-"+lat+"-"+risk
    response = requests.get('http://120.55.167.195:4999/send/{}'.format(tmp))


# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
try:
    while True:
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
        print('Risk: ')
        risk = np.max([tempmf(temperature), pressmf(pressure), trapmf(tracked_days(init_day))]
        print(risk)
        longitude, latitude = find_my_location()
        print('Location: ', longitude, latitude)
        vals_to_send = ['Proto_user', longitude, latitude, risk, temperature, pressure, humidity]
        send_data(vals_to_send)
        time.sleep(60 * 0.2)
except KeyboardInterrupt:
    pass