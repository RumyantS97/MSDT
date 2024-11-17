import mysql.connector


def factorial(n):
    if n == 1:
        return 1
    return factorial(n - 1) * n


def check_duplicate(lst):
    return len(lst) != len(set(lst))


def db_connection(client_id):
    result = None
    cnx = mysql.connector.connect(user='root',
                                  password='root',
                                  host='localhost',
                                  database='project')
    cursor = cnx.cursor()
    query = f"SELECT * FROM client WHERE card_id = {client_id};"
    cursor.execute(query)
    for (card_id, name, address, phone) in cursor:
        result = [card_id, name, address, phone]
    cursor.close()
    cnx.close()
    return result


def get_phone_and_address_by_id(client_id):
    result = db_connection(client_id)
    string = f"Phone: {result[3]}, Address: {result[2]}"
    return string


def palindrome(data):
    if data == '':
        raise Exception('empty input')
    return data == data[::-1]


def transpose(a):
    if not a:
        return []
    rows_count = len(a)
    columns_count = len(a[0])
    new_matrix = []
    for j in range(columns_count):
        tmp = []
        for i in range(rows_count):
            tmp.append(a[i][j])
        new_matrix.append(tmp)
    return new_matrix
