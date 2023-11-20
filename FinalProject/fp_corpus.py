import gensim.corpora as corpora


def create_corpus(conn):

    id2word = corpora.Dictionary.load('/home/irina/data/dictionary')
    print('id2word = %d' % len(id2word))

    page_size = 1000
    cursor = conn.cursor()
    updateCursor = conn.cursor()
    updateCursor.execute("delete from fp_corpus")
    conn.commit()
    offset = 0
    not_empty = True
    while not_empty:
        cursor.execute("select id, tokens from fp_attr_tokens order by id offset %d limit %d" % (offset, page_size))
        not_empty = False
        for row in cursor:
            not_empty = True
            bow = id2word.doc2bow(row[1])
            bow_str = ['{%d, %d}' % (p[0], p[1]) for p in bow]
            updateStr = "insert into fp_corpus values (%d, '{%s}')" % (row[0], ", ".join(bow_str))
            # print(updateStr)
            updateCursor.execute(updateStr)
        print(offset)
        offset += page_size
        conn.commit()

    cursor.close()
    updateCursor.close()

    id2word.doc2bow([])
