from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # change if needed
    database="inventory_db"
)

cursor = db.cursor(dictionary=True)

@app.route("/get_product/<barcode>", methods=["GET"])
def get_product(barcode):
    cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
    product = cursor.fetchone()
    return jsonify(product) if product else jsonify({})

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    cursor.execute(
        "INSERT INTO products (barcode, name, description, quantity, price) VALUES (%s,%s,%s,%s,%s)",
        (data["barcode"], data["name"], data.get("description", ""), data["quantity"], data["price"])
    )
    db.commit()
    return jsonify(message="Product added")

@app.route("/update_product", methods=["POST"])
def update_product():
    data = request.json
    cursor.execute(
        "UPDATE products SET name=%s, description=%s, quantity=%s, price=%s WHERE barcode=%s",
        (data["name"], data.get("description", ""), data["quantity"], data["price"], data["barcode"])
    )
    db.commit()
    return jsonify(message="Product updated")

@app.route("/adjust_inventory", methods=["POST"])
def adjust_inventory():
    data = request.json
    cursor.execute(
        "UPDATE products SET quantity = quantity + %s WHERE barcode=%s",
        (int(data["change"]), data["barcode"])
    )
    db.commit()
    return jsonify(message="Inventory adjusted")

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    cursor.execute(
        "SELECT barcode, name, price, quantity, updated_at FROM products WHERE name LIKE %s OR barcode LIKE %s ORDER BY updated_at DESC",
        (f"%{q}%", f"%{q}%")
    )
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
