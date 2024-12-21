from flask import Flask, request, jsonify

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


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not 'name' in data or not 'price' in data:
        return jsonify({"error": "Invalid data"}), 400

    product_id = len(products) + 1
    product = Product(id=product_id, name=data['name'], price=data['price'])
    products.append(product)
    return jsonify(product.to_dict()), 201


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([product.to_dict() for product in products])


@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    if not data or not 'product_id' in data or not 'quantity' in data:
        return jsonify({"error": "Invalid data"}), 400

    product_id = data['product_id']
    quantity = data['quantity']

    if not any(product.id == product_id for product in products):
        return jsonify({"error": "Product not found"}), 404

    if product_id in cart:
        cart[product_id].quantity += quantity
    else:
        cart[product_id] = CartItem(product_id=product_id, quantity=quantity)

    return jsonify({"message": "Product added to cart"}), 200


@app.route('/cart', methods=['GET'])
def get_cart():
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
    app.run(debug=True)