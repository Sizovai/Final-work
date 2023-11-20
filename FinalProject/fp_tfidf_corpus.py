import gensim
import numpy as np
from gensim import corpora
from tqdm import tqdm

import fp_lda


def filter(conn):
    id2word = corpora.Dictionary.load('/home/irina/data/dictionary')
    corpus = fp_lda.load_corpus(conn, 'fp_corpus')
    tfidf = gensim.models.TfidfModel(corpus, id2word=id2word)
    tfidf_corpus = tfidf[corpus]
    tf_max = max([max(doc[1] for doc in corpus) for corpus in tfidf_corpus])
    tf_min = min([min(doc[1] for doc in corpus) for corpus in tfidf_corpus])
    print(f'tfidf_max: {tf_max}, tfidf_min: {tf_min}')

    doc_ranges = [[doc[1] for doc in corpus] for corpus in tfidf_corpus]
    doc_percentiles = []
    for doc_range in doc_ranges:
        percent_pair = (np.percentile(doc_range, 5), np.percentile(doc_range, 95))
        doc_percentiles.append(percent_pair)

    print(doc_percentiles[0])

    filter_ids = [[0 for i in range(1)] for j in range(len(corpus))]

    # отфильтруем слова внутри каждого документа
    t = tqdm(range(len(tfidf_corpus)))
    for i in t:
        low_val, high_val = doc_percentiles[i]
        for j in range(len(doc_ranges[i])):
            if low_val <= doc_ranges[i][j] <= high_val:
                filter_ids[i].append((tfidf[corpus[i]][j][0], corpus[i][j][1]))

    print(len(filter_ids))
    cursor = conn.cursor()
    updateCursor = conn.cursor()
    updateCursor.execute("delete from fp_filtered_corpus")
    conn.commit()
    i = 0
    cursor.execute('select hat.id from fp_corpus hat order by hat.id')
    for id_row in cursor:
        bow_str = ['{%d, %d}' % (p[0], p[1]) for p in filter_ids[i][1:]]
        updateStr = "insert into fp_filtered_corpus values (%d, '{%s}')" % (id_row[0], ", ".join(bow_str))
        updateCursor.execute(updateStr)
        if i % 1000 == 0:
            print(i)
        i += 1
    conn.commit()
    cursor.close()
    updateCursor.close()


