import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

class Order:
    def __init__(self, order_id, customer_name, amount, items):
        self.order_id = order_id
        self.customer_name = customer_name
        self.amount = amount
        self.items = items
        self.status = "Created"
        self.shipping_address = ""
        self.payment_status = "Pending"
        self.is_delivered = False
        logging.info(f"Order {self.order_id} created for {self.customer_name} with items {self.items}.")

    def update_status(self, new_status):
        old_status = self.status
        self.status = new_status
        logging.info(f"Order {self.order_id} status updated from {old_status} to {new_status}.")

    def set_shipping_address(self, address):
        self.shipping_address = address
        logging.info(f"Shipping address for order {self.order_id} set to: {address}.")

    def process_payment(self):
        if self.amount > 0:
            self.payment_status = "Paid"
            logging.info(f"Payment of {self.amount} for order {self.order_id} processed successfully.")
        else:
            logging.error(f"Invalid payment amount for order {self.order_id}. Payment failed.")

    def ship_order(self):
        if self.status == "Paid" and not self.is_delivered:
            self.update_status("Shipped")
            self.is_delivered = True
            logging.info(f"Order {self.order_id} shipped.")
        else:
            logging.warning(f"Order {self.order_id} cannot be shipped. Either not paid or already shipped.")

    def cancel_order(self):
        if self.status != "Shipped":
            self.update_status("Cancelled")
            logging.info(f"Order {self.order_id} cancelled.")
        else:
            logging.warning(f"Order {self.order_id} cannot be cancelled. It is already shipped.")

    def delete(self):
        logging.info(f"Order {self.order_id} deleted.")
        del self


class OrderSystem:
    def __init__(self):
        self.orders = {}

    def create_order(self, order_id, customer_name, amount, items):
        order = Order(order_id, customer_name, amount, items)
        self.orders[order_id] = order
        logging.info(f"Order {order_id} created for {customer_name}.")

    def update_order(self, order_id, new_status):
        if order_id in self.orders:
            self.orders[order_id].update_status(new_status)
        else:
            logging.warning(f"Order {order_id} not found for update.")

    def set_shipping_address(self, order_id, address):
        if order_id in self.orders:
            self.orders[order_id].set_shipping_address(address)
        else:
            logging.warning(f"Order {order_id} not found for setting shipping address.")

    def process_payment_for_order(self, order_id):
        if order_id in self.orders:
            self.orders[order_id].process_payment()
        else:
            logging.warning(f"Order {order_id} not found for payment processing.")

    def ship_order(self, order_id):
        if order_id in self.orders:
            self.orders[order_id].ship_order()
        else:
            logging.warning(f"Order {order_id} not found for shipment.")

    def cancel_order(self, order_id):
        if order_id in self.orders:
            self.orders[order_id].cancel_order()
        else:
            logging.warning(f"Order {order_id} not found for cancellation.")

    def delete_order(self, order_id):
        if order_id in self.orders:
            self.orders[order_id].delete()
            del self.orders[order_id]
            logging.info(f"Order {order_id} deleted from system.")
        else:
            logging.warning(f"Order {order_id} not found for deletion.")


# Пример работы системы с логированием
system = OrderSystem()
system.create_order(1, "John Doe", 100, ["item1", "item2", "item3"])
system.create_order(2, "Jane Smith", 150, ["item4", "item5"])

system.set_shipping_address(1, "123 Elm St, Springfield, IL")
system.set_shipping_address(2, "456 Oak St, Shelbyville, IL")

system.process_payment_for_order(1)
system.process_payment_for_order(2)

system.ship_order(1)
system.ship_order(2)

system.cancel_order(1)
system.delete_order(1)
system.delete_order(2)
system.delete_order(3)