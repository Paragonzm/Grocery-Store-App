from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_connection import get_sql_connection
import products_dao

app = Flask(__name__)
CORS(app)

@app.route('/getProducts', methods=['GET'])
def get_products():
    conn = get_sql_connection()
    products = products_dao.get_all_products(conn)
    conn.close()
    return jsonify(products)

@app.route('/getProduct/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_sql_connection()
    product = products_dao.get_product_by_id(conn, product_id)
    conn.close()
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    data = request.get_json()
    conn = get_sql_connection()
    product_id = products_dao.insert_new_product(conn, data)
    conn.close()
    return jsonify({'product_id': product_id})

@app.route('/updateProduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    conn = get_sql_connection()
    products_dao.update_product(conn, product_id, data)
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    data = request.get_json()
    conn = get_sql_connection()
    products_dao.delete_product(conn, data['product_id'])
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/getUOMs', methods=['GET'])
def get_uoms():
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT uom_id, uom_name FROM uom")
    uoms = cursor.fetchall()
    conn.close()
    return jsonify([{'uom_id': u[0], 'uom_name': u[1]} for u in uoms])

if __name__ == '__main__':
    print("Starting Flask Server...")
    app.run(port=5000, debug=True)
