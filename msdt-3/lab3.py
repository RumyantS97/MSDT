import re
import csv


def find_first_value(string, regex):
    match = re.search(regex, string, re.DOTALL)
    return match.group(1) if match else None


def find_first_value_without_group(string, regex):
    match = re.search(regex, string, re.DOTALL)
    return match.group() if match else None


def find_all_values(string, regex):
    return re.findall(regex, string, re.DOTALL)


class Product:
    def __init__(self, card):
        self.price = find_first_value(card, r'product-buy__price">(.*?)&')
        self.payment = find_first_value(card, r'product-buy__sub">от (.*?)&')
        self.rating = find_first_value(
            card, r'catalog-product__rating.*?b>([\d.]+).*?</b')
        self.is_sales_stopped = (find_first_value_without_group(
            card, r'Продажи прекращены') is not None)
        self.description = find_first_value(card, r'span>(.*?)</span')
        self.name = find_first_value_without_group(
            self.description, r'Стиральн.+?машина[a-zA-Z0-9 /-]+')
        self.turn = find_first_value(self.description, r'([\d]+?) об/мин')

    def to_dict(self):
        return {"price": self.price, "payment": self.payment,
                "rating": self.rating, "name": self.name,
                "is_sales_stopped": self.is_sales_stopped,
                "description": self.description, "turn": self.turn}


def to_csv_file(file_name, products_):
    with open(file_name, 'w', newline='', encoding="utf-8") as file:
        fieldnames = ["name", "price", "payment", "rating", "turn",
                      "is_sales_stopped", "description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for product_ in products_:
            writer.writerow(product_.to_dict())


if __name__ == "__main__":
    with open("dns.html", 'r', encoding='utf-8') as file:
        page = file.read()

    category_name = find_first_value(page, r'Поиск по категории: (.*?)<')
    product_list = find_first_value(
        page, r'class="products-list (.*?)pagination-container')
    cards = find_all_values(
        product_list,
        r'data-id="product".*?product-buy__price-wrap.*?</div></div>')

    products = []
    for card in cards:
        products.append(Product(card))
        product = products[len(products)-1]
        print(f'{product.name}\t'
              f'{product.rating}\t'
              f'{product.price}\t'
              f'{product.payment}\t'
              f'{product.is_sales_stopped}\t'
              f'{product.turn}\t'
              f'{product.description}\t')

    print(category_name)
    to_csv_file(f'{category_name}.csv', products)
