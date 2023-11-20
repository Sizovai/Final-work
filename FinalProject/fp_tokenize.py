
import pymorphy2
import langid
import re
from gensim.models.phrases import Phraser
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from stopwords import get_stopwords

sentTokenizer = PunktSentenceTokenizer()

tokenizer = RegexpTokenizer(r'\w+')

morph = pymorphy2.MorphAnalyzer()

langid.set_languages(['ru'])
stopWords = set().union(get_stopwords('ru'), stopwords.words('russian'))

def tokenize_string(str_p):
    str = re.sub("[^а-яА-я]", " ", str_p)
    sentList = [sent for sent in sentTokenizer.tokenize(str)]
    tokens = [word for sent in sentList for word in tokenizer.tokenize(sent.lower())]
    lemmedTokens = []
    for token in tokens:
        lemmedTokens.append(morph.parse(token)[0].normal_form)
    goodTokens = [token for token in lemmedTokens if not token in stopWords]
    return goodTokens

page_size = 1000

def tokenize_table(conn):

    bigramPhraser = Phraser.load('/home/irina/data/bigramPhraser.pkl')
    trigramPhraser = Phraser.load('/home/irina/data/trigramPhraser.pkl')

    cursor = conn.cursor()
    updateCursor = conn.cursor()
    updateCursor.execute("delete from fp_attr_tokens")
    conn.commit()
    offset = 0
    not_empty = True
    while not_empty:
        cursor.execute("select id, body from fp_attribute order by id offset %d limit %d" % (offset, page_size))
        not_empty = False
        for row in cursor:
            not_empty = True
            goodTokens = tokenize_string(row[1])
            ngrammsTokens = trigramPhraser[bigramPhraser[goodTokens]]
            updateStr = "insert into fp_attr_tokens values (%d, '{\"%s\"}')" % (row[0], "\", \"".join(ngrammsTokens))
            # print(updateStr)
            updateCursor.execute(updateStr)
        print(offset)
        offset += page_size
        conn.commit()

    cursor.close()
    updateCursor.close()
