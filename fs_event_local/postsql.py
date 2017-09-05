# __author__ = 'ETwise'
import psycopg2
# set connect parameter
conn=psycopg2.connect(database="test",user="postgres",password="postgres",host="192.168.0.183",port="5432")
cur=conn.cursor()
# create one table
cur.execute("CREATE TABLE student(id integer,name varchar,sex varchar);")
# insert one item
cur.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)",(1,'TONY','M'))
cur.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)",(2,'Michelle','F'))
cur.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)",(3,'Albert','M'))

# get result
cur.execute('SELECT * FROM student')
results=cur.fetchall()
print results

# close connect
conn.commit()
cur.close()
conn.close()