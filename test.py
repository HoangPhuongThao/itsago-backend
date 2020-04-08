from csv import writer, reader
from database import match
from synonyms import get_synonyms, find_syns_db, check_similarity, find_similar
from nltk.corpus.reader.wordnet import WordNetError

# 1. option: get results with matching input with wordnet synonyms
# 2. option: get results by comparing input with every word in db - looking at the similarities between words

def option1(input):
    syns = get_synonyms(input)
    return find_syns_db(syns)

def option2(input):
    threshold = 0.7
    most_similar_item = find_similar(input, threshold)
    return most_similar_item

def get_similarities():
    with open('word_pairs.csv', 'r') as read_obj, open('word_pairs_sim.csv', 'w', newline='') as write_obj:
        csv_reader = reader(read_obj, delimiter=';')
        csv_writer = writer(write_obj)
        for row in csv_reader:
            score = check_similarity(row[0], row[1])
            row.append(score)
            row.append(option1(row[0]))
            row.append(option2(row[0]))
            csv_writer.writerow(row)

if __name__ == "__main__":
    get_similarities()
