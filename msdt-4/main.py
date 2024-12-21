import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# Модель продукта
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

# Создание базы данных
@app.before_first_request
def create_tables():
    db.create_all()
    logger.info("База данных создана.")

# Получить всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    logger.info(f"Получено {len(users)} пользователей.")
    return jsonify([user.to_dict() for user in users])

# Добавить нового пользователя
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"Добавлен новый пользователь: {new_user.username} (ID: {new_user.id}).")
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        return jsonify({'message': 'Error adding user'}), 500

# Получить всех продуктов
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    logger.info(f"Получено {len(products)} продуктов.")
    return jsonify([product.to_dict() for product in products])

# Добавить новый продукт
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    try:
        new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
        db.session.add(new_product)
        db.session.commit()
        logger.info(f"Добавлен новый продукт: {new_product.name} (ID: {new_product.id}).")
        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        logger.error(f"Ошибка при добавлении продукта: {e}")
        return jsonify({'message': 'Error adding product'}), 500

# Получить продукт по ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        logger.warning(f"Попытка доступа к несуществующему продукту (ID: {product_id}).")
        return jsonify({'message': 'Product not found'}), 404
    logger.info(f"Получен продукт: {product.name} (ID: {product.id}).")
    return jsonify(product.to_dict())

# Обновить продукт по ID
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    old_name = product.name  # Сохраняем старое имя для логирования
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    logger.info(f"Обновлен продукт: {old_name} -> {product.name} (ID: {product.id}).")
    return jsonify(product.to_dict())

# Удалить продукт по ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    logger.info(f"Удален продукт: {product.name} (ID: {product.id}).")
    return jsonify({'message': 'Product deleted successfully'}), 204

if __name__ == '__main__':
    app.run(debug=True)