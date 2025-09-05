import json
from pydantic import BaseModel
from enum import Enum

class ProductType(str, Enum):
    EDA = "EDA"
    ODEZHDA = "ODEZHDA"


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    type: ProductType

new_product = Product(
    name="Shaurma",
    price=100,
    in_stock=True,
    type=ProductType.EDA,
)

# Сериализуем в жсон
test_json = new_product.model_dump_json()
print(test_json)

# Десиарилизуем в объект Product
test_object = Product.model_validate_json(test_json)
print(test_object)