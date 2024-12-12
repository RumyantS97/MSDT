import unittest
from unittest.mock import Mock, patch, MagicMock
from parameterized import parameterized
from mode_objects import ProductUnit, Product, Discount
from main import ReceiptPrinter
from reciept import ReceiptItem, Receipt


class TestReceiptPrinter(unittest.TestCase):

    def setUp(self):
        self.printer = ReceiptPrinter()

    def test_print_price(self):
        self.assertEqual(self.printer.print_price(123.456), "123.46")
        self.assertEqual(self.printer.print_price(0.001), "0.00")
        self.assertEqual(self.printer.print_price(-12.34), "-12.34")

    def test_print_quantity(self):
        product_each = Mock(spec=Product, unit=ProductUnit.EACH)
        product_weight = Mock(spec=Product, unit=ProductUnit.KILO)
        item_each = Mock(product=product_each, quantity=5)
        item_weight = Mock(product=product_weight, quantity=2.5)

        self.assertEqual(self.printer.print_quantity(item_each), "5")
        self.assertEqual(self.printer.print_quantity(item_weight), "2.500")

    @parameterized.expand([
        ("Apple", "$0.99", "Apple                              $0.99\n"),
        ("Banana", "$1.50", "Banana                             $1.50\n"),
        ("Orange", "$2.00", "Orange                             $2.00\n"),

    ])
    def test2_format_line_with_whitespace(self, name, value, expected_output):
        result = self.printer.format_line_with_whitespace(name, value)
        self.assertEqual(result, expected_output)

    def test_print_receipt_item(self):
        mock_product = MagicMock(spec=Product)
        mock_product.name = "Apple"
        mock_item = MagicMock(spec=ReceiptItem)

        mock_item.product = mock_product
        mock_item.quantity = 1
        mock_item.total_price = 0.99

        expected_output = "Apple                               0.99\n"
        result = self.printer.print_receipt_item(mock_item)
        self.assertEqual(result, expected_output)

    def test_print_discount(self):
        product = Product(name="Test Product", unit=ProductUnit.EACH)
        discount = Discount(description="Discount on Test", product=product, discount_amount=5.00)
        expected_output = "Discount on Test (Test Product)     5.00\n"
        actual_output = self.printer.print_discount(discount)
        self.assertEqual(expected_output, actual_output)

    def test_present_total(self):
        # Создание мока для Receipt
        receipt_mock = Mock(spec=Receipt)

        # Устанавливаем поведение метода total_price
        receipt_mock.total_price.return_value = 140.00

        expected_output = "Total:                            140.00\n"  # Ожидаемый результат

        self.assertEqual(self.printer.present_total(receipt_mock), expected_output)

    @patch('main.ReceiptPrinter.print_receipt_item')
    @patch('main.ReceiptPrinter.print_discount')
    @patch('main.ReceiptPrinter.present_total')
    def test_print_receipt(self, mock_present_total, mock_print_discount, mock_print_receipt_item):
        receipt = Mock(items=[Mock(), Mock()], discounts=[Mock()], total_price=lambda: 100.0)
        mock_print_receipt_item.side_effect = ["item1\n", "item2\n"]
        mock_print_discount.side_effect = ["discount1\n"]
        mock_present_total.return_value = "Total: 100.00\n"

        expected = "item1\nitem2\ndiscount1\n\nTotal: 100.00\n"
        self.assertEqual(self.printer.print_receipt(receipt), expected)

        mock_print_receipt_item.assert_any_call(receipt.items[0])
        mock_print_receipt_item.assert_any_call(receipt.items[1])
        mock_print_discount.assert_called_once_with(receipt.discounts[0])
        mock_present_total.assert_called_once_with(receipt)


if __name__ == '__main__':
    unittest.main()
