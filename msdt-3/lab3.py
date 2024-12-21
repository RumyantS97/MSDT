import re


def get_values(regexp, string):
    matches = re.findall(regexp, string, re.DOTALL)
    return matches


def get_value(regexp, string):
    matcher = re.search(regexp, string, re.DOTALL)
    if matcher:
        return matcher.group(1)
    else:
        return None


if __name__ == "__main__":
    with open("lamoda_page.html", 'r', encoding='utf-8') as file:
        lamoda = file.read()

    category = get_value(r'_categorySelected.*?"page">(.*?)</a', lamoda)
    count_product_in_category = \
        get_value(r'_categorySelected.*?_found_[^>]*?>(.*?)</span', lamoda)

    print(f'Категория: {category}. '
          f'Количество продуктов: {count_product_in_category}')

    cards = get_values(
        r'x-product-card-description(.*?)</span></span>', lamoda)

    for card in cards:
        old_price = get_value(r'_price-old[^>]*?>(.*?)</span', card)
        old_price2 = get_value(r'_price-second-old[^>]*?>(.*?)</span', card)
        price = get_value(r'_price-new[^>]*?>(.*?)</span', card)
        brand = get_value(r'_brand-name[^>]*?>(.*?)</div', card)
        product_name = get_value(r'_product-name[^>]*?>(.*?)</div', card)
        rating = get_value(r'_rating[^>]*?>(.*?)<span', card)
        reviews_count = get_value(r'_reviewsCount[^>]*?>.+?\((.*?)\)', card)

        print(f'Бренд: {brand}; Название: {product_name}; '
              f'Старая цена: {old_price}; Вторая старая цена: {old_price2}; '
              f'Актуальная цена: {price}; рейтинг: {rating}; '
              f'количество отзывов: {reviews_count}')
