import sqlite3

conn = sqlite3.connect('entertainments.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE entertainment
          ''')

conn.commit()
conn.close()
