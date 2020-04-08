####################### RUN THIS FOR THE FIRST TIME USING NLTK LIBRARY #################################
# import nltk
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()

import re
from nltk.corpus import wordnet
from database import match

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
    w1 = wordnet.synset(word1, '.n.01')
    w2 = wordnet.synset(word2, '.n.01')
    print(w1.wup_similarity(w2))

if __name__ == '__main__':
    syns = get_synonyms("bottle")
    print(syns)
    print(find_syns_db(syns))
