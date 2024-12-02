from dataclasses import dataclass, field
from typing import List

from model_objects import Customer, ShoppingList, CustomerType, Address


class CustomerMatches:
    """
    Represents a class to hold customer matching information, including potential duplicates.
    """

    def __init__(self):
        """
        Initializes the CustomerMatches object.
        """
        self.matchTerm = None
        self.customer = None
        self.duplicates = []

    def has_duplicates(self):
        """
        Checks if there are any duplicate customers.

        Returns:
            bool: True if there are duplicates, False otherwise.
        """
        return bool(self.duplicates)

    def add_duplicate(self, duplicate):
        """
        Adds a duplicate customer to the list of duplicates.

        Args:
            duplicate (Customer): The duplicate customer to add.
        """
        self.duplicates.append(duplicate)


class CustomerDataAccess:
    """
    Provides methods to interact with customer data, including loading, updating, and creating customer records.
    """

    def __init__(self, db):
        """
        Initializes the CustomerDataAccess object with a database connection.

        Args:
            db: The database connection object.
        """
        self.customerDataLayer = CustomerDataLayer(db)

    def loadCompanyCustomer(self, externalId, companyNumber):
        """
        Loads a company customer by external ID and company number, checking for duplicates.

        Args:
            externalId (str): The external ID of the customer.
            companyNumber (str): The company number of the customer.

        Returns:
            CustomerMatches: An object containing the matched customer and any duplicates.
        """
        matches = CustomerMatches()
        matchByExternalId: Customer = self.customerDataLayer.findByExternalId(externalId)
        if matchByExternalId is not None:
            matches.customer = matchByExternalId
            matches.matchTerm = "ExternalId"
            matchByMasterId: Customer = self.customerDataLayer.findByMasterExternalId(externalId)
            if matchByMasterId is not None:
                matches.add_duplicate(matchByMasterId)
        else:
            matchByCompanyNumber: Customer = self.customerDataLayer.findByCompanyNumber(companyNumber)
            if matchByCompanyNumber is not None:
                matches.customer = matchByCompanyNumber
                matches.matchTerm = "CompanyNumber"

        return matches

    def loadPersonCustomer(self, externalId):
        """
        Loads a person customer by external ID.

        Args:
            externalId (str): The external ID of the customer.

        Returns:
            CustomerMatches: An object containing the matched customer.
        """
        matches = CustomerMatches()
        matchByPersonalNumber: Customer = self.customerDataLayer.findByExternalId(externalId)
        matches.customer = matchByPersonalNumber
        if matchByPersonalNumber is not None:
            matches.matchTerm = "ExternalId"
        return matches

    def updateCustomerRecord(self, customer):
        """
        Updates an existing customer record in the database.

        Args:
            customer (Customer): The customer object to update.
        """
        self.customerDataLayer.updateCustomerRecord(customer)

    def createCustomerRecord(self, customer):
        """
        Creates a new customer record in the database.

        Args:
            customer (Customer): The customer object to create.

        Returns:
            Customer: The created customer object.
        """
        return self.customerDataLayer.createCustomerRecord(customer)

    def updateShoppingList(self, customer: Customer, shoppingList: ShoppingList):
        """
        Updates the shopping list for a customer.

        Args:
            customer (Customer): The customer object.
            shoppingList (ShoppingList): The shopping list to update.
        """
        customer.addShoppingList(shoppingList)
        self.customerDataLayer.updateShoppingList(shoppingList)
        self.customerDataLayer.updateCustomerRecord(customer)


