import sqlite3
import json


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

