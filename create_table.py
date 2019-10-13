import sqlite3

conn = sqlite3.connect("user_feature.db")
c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE user_feature
#              (username text, latitude  real, Longitude real, temperature real, pressure real, humidity real)''')

c.execute('''CREATE TABLE user_info
              (username text, lon real, lat real, risk real)''')

c.execute('''CREATE TABLE user_email
              (username text, email text)''')