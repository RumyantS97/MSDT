from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from model_objects import Customer, ShoppingList, CustomerType, Address


class CustomerMatches:
    """
    Represents a class to hold customer matching information, 
    including potential duplicates.
    """

    def __init__(self):
        """
        Initializes the CustomerMatches object.
        """
        self.match_term: Optional[str] = None
        self.customer: Optional[Customer] = None
        self.duplicates: List[Customer] = []

    def has_duplicates(self) -> bool:
        """
        Checks if there are any duplicate customers.

        Returns:
            bool: True if there are duplicates, False otherwise.
        """
        return bool(self.duplicates)

    def add_duplicate(self, duplicate: Customer):
        """
        Adds a duplicate customer to the list of duplicates.

        Args:
            duplicate (Customer): The duplicate customer to add.
        """
        self.duplicates.append(duplicate)


class CustomerDataAccess:
    """
    Provides methods to interact with customer data, including loading, 
    updating, and creating customer records.
    """

    def __init__(self, db):
        """
        Initializes the CustomerDataAccess object with a database connection.

        Args:
            db: The database connection object.
        """
        self.customer_data_layer: CustomerDataLayer = CustomerDataLayer(db)

    def load_company_customer(self, external_id: str, company_number: str)\
          -> CustomerMatches:
        """
        Loads a company customer by external ID and company number, 
        checking for duplicates.

        Args:
            external_id (str): The external ID of the customer.
            company_number (str): The company number of the customer.

        Returns:
            CustomerMatches: An object containing the matched customer
              and any duplicates.
        """
        matches = CustomerMatches()
        match_by_external_id: Optional[Customer] \
            = self.customer_data_layer.find_by_external_id(external_id)
        if match_by_external_id is not None:
            matches.customer = match_by_external_id
            matches.match_term = "ExternalId"
            match_by_master_id: Optional[Customer] \
                = self.customer_data_layer.find_by_master_external_id(external_id)
            if match_by_master_id is not None:
                matches.add_duplicate(match_by_master_id)
        else:
            match_by_company_number: Optional[Customer] \
                = self.customer_data_layer.find_by_company_number(company_number)
            if match_by_company_number is not None:
                matches.customer = match_by_company_number
                matches.match_term = "CompanyNumber"

        return matches

    def load_person_customer(self, external_id: str) -> CustomerMatches:
        """
        Loads a person customer by external ID.

        Args:
            external_id (str): The external ID of the customer.

        Returns:
            CustomerMatches: An object containing the matched customer.
        """
        matches = CustomerMatches()
        match_by_personal_number: Optional[Customer] = \
            self.customer_data_layer.find_by_external_id(external_id)
        matches.customer = match_by_personal_number
        if match_by_personal_number is not None:
            matches.match_term = "ExternalId"
        return matches

    def update_customer_record(self, customer: Customer):
        """
        Updates an existing customer record in the database.

        Args:
            customer (Customer): The customer object to update.
        """
        self.customer_data_layer.update_customer_record(customer)

    def create_customer_record(self, customer: Customer) -> Customer:
        """
        Creates a new customer record in the database.

        Args:
            customer (Customer): The customer object to create.

        Returns:
            Customer: The created customer object.
        """
        return self.customer_data_layer.create_customer_record(customer)

    def update_shopping_list(self, customer: Customer, \
        shopping_list: ShoppingList):
        """
        Updates the shopping list for a customer.

        Args:
            customer (Customer): The customer object.
            shopping_list (ShoppingList): The shopping list to update.
        """
        customer.add_shopping_list(shopping_list)
        self.customer_data_layer.update_shopping_list(shopping_list)
        self.customer_data_layer.update_customer_record(customer)


