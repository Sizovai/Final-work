
import gensim.corpora as corpora

page_size = 1000
def docs_generator(cursor, logPrefix):
    offset = 0
    not_empty = True
    while not_empty:
        query = "select hat.id, hat.tokens from fp_attr_tokens hat order by hat.id offset %d limit %d" % (offset, page_size)
        cursor.execute(query)
        not_empty = False
        for row in cursor:
            not_empty = True
            yield row[1]
        print('%s:%d:%d' % (logPrefix, offset, offset))
        offset += page_size

def create_dictionary(conn):
    cursor = conn.cursor()

    id2word = corpora.Dictionary(docs_generator(cursor, 'dc'))

    print('id2word = %d' % len(id2word))

    id2word.save('/home/irina/data/dictionary')
