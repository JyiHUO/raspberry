import sqlite3

conn = sqlite3.connect("user_location.db")
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE user_location
             (username text, latitude  real, Longitude real, temperature real, pressure real, humidity real)''')

