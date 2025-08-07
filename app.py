from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

@app.route('/users', methods=['GET'])
def get_users():
    users = load_json('01_users.json')
    return jsonify(users)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = load_json('02_products.json')
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/orders/<email>', methods=['GET'])
def get_orders_by_email(email):
    orders = load_json('01_users.json')
    user_orders = [o for o in orders if o['user_email'] == email]
    return jsonify(user_orders)

@app.route('/revenue', methods=['GET'])
def get_revenue():
    orders = load_json('02_orders.json')
    products = load_json('03_products.json')
    product_price = {p['id']: p['price'] for p in products}
    revenue = {}
    for order in orders:
        pid = order['product_id']
        revenue[pid] = revenue.get(pid, 0) + product_price.get(pid, 0) * order.get('quantity', 1)
    return jsonify(revenue)

if __name__ == '__main__':
    app.run(debug=True)