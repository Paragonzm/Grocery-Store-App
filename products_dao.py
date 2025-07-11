from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = """
        SELECT p.product_id, p.name, p.uom_id, p.price_per_unit, u.uom_name
        FROM products p
        INNER JOIN uom u ON p.uom_id = u.uom_id
    """
    cursor.execute(query)
    result = cursor.fetchall()
    response = [{
        'product_id': row[0],
        'name': row[1],
        'uom_id': row[2],
        'price_per_unit': float(row[3]),
        'uom_name': row[4]
    } for row in result]
    return response

def get_product_by_id(connection, product_id):
    cursor = connection.cursor()
    query = """
        SELECT product_id, name, uom_id, price_per_unit
        FROM products
        WHERE product_id = %s
    """
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    if result:
        return {
            'product_id': result[0],
            'name': result[1],
            'uom_id': result[2],
            'price_per_unit': float(result[3])
        }
    return None

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = "INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)"
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def update_product(connection, product_id, product):
    cursor = connection.cursor()
    query = """
        UPDATE products
        SET name = %s, uom_id = %s, price_per_unit = %s
        WHERE product_id = %s
    """
    data = (product['product_name'], product['uom_id'], product['price_per_unit'], product_id)
    cursor.execute(query, data)
    connection.commit()

def delete_product(connection, product_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    connection.commit()
