from server.driver import connect

# Connect to the database
conn = connect("http://localhost:8000")
cursor = conn.cursor()

# # Execute a query
cursor.execute("SELECT * FROM users")

row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

# cursor.execute("SELECT users.name, orders.product FROM users JOIN orders ON users.id = orders.user_id")

# results = cursor.fetchall()
# print(results)

cursor.close()
conn.close()