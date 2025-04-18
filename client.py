from server.driver import connect

# Connect to the database
conn = connect("http://localhost:8000")
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT name, age FROM users WHERE name = 184")


results = cursor.fetchall()
print(results)


cursor.close()
conn.close()