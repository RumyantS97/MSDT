import unittest
from msdt_5.code import Product, Order, Shop

class TestProduct(unittest.TestCase):
    def test_product_reduce_stock_success(self):
        product = Product("Laptop", 999.99, 5)
        self.assertTrue(product.reduce_stock(2))
        self.assertEqual(product.stock, 3)

    def test_product_reduce_stock_failure(self):
        product = Product("Laptop", 999.99, 5)
        self.assertFalse(product.reduce_stock(6))
        self.assertEqual(product.stock, 5)

    def test_product_str(self):
        product = Product("Laptop", 999.99, 5)
        self.assertEqual(str(product), "Laptop: $999.99 (5 in stock)")

class TestOrder(unittest.TestCase):
    def test_order_add_product(self):
        product = Product("Laptop", 999.99, 5)
        order = Order()
        order.add_product(product, 2)
        self.assertIn("Laptop", order.items)
        self.assertEqual(order.items["Laptop"]["quantity"], 2)

    def test_order_calculate_total(self):
        product1 = Product("Laptop", 999.99, 5)
        product2 = Product("Mouse", 19.99, 10)
        order = Order()
        order.add_product(product1, 2)
        order.add_product(product2, 3)
        total = order.calculate_total()
        self.assertEqual(total, 2 * 999.99 + 3 * 19.99)

    def test_order_add_product_insufficient_stock(self):
        shop = Shop()
        product = Product("Laptop", 999.99, 5)
        shop.add_product(product)
        order = Order()
        
        with self.assertRaises(ValueError) as context:
            order.add_product(product, 6)
        self.assertEqual(str(context.exception), "Insufficient stock for Laptop")
        self.assertEqual(len(order.items), 0)

class TestShop(unittest.TestCase):
    def test_shop_add_product(self):
        shop = Shop()
        product = Product("Phone", 499.99, 10)
        shop.add_product(product)
        self.assertIn(product, shop.products)

    def test_shop_find_product(self):
        shop = Shop()
        product = Product("Phone", 499.99, 10)
        shop.add_product(product)
        found_product = shop.find_product("Phone")
        self.assertEqual(found_product, product)

    def test_shop_find_product_not_found(self):
        shop = Shop()
        product = Product("Phone", 499.99, 10)
        shop.add_product(product)
        found_product = shop.find_product("Laptop")
        self.assertIsNone(found_product)

    def test_shop_process_order_complex(self):
        shop = Shop()
        product1 = Product("Laptop", 999.99, 5)
        product2 = Product("Mouse", 19.99, 10)
        product3 = Product("Keyboard", 49.99, 7)
        shop.add_product(product1)
        shop.add_product(product2)
        shop.add_product(product3)
        
        order = Order()
        order.add_product(product1, 2)
        order.add_product(product2, 3)
        order.add_product(product3, 1)
        
        shop.process_order(order)
        
        self.assertEqual(product1.stock, 3)
        self.assertEqual(product2.stock, 7)
        self.assertEqual(product3.stock, 6)
        
        total = order.calculate_total()
        self.assertEqual(total, 2 * 999.99 + 3 * 19.99 + 1 * 49.99)
        
        self.assertTrue(order.processed)

if __name__ == "__main__":
    unittest.main()