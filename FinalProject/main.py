# This is a sample Python script.
import psycopg2 as psycopg2
import fp_gramms
import fp_tokenize
import fp_dictionary
import fp_corpus
import fp_tfidf_corpus
import fp_lda
import fp_vectorize

conn = psycopg2.connect(dbname='hr', user='app', password='12345678', host='192.168.2.144', port=6432)

# bigrams = fp_gramms.create_bigramms(conn)
# fp_gramms.create_trigramms(conn, bigrams)
# fp_tokenize.tokenize_table(conn)
#fp_dictionary.create_dictionary(conn)
# fp_corpus.create_corpus(conn)
#fp_tfidf_corpus.filter(conn)
#fp_lda.probe_topics_num(conn, 50)
#fp_vectorize.vec_topics(conn)
