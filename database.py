import sqlite3
import csv

conn = sqlite3.connect('items.db')

c = conn.cursor()

def insert(item):
    with conn:
        c.execute("INSERT INTO items VALUES (:name, :classification, :info)",
                  {'name': item['name'], 'classification': item['classification'], 'info': item['info']})

def get(name):
    c.execute("SELECT * FROM items WHERE name=:name", {'name': name})
    return c.fetchall()

def remove(item):
    with conn:
        c.execute("DELETE from items WHERE name = :name", {'name': item['name']})

# Importing items from csv file
#
# with open('list_of_items.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         new_item = {
#             'name': row[0],
#             'classification': row[1],
#             'info': row[2]
#         }
#         insert(new_item)

# Checking number of items in db
#
# c.execute("SELECT * FROM items")
# results = c.fetchall()
# print(len(results))

conn.close()
