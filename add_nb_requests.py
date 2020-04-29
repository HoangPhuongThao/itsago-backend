import sqlite3
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
c.execute("""CREATE TABLE requests (
            n_requests integer
            )""")
with conn:
    c.execute("INSERT INTO requests VALUES (:n_requests)", {'n_requests': 2400})
conn.close()