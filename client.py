from server.driver import connect

# Connect to the database
conn = connect("http://localhost:8000")
cursor = conn.cursor()

# # Execute a query
cursor.execute("SELECT name, age FROM users WHERE name = Alice")

row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

cursor.execute("SELECT name, age FROM users WHERE age < 20")

results = cursor.fetchall()
print(results)

cursor.close()
conn.close()