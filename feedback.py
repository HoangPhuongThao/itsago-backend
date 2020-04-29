import sqlite3
import json

# feedback.db consists of 3 tables: requests (where current number of requests to GAPI is hold)
#                                   rank_feedback (users ranking our app on scale 1-5)
#                                   notfound_feedback (items that were not found in items.db and are requested by users)


def update_nRequests():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM '{}'".format('requests'))
        current = c.fetchall()[0][0]
        c.execute('''UPDATE requests SET n_requests = ? WHERE n_requests = ?''', (current + 1, current))


def get_nRequests():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM '{}'".format('requests'))
        return c.fetchall()[0][0]


def process_feedback(rank, text):
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO rank_feedback VALUES (:rank, :text)", {'rank': rank, 'text': text})


def process_unfound_item(text):
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO notfound_feedback VALUES (:text)", {'text': text})


def retrieve_all(table):
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM '{}'".format(table))
    data = c.fetchall();
    return json.dumps(data)


def remove(table):
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    with conn:
        c.execute("DELETE from '{}'".format(table), {'text': "piano keyboard"})