class CustomerDataLayer:
    """
    Provides methods to interact with the database for customer-related operations.
    """

    def __init__(self, conn):
        """
        Initializes the CustomerDataLayer object with a database connection.

        Args:
            conn: The database connection object.
        """
        self.conn = conn
        self.cursor = self.conn.cursor()

    def findByExternalId(self, externalId):
        """
        Finds a customer by their external ID.

        Args:
            externalId (str): The external ID of the customer.

        Returns:
            Customer: The customer object if found, None otherwise.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE externalId=?',
            (externalId,))
        customer = self._customer_from_sql_select_fields(self.cursor.fetchone())
        return customer

    def _find_addressId(self, customer):
        """
        Finds the address ID associated with a customer.

        Args:
            customer (Customer): The customer object.

        Returns:
            int: The address ID if found, None otherwise.
        """
        self.cursor.execute('SELECT addressId FROM customers WHERE internalId=?', (customer.internalId,))
        (addressId,) = self.cursor.fetchone()
        if addressId:
            return int(addressId)
        return None

    def _customer_from_sql_select_fields(self, fields):
        """
        Constructs a Customer object from SQL select fields.

        Args:
            fields (tuple): The fields returned from the SQL query.

        Returns:
            Customer: The constructed customer object.
        """
        if not fields:
            return None
        customer = Customer(internalId=fields[0], externalId=fields[1], masterExternalId=fields[2], name=fields[3],
                            customerType=CustomerType(fields[4]), companyNumber=fields[5])
        addressId = self._find_addressId(customer)
        if addressId:
            self.cursor.execute('SELECT street, city, postalCode FROM addresses WHERE addressId=?',
                                (addressId,))
            addresses = self.cursor.fetchone()
            if addresses:
                (street, city, postalCode) = addresses
                address = Address(street, city, postalCode)
                customer.address = address
        self.cursor.execute('SELECT shoppinglistId FROM customer_shoppinglists WHERE customerId=?',
                            (customer.internalId,))
        shoppinglists = self.cursor.fetchall()
        for sl in shoppinglists:
            self.cursor.execute('SELECT products FROM shoppinglists WHERE shoppinglistId=?', (sl[0],))
            products_as_str = self.cursor.fetchone()
            products = products_as_str[0].split(", ")
            customer.addShoppingList(ShoppingList(products))
        return customer

    def findByMasterExternalId(self, masterExternalId):
        """
        Finds a customer by their master external ID.

        Args:
            masterExternalId (str): The master external ID of the customer.

        Returns:
            Customer: The customer object if found, None otherwise.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE masterExternalId=?',
            (masterExternalId,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def findByCompanyNumber(self, companyNumber):
        """
        Finds a customer by their company number.

        Args:
            companyNumber (str): The company number of the customer.

        Returns:
            Customer: The customer object if found, None otherwise.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE companyNumber=?',
            (companyNumber,))
        return self._customer_from_sql_select_fields(self.cursor.fetchone())

    def createCustomerRecord(self, customer):
        """
        Creates a new customer record in the database.

        Args:
            customer (Customer): The customer object to create.

        Returns:
            Customer: The created customer object.
        """
        customer.internalId = self._nextid("customers")
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?);', (
            customer.internalId, customer.externalId, customer.masterExternalId, customer.name, customer.customerType.value,
            customer.companyNumber, None))
        if customer.address:
            addressId = self._nextid("addresses")
            self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (
                addressId, customer.address.street, customer.address.city, customer.address.postalCode))
            self.cursor.execute('UPDATE customers set addressId=? WHERE internalId=?', (addressId, customer.internalId))

        if customer.shoppingLists:
            for sl in customer.shoppingLists:
                data = ", ".join(sl)
                self.cursor.execute('SELECT shoppinglistId FROM shoppinglists WHERE products=?', (data,))
                shoppinglistId = self.cursor.fetchone()
                if not shoppinglistId:
                    shoppinglistId = self._nextid("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)', (shoppinglistId, data))
                self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)', (customer.internalId, shoppinglistId))
        self.conn.commit()
        return customer

    def _nextid(self, tablename):
        """
        Generates the next ID for a given table.

        Args:
            tablename (str): The name of the table.

        Returns:
            int: The next available ID.
        """
        self.cursor.execute(f'SELECT MAX(ROWID) AS max_id FROM {tablename};')
        (id,) = self.cursor.fetchone()
        if id:
            return int(id) + 1
        else:
            return 1

    def updateCustomerRecord(self, customer):
        """
        Updates an existing customer record in the database.

        Args:
            customer (Customer): The customer object to update.
        """
        self.cursor.execute(
            'UPDATE customers SET externalId=?, masterExternalId=?, name=?, customerType=?, companyNumber=? WHERE internalId=?',
            (customer.externalId, customer.masterExternalId, customer.name, customer.customerType.value,
             customer.companyNumber, customer.internalId))
        if customer.address:
            addressId = self._find_addressId(customer)
            if not addressId:
                addressId = self._nextid("addresses")
                self.cursor.execute('INSERT INTO addresses VALUES (?, ?, ?, ?)', (addressId, customer.address.street, customer.address.city, customer.address.postalCode))
                self.cursor.execute('UPDATE customers SET addressId=? WHERE internalId=?', (addressId, customer.internalId))

        self.cursor.execute('DELETE FROM customer_shoppinglists WHERE customerId=?', (customer.internalId,))
        if customer.shoppingLists:
            for sl in customer.shoppingLists:
                products = ", ".join(sl.products)
                self.cursor.execute('SELECT shoppinglistId FROM shoppinglists WHERE products=?', (products,))
                shoppinglistIds = self.cursor.fetchone()
                if shoppinglistIds is not None:
                    (shoppinglistId,) = shoppinglistIds
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                        (customer.internalId, shoppinglistId))
                else:
                    shoppinglistId = self._nextid("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)', (shoppinglistId, products))
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)', (customer.internalId, shoppinglistId))

        self.conn.commit()

    def updateShoppingList(self, shoppingList):
        """
        Updates a shopping list in the database.

        Args:
            shoppingList (ShoppingList): The shopping list to update.
        """
        pass