class CustomerDataLayer:
    """
    Provides methods to interact with the database for 
    customer-related operations.
    """

    def __init__(self, conn):
        """
        Initializes the CustomerDataLayer object with a database connection.

        Args:
            conn: The database connection object.
        """
        self.conn = conn
        self.cursor = self.conn.cursor()

    def find_by_external_id(self, external_id: str) -> Optional[Customer]:
        """
        Finds a customer by their external ID.

        Args:
            external_id (str): The external ID of the customer.

        Returns:
            Optional[Customer]: The customer object if found, None otherwise.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType,\
                  companyNumber FROM customers WHERE externalId=?',
            (external_id,))
        customer = self._customer_from_sql_select_fields(self.cursor.fetchone())
        return customer

    def _find_address_id(self, customer: Customer) -> Optional[int]:
        """
        Finds the address ID associated with a customer.

        Args:
            customer (Customer): The customer object.

        Returns:
            Optional[int]: The address ID if found, None otherwise.
        """
        self.cursor.execute('SELECT addressId FROM customers WHERE internalId=?', \
                            (customer.internal_id,))
        (address_id,) = self.cursor.fetchone()
        if address_id:
            return int(address_id)
        return None

    def _customer_from_sql_select_fields(self, fields: Optional[Tuple])\
          -> Optional[Customer]:
        """
        Constructs a Customer object from SQL select fields.

        Args:
            fields (Optional[Tuple]): The fields returned from the SQL query.

        Returns:
            Optional[Customer]: The constructed customer object.
        """
        if not fields:
            return None
        customer = Customer(internal_id=fields[0], external_id=fields[1], \
                            master_external_id=fields[2], name=fields[3],
                            customer_type=CustomerType(fields[4]), company_number=fields[5])
        address_id = self._find_address_id(customer)
        if address_id:
            self.cursor.execute('SELECT street, city, postalCode\
                                 FROM addresses WHERE addressId=?',
                                (address_id,))
            addresses = self.cursor.fetchone()
            if addresses:
                (street, city, postal_code) = addresses
                address = Address(street, city, postal_code)
                customer.address = address
        self.cursor.execute('SELECT shoppinglistId FROM \
                            customer_shoppinglists WHERE customerId=?',
                            (customer.internal_id,))
        shopping_lists = self.cursor.fetchall()
        for sl in shopping_lists:
            self.cursor.execute('SELECT products FROM shoppinglists \
                                WHERE shoppinglistId=?', (sl[0],))
            products_as_str = self.cursor.fetchone()
            products = products_as_str[0].split(", ")
            customer.add_shopping_list(ShoppingList(products))
        return customer

    def find_by_master_external_id(self, master_external_id: str) \
        -> Optional[Customer]:
        """
        Finds a customer by their master external ID.

        Args:
            master_external_id (str): The master external ID of the customer.

        Returns:
            Optional[Customer]: The customer object if found, None otherwise.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType,\
              companyNumber FROM customers WHERE masterExternalId=?',
            (master_external_id,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def find_by_company_number(self, company_number: str) -> Optional[Customer]:
        """
        Finds a customer by their company number.

        Args:
            company_number (str): The company number of the customer.

        Returns:
            Optional[Customer]: The customer object if found, None otherwise.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType,\
                companyNumber FROM customers WHERE companyNumber=?',
            (company_number,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def create_customer_record(self, customer: Customer) -> Customer:
        """
        Creates a new customer record in the database.

        Args:
            customer (Customer): The customer object to create.

        Returns:
            Customer: The created customer object.
        """
        customer.internal_id = self._next_id("customers")
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?);', (
            customer.internal_id, customer.external_id, customer.master_external_id,\
                  customer.name, customer.customer_type.value,
            customer.company_number, None))
        if customer.address:
            address_id = self._next_id("addresses")
            self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                address_id, customer.address.street, customer.address.city, \
                    customer.address.postal_code))
            self.cursor.execute('UPDATE customers set addressId=? WHERE internalId=?',\
                                 (address_id, customer.internal_id))

        if customer.shopping_lists:
            for sl in customer.shopping_lists:
                data = ", ".join(sl)
                self.cursor.execute('SELECT shoppinglistId FROM shoppinglists \
                                    WHERE products=?', (data,))
                shopping_list_id = self.cursor.fetchone()
                if not shopping_list_id:
                    shopping_list_id = self._next_id("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)',\
                                         (shopping_list_id, data))
                self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)', \
                                    (customer.internal_id, shopping_list_id))
        self.conn.commit()
        return customer

    def _next_id(self, table_name: str) -> int:
        """
        Generates the next ID for a given table.

        Args:
            table_name (str): The name of the table.

        Returns:
            int: The next available ID.
        """
        self.cursor.execute(f'SELECT MAX(ROWID) AS max_id FROM {table_name};')
        (id,) = self.cursor.fetchone()
        if id:
            return int(id) + 1
        else:
            return 1

    def update_customer_record(self, customer: Customer):
        """
        Updates an existing customer record in the database.

        Args:
            customer (Customer): The customer object to update.
        """
        self.cursor.execute(
            'UPDATE customers SET externalId=?, masterExternalId=?, name=?,\
                  customerType=?, companyNumber=? WHERE internalId=?',
            (customer.external_id, customer.master_external_id, customer.name, \
             customer.customer_type.value,
             customer.company_number, customer.internal_id))
        if customer.address:
            address_id = self._find_address_id(customer)
            if not address_id:
                address_id = self._next_id("addresses")
                self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', 
                    (address_id, customer.address.street, customer.address.city, \
                     customer.address.postal_code))
                self.cursor.execute('UPDATE customers SET addressId=? WHERE internalId=?',
                                     (address_id, customer.internal_id))

        self.cursor.execute('DELETE FROM customer_shoppinglists WHERE customerId=?', \
                            (customer.internal_id,))
        if customer.shopping_lists:
            for sl in customer.shopping_lists:
                products = ", ".join(sl.products)
                self.cursor.execute('SELECT shoppinglistId FROM \
                                    shoppinglists WHERE products=?', (products,))
                shopping_list_ids = self.cursor.fetchone()
                if shopping_list_ids is not None:
                    (shopping_list_id,) = shopping_list_ids
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                        (customer.internal_id, shopping_list_id))
                else:
                    shopping_list_id = self._next_id("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)', 
                                        (shopping_list_id, products))
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                         (customer.internal_id, shopping_list_id))

        self.conn.commit()

    def update_shopping_list(self, shopping_list: ShoppingList):
        """
        Updates a shopping list in the database.

        Args:
            shopping_list (ShoppingList): The shopping list to update.
        """
        pass