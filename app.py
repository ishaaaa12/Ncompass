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

@app.route('/orders', methods=['GET'])
def get_orders_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    users = load_json('01_users.json')
    products = load_json('02_products.json')
    orders = load_json('03_orders.json')

    
    user = next((u for u in users if u.get('email') == email), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_orders = [o for o in orders if o.get('user_id') == user['id']]

    
    product_lookup = {p['id']: p for p in products}

    result = []
    for order in user_orders:
        product = product_lookup.get(order['product_id'])
        if not product:
            continue  

        order_value = product['price'] * order['quantity']
        result.append({
            'order_id': order['order_id'],
            'user_id': user['id'],
            'user_name': user['name'],
            'product_id': product['id'],
            'product_name': product['name'],
            'quantity': order['quantity'],
            'order_value': order_value,
            'order_date': order['order_date']
        })

    return jsonify(result)

@app.route('/revenue', methods=['GET'])
def get_revenue():
    orders = load_json('03_orders.json')
    products = load_json('02_products.json')
    product_price = {p['id']: p['price'] for p in products}
    revenue_by_date = {}
    for order in orders:
        date = order['order_date']
        price = product_price.get(order['product_id'], 0)
        order_revenue = price * order.get('quantity', 1)
        revenue_by_date[date] = revenue_by_date.get(date, 0) + order_revenue


    result = [
        {"date": date, "total_revenue": total}
        for date, total in sorted(revenue_by_date.items())
    ]
    return jsonify(result)

if __name__ == '__main__':

    app.run(debug=True)
