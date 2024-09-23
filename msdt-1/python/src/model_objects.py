from dataclasses import dataclass, field
from typing import List, Optional

from enum import Enum

from dataclasses_json import dataclass_json


class customer_type(Enum):
    PERSON = 1
    COMPANY = 2

@dataclass_json
@dataclass
class ShoppingList:
    products: List[str] = field(default_factory=list)

@dataclass_json
@dataclass(frozen=True)
class Address:

    street: str
    city: str
    postal_code: str

@dataclass_json
@dataclass(frozen=True)
class ExternalCustomer:

    external_id: str
    name: str
    is_company: bool
    company_number: Optional[str]
    preferred_store: str
    postal_address: Address
    shopping_lists: List[ShoppingList] = field(default_factory=list)


class Customer:
    
    def __init__(self, internal_id: str = None, external_id: str = None, masterexternal_id: str = None, name: str = None, customer_type: customer_type = None, company_number: str = None):
        self.internal_id = internal_id
        self.external_id = external_id
        self.masterexternal_id = masterexternal_id
        self.name = name
        self.customer_type = customer_type
        self.company_number = company_number
        self.shopping_lists = []
        self.address = None

    def addShoppingList(self, shoppingList):
        self.shopping_lists.append(shoppingList)
