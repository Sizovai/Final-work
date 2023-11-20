import psycopg2 as psycopg2

conn = psycopg2.connect(dbname='hr', user='app', password='12345678', host='192.168.2.144', port=6432)

def get_recs(salary_from, salary_to):
    cursor = conn.cursor()
    query = """
        select ft.vis, fadt.topic, count(*) as cnt from fp_attribute fa 
        join fp_attr_dominate_topic fadt on fa.id = fadt.id
        join fp_topics ft on fadt.topic = ft.id 
        where salary >= %s and salary <= %s 
        group by fadt.topic, ft.vis order by cnt desc limit 10
    """ % (salary_from, salary_to)
    print(query)
    cursor.execute(query)
    return [row[0] for row in cursor]