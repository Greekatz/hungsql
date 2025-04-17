from server.driver import connect

conn = connect("http://localhost:8000", username="admin", password="1234")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE age > 24")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
