import psycopg2
import time

conn = psycopg2.connect(
    host="127.0.0.1",
    database="meta-land",
    user="postgres",
    password="gtongel553",
    port = "5432"
)

conn.autocommit = True

cur = conn.cursor()

cur.execute("SELECT * FROM user_info")
rows = cur.fetchall()

for i in range(len(rows)):
    for j in range(len(rows[i])):
        print(rows[i][j])


cur.execute("DELETE FROM user_info")
conn.commit()

cur.execute("SELECT * FROM user_info")
rows = cur.fetchall()

for i in range(len(rows)):
    for j in range(len(rows[i])):
        print(rows[i][j])


query_insert = (
    f"INSERT INTO user_info (first_name, last_name, password, amount_of_food, amount_of_stuff, amount_of_money)"
    f" VALUES ('Yasemin', 'Egeli', 'Y2001@Egeli', '100', '100', '100');"
)

cur.execute(query_insert)

cur.execute("SELECT * FROM user_info")
rows = cur.fetchall()

for i in range(len(rows)):
    for j in range(len(rows[i])):
        print(rows[i][j])


query_update = """
    UPDATE user_info
    SET amount_of_food = 95
    WHERE first_name = 'Yasemin';
"""

cur.execute(query_update)
cur.execute("SELECT * FROM user_info")
rows = cur.fetchall()

for i in range(len(rows)):
    for j in range(len(rows[i])):
        print(rows[i][j])



conn.close()