import re


def find_first_value(string, regex):
    match = re.search(regex, string)
    return match.group() if match else None


def find_all_values(string, regex):
    return re.findall(regex, string, re.DOTALL)


if __name__ == "__main__":
    with open("dns.html", 'r', encoding='utf-8') as file:
        page = file.read()

    cards = find_all_values(page, r'data-id="product"(.*?)</span></div>')
