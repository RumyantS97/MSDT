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
        self.customerDataLayer = CustomerDataLayer(db)

    def load_company_customer(self, external_id, company_number):
        matches = CustomerMatches()
        match_by_external_id: Customer = self.customerDataLayer.find_by_external_Id(
            external_id)
        if match_by_external_id is not None:
            matches.customer = match_by_external_id
            matches.match_term = "ExternalId"
            match_by_master_id: Customer = self.customerDataLayer.find_by_master_external_id(
                external_id)
            if match_by_master_id is not None:
                matches.add_duplicate(match_by_master_id)
        else:
            match_by_company_number: Customer = self.customerDataLayer.find_by_company_number(
                company_number)
            if match_by_company_number is not None:
                matches.customer = match_by_company_number
                matches.match_term = "CompanyNumber"

        return matches

    def load_person_customer(self, external_id):
        matches = CustomerMatches()
        match_by_personal_number: Customer = self.customerDataLayer.find_by_external_Id(
            external_id)
        matches.customer = match_by_personal_number
        if match_by_personal_number is not None:
            matches.match_term = "ExternalId"
        return matches

    def update_customer_record(self, customer):
        self.customerDataLayer.update_customer_record(customer)

    def create_customer_record(self, customer):
        return self.customerDataLayer.create_customer_record(customer)

    def update_shopping_list(self, customer: Customer,
                             shopping_list: shopping_list):
        customer.add_shopping_list(shopping_list)
        self.customerDataLayer.update_shopping_list(shopping_list)
        self.customerDataLayer.update_customer_record(customer)


class CustomerDataLayer:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def find_by_external_Id(self, external_id):
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, '
            'customerType, companyNumber FROM customers WHERE externalId=?',
            (external_id,))
        customer = self._customer_from_sql_select_fields(
            self.cursor.fetchone())
        return customer

    def _find_addressId(self, customer):
        self.cursor.execute('SELECT addressId FROM customers WHERE '
                            'internalId=?', (customer.internal_id,))
        (address_id,) = self.cursor.fetchone()
        if address_id:
            return int(address_id)
        return None

    def _customer_from_sql_select_fields(self, fields):
        if not fields:
            return None

        customer = Customer(internal_id=fields[0], external_id=fields[1],
                            master_external_id=fields[2], name=fields[3],
                            customer_type=CustomerType(fields[4]),
                            company_number=fields[5])
        address_id = self._find_addressId(customer)
        if address_id:
            self.cursor.execute('SELECT street, city, postalCode FROM '
                                'addresses WHERE addressId=?',
                                (address_id,))
            addresses = self.cursor.fetchone()
            if addresses:
                (street, city, postalCode) = addresses
                address = Address(street, city, postalCode)
                customer.address = address
        self.cursor.execute('SELECT shoppinglistId FROM '
                            'customer_shoppinglists WHERE customerId=?',
                            (customer.internal_id,))
        shopping_lists = self.cursor.fetchall()
        for sl in shopping_lists:
            self.cursor.execute('SELECT products FROM shoppinglists WHERE '
                                'shoppinglistId=?', (sl[0],))
            products_as_str = self.cursor.fetchone()
            products = products_as_str[0].split(", ")
            customer.add_shopping_list(shopping_list(products))
        return customer

    def find_by_master_external_id(self, master_external_id):
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, '
            'customerType, companyNumber FROM customers WHERE '
            'masterExternalId=?',
            (master_external_id,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def find_by_company_number(self, company_number):
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE companyNumber=?',
            (company_number,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def create_customer_record(self, customer):
        customer.internal_id = self._nextid("customers")
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, '
                            '?);', (
                                customer.internal_id, customer.external_id,
                                customer.master_external_id, customer.name,
                                customer.customer_type.value,
                                customer.company_number, None))
        if customer.address:
            address_id = self._nextid("addresses")
            self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                address_id, customer.address.street, customer.address.city,
                customer.address.postal_code))
            self.cursor.execute(
                'UPDATE customers set addressId=? WHERE internalId=?',
                (address_id, customer.internal_id))

        if customer.shopping_lists:
            for sl in customer.shopping_lists:
                data = ", ".join(sl)
                self.cursor.execute(
                    'SELECT shoppinglistId FROM shoppinglists WHERE products=?',
                    (data,))
                shopping_list_id = self.cursor.fetchone()
                if not shopping_list_id:
                    shopping_list_id = self._nextid("shoppinglists")
                    self.cursor.execute(
                        'INSERT INTO shoppinglists VALUES (?, ?)',
                        (shopping_list_id, data))
                self.cursor.execute(
                    'INSERT INTO customer_shoppinglists VALUES (?, ?)',
                    (customer.internal_id, shopping_list_id))
        self.conn.commit()
        return customer

    def _nextid(self, table_name):
        self.cursor.execute(f'SELECT MAX(ROWID) AS max_id FROM {table_name};')
        (id,) = self.cursor.fetchone()
        if id:
            return int(id) + 1
        else:
            return 1

    def update_customer_record(self, customer):
        self.cursor.execute(
            'Update customers set externalId=?, masterExternalId=?, name=?, '
            'customerType=?, companyNumber=? WHERE internalId=?',
            (customer.external_id, customer.master_external_id, customer.name,
             customer.customer_type.value,
             customer.company_number, customer.internal_id))
        if customer.address:
            address_id = self._find_addressId(customer)
            if not address_id:
                address_id = self._nextid("addresses")
                self.cursor.execute(
                    'INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                    address_id, customer.address.street, customer.address.city,
                    customer.address.postal_code))
                self.cursor.execute(
                    'UPDATE customers set addressId=? WHERE internalId=?',
                    (address_id, customer.internal_id))

        self.cursor.execute(
            'DELETE FROM customer_shoppinglists WHERE customerId=?',
            (customer.internal_id,))
        if customer.shopping_lists:
            for sl in customer.shopping_lists:
                products = ", ".join(sl.products)
                self.cursor.execute(
                    'SELECT shoppinglistId FROM shoppinglists WHERE products=?',
                    (products,))
                shopping_list_ids = self.cursor.fetchone()
                if shopping_list_ids is not None:
                    (shopping_list_id,) = shopping_list_ids
                    self.cursor.execute(
                        'INSERT INTO customer_shoppinglists VALUES (?, ?)',
                        (customer.internal_id, shopping_list_id))
                else:
                    shopping_list_id = self._nextid("shoppinglists")
                    self.cursor.execute(
                        'INSERT INTO shoppinglists VALUES (?, ?)',
                        (shopping_list_id, products))
                    self.cursor.execute(
                        'INSERT INTO customer_shoppinglists VALUES (?, ?)',
                        (customer.internal_id, shopping_list_id))

        self.conn.commit()

    def update_shopping_list(self, shopping_list):
        pass
