import sqlite3
#数据库名
db_name = "data.db"
#表名
table_name = "roles"
conn = sqlite3.connect(db_name)
rs = conn.cursor()
sql = "Select * from " + table_name
rs.execute('insert into roles (id, name) values (\'1\', \'Michael\')')
res = rs.execute(sql)
values = rs.fetchall()
print(values)