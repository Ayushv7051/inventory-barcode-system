import mysql.connector

# ---------- MySQL connection ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",  # change if needed
    password="",  # change if needed
    database="inventory_db"
)

cursor = db.cursor(dictionary=True)

# Test query
cursor.execute("SELECT * FROM products WHERE barcode = '12345678'")
product = cursor.fetchone()

print(product)
