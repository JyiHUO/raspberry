import geocoder


def find_my_location():
    g = geocoder.ip('me')
    return g