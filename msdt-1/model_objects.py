from dataclasses import dataclass, field
from typing import List, Optional

from enum import Enum




class CustomerType(Enum):
    PERSON = 1
    COMPANY = 2


@dataclass
class ShoppingList:
    products: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Address:
    street: str
    city: str
    postalCode: str


@dataclass(frozen=True)
class ExternalCustomer:
    externalId: str
    name: str
    isCompany: bool
    companyNumber: Optional[str]
    preferredStore: str
    postalAddress: Address
    shoppingLists: List[ShoppingList] = field(default_factory=list)


class Customer:
    def __init__(self, internal_id: str = None, external_id: str = None, master_external_id: str = None, name: str = None,
                 customer_type: CustomerType = None, company_number: str = None):
        self.internal_id = internal_id
        self.external_id = external_id
        self.master_external_id = master_external_id
        self.name = name
        self.customer_type = customer_type
        self.company_number = company_number
        self.shopping_lists = []
        self.address = None

    def add_shopping_list(self, shopping_list):
        self.shopping_lists.append(shopping_list)