import sqlite3

conn = sqlite3.connect('entertainments.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE entertainment
          (id INTEGER PRIMARY KEY ASC, 
           name VARCHAR(250) NOT NULL,
           year_released INTEGER NOT NULL,
           director VARCHAR(100) NOT NULL,
           rating FLOAT (2) NOT NULL,
           type VARCHAR(10) NOT NULL,
           length FLOAT (2)
           )
          ''')

conn.commit()
conn.close()
