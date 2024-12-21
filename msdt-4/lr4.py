import logging
from flask import Flask, request, jsonify
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)

products = []
cart = {}


class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }


class CartItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }


def log_event(message, line=None):
    if line:
        message += f" (line {line})"
    logging.info(message)


@app.route('/products', methods=['POST'])
def create_product():
    log_event("Creating a new product", line=1)
    data = request.get_json()
    if not data or not 'name' in data or not 'price' in data:
        log_event("Invalid data received", line=2)
        return jsonify({"error": "Invalid data"}), 400

    product_id = len(products) + 1
    product = Product(id=product_id, name=data['name'], price=data['price'])
    products.append(product)
    log_event(f"Product created: {product.to_dict()}", line=3)
    return jsonify(product.to_dict()), 201


@app.route('/products', methods=['GET'])
def get_products():
    log_event("Fetching all products", line=4)
    return jsonify([product.to_dict() for product in products])


@app.route('/cart', methods=['POST'])
def add_to_cart():
    log_event("Adding product to cart", line=5)
    data = request.get_json()
    if not data or not 'product_id' in data or not 'quantity' in data:
        log_event("Invalid data received", line=6)
        return jsonify({"error": "Invalid data"}), 400

    product_id = data['product_id']
    quantity = data['quantity']

    if not any(product.id == product_id for product in products):
        log_event("Product not found", line=7)
        return jsonify({"error": "Product not found"}), 404

    if product_id in cart:
        cart[product_id].quantity += quantity
        log_event(f"Product quantity updated in cart: {product_id}, new quantity: {cart[product_id].quantity}", line=8)
    else:
        cart[product_id] = CartItem(product_id=product_id, quantity=quantity)
        log_event(f"Product added to cart: {product_id}, quantity: {quantity}", line=9)

    return jsonify({"message": "Product added to cart"}), 200


@app.route('/cart', methods=['GET'])
def get_cart():
    log_event("Fetching cart contents", line=10)
    cart_items = []
    for item in cart.values():
        product = next((p for p in products if p.id == item.product_id), None)
        if product:
            cart_items.append({
                "product": product.to_dict(),
                "quantity": item.quantity
            })
    return jsonify(cart_items)


if __name__ == '__main__':
    log_event("Starting the server", line=11)
    app.run(debug=True)