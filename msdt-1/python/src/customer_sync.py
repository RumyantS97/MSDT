from dataclasses import dataclass, field
from typing import List

from customer_data_access import customer_matches
from model_objects import Customer, external_customer, CustomerType



class ConflictException(Exception):
    pass


class CustomerSync:

    def __init__(self, customer_data_access):
        self.customer_data_access = customer_data_access

    def syncWithDataLayer(self, external_customer):
        customer_matches: customer_matches
        if external_customer.isCompany:
            customer_matches = self.load_company(external_customer)
        else:
            customer_matches = self.load_person(external_customer)

        customer = customer_matches.customer

        if customer is None:
            customer = Customer()
            customer.external_id = external_customer.external_id
            customer.masterexternal_id = external_customer.external_id

        self.populate_fields(external_customer, customer)

        created = False
        if customer.internalId is None:
            customer = self.create_customer(customer)
            created = True
        else:
            self.update_customer(customer)

        self.update_contact_info(external_customer, customer)

        if customer_matches.has_duplicates:
            for duplicate in customer_matches.duplicates:
                self.update_duplicate(external_customer, duplicate)

        self.update_relations(external_customer, customer)
        self.update_preferred_store(external_customer, customer)

        return created


    def update_relations(self, external_customer: external_customer, customer: Customer):
        consumer_shopping_lists = external_customer.shoppingLists
        for consumer_shopping_list in consumer_shopping_lists:
            self.customer_data_access.updateShoppingList(customer, consumer_shopping_list)


    def update_customer(self, customer):
        return self.customer_data_access.update_customerRecord(customer)


    def update_duplicate(self, external_customer: external_customer, duplicate: Customer):
        if duplicate is None:
            duplicate = Customer()
            duplicate.external_id = external_customer.external_id
            duplicate.masterexternal_id = external_customer.external_id

        duplicate.name = external_customer.name

        if duplicate.internalId is None:
            self.create_customer(duplicate)
        else:
            self.update_customer(duplicate)


    def update_preferred_store(self, external_customer: external_customer, customer: Customer):
        customer.preferredStore = external_customer.preferredStore


    def create_customer(self, customer) -> Customer:
        return self.customer_data_access.create_customerRecord(customer)


    def populate_fields(self, external_customer: external_customer, customer: Customer):
        customer.name = external_customer.name
        if external_customer.isCompany:
            customer.company_number = external_customer.company_number
            customer.customerType = CustomerType.COMPANY
        else:
            customer.customerType = CustomerType.PERSON


    def update_contact_info(self, external_customer: external_customer, customer: Customer):
        customer.address = external_customer.postalAddress


    def load_company(self, external_customer) -> customer_matches:
        external_id = external_customer.external_id
        company_number = external_customer.company_number

        customer_matches = self.customer_data_access.load_companyCustomer(external_id, company_number)

        if customer_matches.customer is not None and CustomerType.COMPANY != customer_matches.customer.customerType:
            raise ConflictException("Existing customer for external_customer {external_id} already exists and is not a company")

        if "external_id" == customer_matches.matchTerm:
            customercompany_number = customer_matches.customer.company_number
            if company_number != customercompany_number:
                customer_matches.customer.masterexternal_id = None
                customer_matches.add_duplicate(customer_matches.customer)
                customer_matches.customer = None
                customer_matches.matchTerm = None

        elif "company_number" == customer_matches.matchTerm:
            customerexternal_id = customer_matches.customer.external_id
            if customerexternal_id is not None and external_id != customerexternal_id:
                raise ConflictException(f"Existing customer for external_customer {company_number} doesn't match external id {external_id} instead found {customerexternal_id}")

            customer = customer_matches.customer
            customer.external_id = external_id
            customer.masterexternal_id = external_id
            customer_matches.addDuplicate(None)

        return customer_matches


    def load_person(self, external_customer):
        external_id = external_customer.external_id

        customer_matches = self.customer_data_access.load_personCustomer(external_id)

        if customer_matches.customer is not None:
            if CustomerType.PERSON != customer_matches.customer.customerType:
                raise ConflictException(f"Existing customer for external_customer {external_id} already exists and is not a person")

            if "external_id" != customer_matches.matchTerm:
                customer = customer_matches.customer
                customer.external_id = external_id
                customer.masterexternal_id = external_id

        return customer_matches
