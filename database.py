import sqlite3
import csv
import json
import re


def insert(item):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO items VALUES (:name, :classification, :info)",
                  {'name': item['name'], 'classification': item['classification'], 'info': item['info']})

# This function is implemented to get a list of suggestions for search bar
def get_all():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT name FROM items")
    data = c.fetchall(); results = []
    for item in data:
        results.append(item[0])
    return json.dumps(results)

def match(substring, match_whole_substring=True):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    if match_whole_substring:
        c.execute("SELECT * FROM items WHERE name LIKE '{}'".format(substring))
    else:
        c.execute("SELECT * FROM items WHERE name LIKE '{}%'".format(substring))
    matched_items = c.fetchall()
    results = []
    if len(matched_items) != 0:
        for data in matched_items:
            m = re.search('.*?([!.])', data[2])
            if m is not None:
                text = m.group()
                info = data[2][len(text):]
            else:
                text = ''
                info = ''
            item = {
                'name': data[0],
                'classification': data[1],
                'text': text,
                'info': info
            }
            results.append(item)
    return json.dumps(results)


def remove(item_name):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    with conn:
        c.execute("DELETE from items WHERE name = :name", {'name': item_name})


# Importing items from csv file
#
# with open('list_of_items.csv', 'r+', encoding="utf-8") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
#     for row in csv_reader:
#         new_item = {
#             'name': row[0],
#             'classification': row[1],
#             'info': row[2]
#         }
#         insert(new_item)
