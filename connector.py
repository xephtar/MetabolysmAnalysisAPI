from decouple import config
import psycopg2

DATABASE_NAME = config('DATABASE_NAME')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')

conn_str = "host=manny.db.elephantsql.com dbname={} user={} password={}".format(DATABASE_NAME, DATABASE_NAME,
                                                                                DATABASE_PASSWORD)

conn = psycopg2.connect(conn_str)
cursor = conn.cursor()
cursor.execute('SELECT * FROM articles_article LIMIT 10')
records = cursor.fetchall()

cursor.execute("ROLLBACK")
cursor.commit()
