from dataclasses import dataclass, field
from typing import List

from model_objects import Customer, ShoppingList, CustomerType, Address


class CustomerMatches:
    def __init__(self):
        self.match_term = None
        self.customer = None
        self.duplicates = []

    def has_duplicates(self):
        return self.duplicates

    def add_duplicate(self, duplicate):
        self.duplicates.append(duplicate)


class CustomerDataAccess:
    def __init__(self, db):
        self.customer_data_layer = CustomerDataLayer(db)

    def load_company_customer(self, external_id, company_number):
        matches = customer_matches()
        match_by_external_id: Customer = self.customer_data_layer.find_by_external_id(external_id)
        if match_by_external_id is not None:
            matches.customer = match_by_external_id
            matches.match_term = "ExternalId"
            match_by_master_id: Customer = self.customer_data_layer.find_by_master_external_id(external_id)
            if match_by_master_id is not None:
                matches.add_duplicate(match_by_master_id)
        else:
            match_by_company_number: Customer = self.customer_data_layer.find_by_company_number(company_number)
            if match_by_company_number is not None:
                matches.customer = match_by_company_number
                matches.match_term = "CompanyNumber"

        return matches

    def load_person_customer(self, external_id):
        matches = customer_matches()
        match_by_personal_number: Customer = self.customer_data_layer.find_by_external_id(external_id)
        matches.customer = match_by_personal_number
        if match_by_personal_number is not None:
            matches.match_term = "ExternalId"
        return matches

    def update_customer_record(self, customer):
        self.customer_data_layer.update_customer_record(customer)

    def create_customer_record(self, customer):
        return self.customer_data_layer.create_customer_record(customer)

    def update_shopping_list(self, customer: Customer, shopping_list: ShoppingList):
        customer.addShoppingList(shopping_list)
        self.customer_data_layer.update_shopping_list(shopping_list)
        self.customer_data_layer.update_customer_record(customer)


class CustomerDataLayer:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def find_by_external_id(self, external_id):
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, '
            'companyNumber FROM customers WHERE externalId=?',
            (external_id,))
        customer = self.customer_from_sql_select_fields(self.cursor.fetchone())
        return customer

    def find_address_id(self, customer):
        self.cursor.execute('SELECT addressId FROM customers WHERE internalId=?', (customer.internal_id,))
        (addressId,) = self.cursor.fetchone()
        if addressId:
            return int(addressId)
        return None

    def customer_from_sql_select_fields(self, fields):
        if not fields:
            return None

        customer = Customer(internalId=fields[0], externalId=fields[1], masterExternalId=fields[2], name=fields[3],
                            customerType=CustomerType(fields[4]), companyNumber=fields[5])
        address_id = self.find_address_id(customer)
        if address_id:
            self.cursor.execute('SELECT street, city, postalCode FROM addresses WHERE address_id=?',
                                (address_id,))
            addresses = self.cursor.fetchone()
            if addresses:
                (street, city, postalCode) = addresses
                address = Address(street, city, postalCode)
                customer.address = address
        self.cursor.execute('SELECT shoppinglistId FROM customer_shoppinglists WHERE customerId=?',
                            (customer.internal_id,))
        shopping_lists = self.cursor.fetchall()
        for sl in shopping_lists:
            self.cursor.execute('SELECT products FROM shopping_lists WHERE shoppinglistId=?', (sl[0],))
            products_as_str = self.cursor.fetchone()
            products = products_as_str[0].split(", ")
            customer.addShoppingList(ShoppingList(products))
        return customer

    def find_by_master_external_id(self, master_external_id):
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE '
            'masterExternalId=?',
            (master_external_id,))
        return self.customer_from_sql_select_fields(self.cursor.fetchone())

    def find_by_company_number(self, companyNumber):
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE '
            'companyNumber=?',
            (companyNumber,))
        return self.customer_from_sql_select_fields(self.cursor.fetchone())

    def create_customer_record(self, customer):
        customer.internal_id = self.next_id("customers")
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?);', (
            customer.internal_id, customer.external_id, customer.master_external_id, customer.name,
            customer.customer_type.value,
            customer.companyNumber, None))
        if customer.address:
            address_id = self.next_id("addresses")
            self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                address_id, customer.address.street, customer.address.city, customer.address.postalCode))
            self.cursor.execute('UPDATE customers set address_id=? WHERE internalId=?',
                                (address_id, customer.internal_id))

        if customer.shoppingLists:
            for sl in customer.shopping_lists:
                data = ", ".join(sl)
                self.cursor.execute('SELECT shopping_list_id FROM shoppinglists WHERE products=?', (data,))
                shopping_list_id = self.cursor.fetchone()
                if not shopping_list_id:
                    shopping_list_id = self.next_id("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)', (shopping_list_id, data))
                self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                    (customer.internal_id, shopping_list_id))
        self.conn.commit()
        return customer

    def next_id(self, tablename):
        self.cursor.execute(f'SELECT MAX(ROWID) AS max_id FROM {tablename};')
        (id,) = self.cursor.fetchone()
        if id:
            return int(id) + 1
        else:
            return 1

    def update_customer_record(self, customer):
        self.cursor.execute(
            'Update customers set externalId=?, masterExternalId=?, name=?, customerType=?, companyNumber=? WHERE '
            'internalId=?',
            (customer.externalId, customer.masterExternalId, customer.name, customer.customerType.value,
             customer.companyNumber, customer.internal_id))
        if customer.address:
            address_id = self.find_address_id(customer)
            if not address_id:
                address_id = self.next_id("addresses")
                self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                    address_id, customer.address.street, customer.address.city, customer.address.postalCode))
                self.cursor.execute('UPDATE customers set address_id=? WHERE internalId=?',
                                    (address_id, customer.internal_id))

        self.cursor.execute('DELETE FROM customer_shoppinglists WHERE customerId=?', (customer.internal_id,))
        if customer.shoppingLists:
            for sl in customer.shoppingLists:
                products = ", ".join(sl.products)
                self.cursor.execute('SELECT shopping_list_id FROM shoppinglists WHERE products=?', (products,))
                shopping_list_ids = self.cursor.fetchone()
                if shopping_list_ids is not None:
                    (shopping_list_id,) = shopping_list_ids
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                        (customer.internal_id, shopping_list_id))
                else:
                    shopping_list_id = self.next_id("shopping_lists")
                    self.cursor.execute('INSERT INTO shopping_lists VALUES (?, ?)', (shopping_list_id, products))
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                        (customer.internal_id, shopping_list_id))

        self.conn.commit()

    def update_shopping_list(self, shoppingList):
        pass
