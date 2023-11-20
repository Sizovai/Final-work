import logging
from sys import stdout

import gensim.corpora as corpora
import gensim.models
from IPython import get_ipython
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim  # don't skip this

def load_corpus(conn, table_name):
    cursor = conn.cursor()
    query = 'select hat.id, hat.bow from %s hat order by hat.id' % table_name
    cursor.execute(query)
    corpus = [row[1] for row in cursor]
    print('executed query, size %d' % len(corpus))
    return corpus

def probe_topics_num(conn, selected_topics_num=None):
    id2word = corpora.Dictionary.load('/home/irina/data/dictionary')
    print('id2word = %d' % len(id2word))
    corpus = load_corpus(conn, 'fp_filtered_corpus')
    cursor = conn.cursor()
    cursor.execute("select id, tokens from fp_attr_tokens order by id")
    data_lemmatized = [row[1] for row in cursor]
    print("read data_lemmatized, size = %d" % len(data_lemmatized))
    if not selected_topics_num:
        for topics_num in range(10, 50, 10):
            print('probe topics num %d' % topics_num)
            lda(conn, topics_num, id2word, corpus, data_lemmatized)
    else:
        lda(conn, selected_topics_num, id2word, corpus, data_lemmatized)


def lda(conn, topics_num, id2word, corpus, data_lemmatized):

    lda_model = gensim.models.ldamodel.LdaModel(corpus, topics_num, id2word)
    lda_model.save('/home/irina/data/lda_model')

    topics = lda_model.get_topics()
    print(topics)
    update_cursor = conn.cursor()
    update_cursor.execute('delete from fp_topics')
    conn.commit()
    for i in range(0,topics_num):
        topic = lda_model.get_topic_terms(i)
        words = [id2word[term[0]] for term in topic]
        vis = ','.join(words)
        update_cursor.execute('insert into fp_topics values (%d, \'%s\')' % (i, vis))
    conn.commit()

    print('\nPerplexity: ', lda_model.log_perplexity(corpus))

    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)
