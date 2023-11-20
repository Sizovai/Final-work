
import gensim.models

page_size = 1000

def vec_topics(conn):
    lda_model = gensim.models.ldamodel.LdaModel.load('/home/irina/data/lda_model')
    cursor = conn.cursor()
    updateCursor = conn.cursor()
    offset = 0
    not_empty = True
    updateCursor.execute('delete from fp_attr_dominate_topic')
    conn.commit()
    while not_empty:
        cursor.execute("select hat.id, hat.bow from fp_filtered_corpus hat order by hat.id offset %d limit %d" % (offset, page_size))
        not_empty = False
        for row in cursor:
            not_empty = True
            doc_topics = lda_model.get_document_topics(row[1])
            if not doc_topics:
                continue
            dominate_topic = None
            for topic in doc_topics:
                if not dominate_topic or topic[1] > dominate_topic[1]:
                    dominate_topic = topic
            updateCursor.execute('insert into fp_attr_dominate_topic values (%d, %d)' % (row[0], dominate_topic[0]))
        print(offset)
        offset += page_size
        conn.commit()
    cursor.close()
    updateCursor.close()
