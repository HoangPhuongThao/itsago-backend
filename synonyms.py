"""
####################### RUN THIS FOR THE FIRST TIME USING NLTK LIBRARY #################################
import nltk
import ssl

try:
     _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
"""

import re, json
from nltk.corpus import wordnet
from database import match, get_all
from nltk.corpus.reader.wordnet import WordNetError

def get_synonyms(word):
    syns = [word.lower()]
    for synset in wordnet.synsets(word, pos='n'):
        for lemma in synset.lemmas():
            syn = lemma.name()
            syn = re.sub(r'[\W_]', ' ', syn)
            if syn not in syns:
                syns.append(syn)
    return syns

def find_syns_db(syns):
    for syn in syns:
        if len(match(syn)) > 0:
            return match(syn)

def check_similarity(word1, word2):
    try:
        w1 = wordnet.synset(word1 + '.n.01')
        w2 = wordnet.synset(word2 + '.n.01')
        return w1.wup_similarity(w2)
    except WordNetError:
        return 0

def find_similar(input, threshold=0.8):
    db_items = json.loads(get_all())
    max_score = threshold
    similar_word = ''
    for item in db_items:
        score = check_similarity(input, item)
        if score > max_score:
            max_score = score
            similar_word = item
    if max_score > threshold:
        # print(max_score)
        return match(similar_word)
    return []

if __name__ == '__main__':
    # syns = get_synonyms("bottle")
    # print(syns)
    # print(find_syns_db(syns))
    print(find_similar('bottle'))

