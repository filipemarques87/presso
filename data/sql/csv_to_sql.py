import csv
import sqlite3

conn = sqlite3.connect('crypto.db')
cursor = conn.cursor()

header = True
with open('BTCUSDT_1m.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        if header:
            header = False
            continue
    

        cursor.execute('INSERT INTO stocks\
            (date, symbol, granularity, open, high, low, close, volume)' \
                'VALUES(?, "BTCUSDT", "1", ?, ?, ?, ?, ?)',
            [row['Open time'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']])

#close the connection to the database.
conn.commit()
cursor.close()
print("Done")
