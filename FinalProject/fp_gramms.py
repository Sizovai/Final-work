
import fp_tokenize
from gensim.models.phrases import Phrases, Phraser

page_size = 1000

def tokenize_strings_generator(cursor):
    offset = 0
    not_empty = True
    while not_empty:
        cursor.execute("select id, body from fp_attribute order by id offset %d limit %d" % (offset, page_size))
        not_empty = False
        for row in cursor:
            not_empty = True
            tokenized_string = fp_tokenize.tokenize_string(row[1])
            yield tokenized_string
        print(offset)
        offset += page_size

def create_bigramms(conn):
    cursor = conn.cursor()
    bigrams = Phrases(tokenize_strings_generator(cursor), min_count=1, threshold=5)  ## finding bigrams in the collection
    print(bigrams.__sizeof__())
    bigramPhraser = Phraser(bigrams)  ## setting up parser for bigrams
    bigramPhraser.save('/home/irina/data/bigramPhraser.pkl')
    return bigrams

def create_trigramms(conn, bigrams):
    cursor = conn.cursor()
    trigrams = Phrases(bigrams[tokenize_strings_generator(cursor)], min_count=2, threshold=5)  ## finding trigrams
    print(trigrams.__sizeof__())
    trigramPhraser = Phraser(trigrams)  ## parser for trigrams
    trigramPhraser.save('/home/irina/data/trigramPhraser.pkl')
