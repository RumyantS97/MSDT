from dataclasses import dataclass, field
from typing import List

from model_objects import Customer, shopping_list, CustomerType, Address


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
        self.customer_data_layer = customer_data_layer(db)

    def load_company_customer(self, external_id, company_number):
        matches = CustomerMatches()
        match_by_external_id: Customer = self.customer_data_layer.find_by_external_id(external_id)
        if match_by_external_id is not None:
            matches.customer = match_by_external_id
            matches.match_term = "external_id"
            match_by_master_id: Customer = self.customer_data_layer.find_by_master_external_id(external_id)
            if match_by_master_id is not None:
                matches.add_duplicate(match_by_master_id)
        else:
            match_by_company_number: Customer = self.customer_data_layer.find_by_company_number(company_number)
            if match_by_company_number is not None:
                matches.customer = match_by_company_number
                matches.match_term = "company_number"

        return matches

    def load_person_customer(self, external_id):
        matches = CustomerMatches()
        match_by_personal_number: Customer = self.customer_data_layer.find_by_external_id(external_id)
        matches.customer = match_by_personal_number
        if match_by_personal_number is not None:
            matches.match_term = "external_id"
        return matches

    def update_customer_record(self, customer):
        self.customer_data_layer.update_customer_record(customer)

    def create_customer_record(self, customer):
        return self.customer_data_layer.create_customer_record(customer)

    def update_shopping_list(self, customer: Customer, shopping_list: shopping_list):
        customer.addshopping_list(shopping_list)
        self.customer_data_layer.update_shopping_list(shopping_list)
        self.customer_data_layer.update_customer_record(customer)


class customer_data_layer:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def find_by_external_id(self, external_id):
        self.cursor.execute(
            'SELECT internalId, external_id, masterexternal_id, name, customerType, company_number FROM customers WHERE external_id=?',
            (external_id,))
        customer = self._customer_from_sql_select_fields(self.cursor.fetchone())
        return customer

    def _find_address_id(self, customer):
        self.cursor.execute('SELECT address_id FROM customers WHERE internalId=?', (customer.internalId,))
        (address_id,) = self.cursor.fetchone()
        if address_id:
            return int(address_id)
        return None

    def _customer_from_sql_select_fields(self, fields):
        if not fields:
            return None

        customer = Customer(internalId=fields[0], external_id=fields[1], masterexternal_id=fields[2], name=fields[3],
                        customerType=CustomerType(fields[4]), company_number=fields[5])
        address_id = self._find_address_id(customer)
        if address_id:
            self.cursor.execute('SELECT street, city, postal_code FROM addresses WHERE address_id=?',
                                          (address_id, ))
            addresses = self.cursor.fetchone()
            if addresses:
                (street, city, postal_code) = addresses
                address = Address(street, city, postal_code)
                customer.address = address
        self.cursor.execute('SELECT shopping_list_id FROM customer_shopping_lists WHERE customerId=?', (customer.internalId,))
        shopping_lists = self.cursor.fetchall()
        for sl in shopping_lists:
            self.cursor.execute('SELECT products FROM shopping_lists WHERE shopping_list_id=?', (sl[0],))
            products_as_str = self.cursor.fetchone()
            products = products_as_str[0].split(", ")
            customer.addshopping_list(shopping_list(products))
        return customer

    def find_by_master_external_id(self, masterexternal_id):
        self.cursor.execute(
            'SELECT internalId, external_id, masterexternal_id, name, customerType, company_number FROM customers WHERE masterexternal_id=?',
            (masterexternal_id,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def find_by_company_number(self, company_number):
        self.cursor.execute(
            'SELECT internalId, external_id, masterexternal_id, name, customerType, company_number FROM customers WHERE company_number=?',
            (company_number,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def create_customer_record(self, customer):
        customer.internalId = self._nextid("customers")
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?);', (
        customer.internalId, customer.external_id, customer.masterexternal_id, customer.name, customer.customerType.value,
        customer.company_number, None))
        if customer.address:
            address_id = self._nextid("addresses")
            self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                address_id, customer.address.street, customer.address.city, customer.address.postal_code))
            self.cursor.execute('UPDATE customers set address_id=? WHERE internalId=?', (address_id, customer.internalId))

        if customer.shopping_lists:
            for sl in customer.shopping_lists:
                data = ", ".join(sl)
                self.cursor.execute('SELECT shopping_list_id FROM shopping_lists WHERE products=?', (data,))
                shopping_list_id = self.cursor.fetchone()
                if not shopping_list_id:
                    shopping_list_id = self._nextid("shopping_lists")
                    self.cursor.execute('INSERT INTO shopping_lists VALUES (?, ?)', (shopping_list_id, data))
                self.cursor.execute('INSERT INTO customer_shopping_lists VALUES (?, ?)', (customer.internalId, shopping_list_id))
        self.conn.commit()
        return customer

    def _nextid(self, tablename):
        self.cursor.execute(f'SELECT MAX(ROWID) AS max_id FROM {tablename};')
        (id,) = self.cursor.fetchone()
        if id:
            return int(id) + 1
        else:
            return 1

    def update_customer_record(self, customer):
        self.cursor.execute(
            'Update customers set external_id=?, masterexternal_id=?, name=?, customerType=?, company_number=? WHERE internalId=?',
            (customer.external_id, customer.masterexternal_id, customer.name, customer.customerType.value,
                customer.company_number, customer.internalId))
        if customer.address:
            address_id = self._find_address_id(customer)
            if not address_id:
                address_id = self._nextid("addresses")
                self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (address_id, customer.address.street, customer.address.city, customer.address.postal_code))
                self.cursor.execute('UPDATE customers set address_id=? WHERE internalId=?', (address_id, customer.internalId))

        self.cursor.execute('DELETE FROM customer_shopping_lists WHERE customerId=?', (customer.internalId,))
        if customer.shopping_lists:
            for sl in customer.shopping_lists:
                products = ", ".join(sl.products)
                self.cursor.execute('SELECT shopping_list_id FROM shopping_lists WHERE products=?', (products,))
                shopping_list_ids = self.cursor.fetchone()
                if shopping_list_ids is not None:
                    (shopping_list_id,) = shopping_list_ids
                    self.cursor.execute('INSERT INTO customer_shopping_lists VALUES (?, ?)',
                                        (customer.internalId, shopping_list_id))
                else:
                    shopping_list_id = self._nextid("shopping_lists")
                    self.cursor.execute('INSERT INTO shopping_lists VALUES (?, ?)', (shopping_list_id, products))
                    self.cursor.execute('INSERT INTO customer_shopping_lists VALUES (?, ?)', (customer.internalId, shopping_list_id))

        self.conn.commit()

    def update_shopping_list(self, shopping_list):
        pass
