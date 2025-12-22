from mongoengine import Document, StringField, DateTimeField, IntField
from datetime import datetime

from mongoengine import FloatField, BooleanField, ReferenceField
from mongoengine import BooleanField, DateField, IntField, EmbeddedDocumentField
from mongoengine import EmbeddedDocument, EmbeddedDocumentField

class Profile(Document):
    user_id = IntField(required=True, unique=True)  # Django User ID
    date_modified = DateTimeField(default=datetime.utcnow)
    phone = StringField(max_length=20)
    address1 = StringField(max_length=200)
    address2 = StringField(max_length=200)
    city = StringField(max_length=200)
    state = StringField(max_length=200)
    zipcode = StringField(max_length=200)
    country = StringField(max_length=200)

    meta = {"collection": "profiles"}

class Category(Document):
    name = StringField(max_length=100, required=True)

    meta = {"collection": "categories"}

   


class Customer(Document):
    first_name = StringField(max_length=20, required=True)
    last_name = StringField(max_length=20, required=True)
    email = StringField(max_length=100, required=True, unique=True)
    password = StringField(max_length=100)
    phone = StringField(max_length=20)

    meta = {"collection": "customers"}



class Product(Document):
    name = StringField(max_length=50, required=True)
    price = FloatField(default=0)
    category = ReferenceField(Category, required=True)
    description = StringField(max_length=200)
    image = StringField()  # store path or URL
    on_sale = BooleanField(default=False)
    if_sale = FloatField(default=0)

    meta = {"collection": "products"}

class ProductSnapshot(EmbeddedDocument):
    product_id = StringField()
    name = StringField()
    price = FloatField()

class Order(Document):
    customer = ReferenceField(Customer, required=True)
    product = EmbeddedDocumentField(ProductSnapshot)
    quantity = IntField(default=1)
    address = StringField(max_length=100)
    phone = StringField(max_length=20)
    date = DateField(default=datetime.utcnow)
    status = BooleanField(default=False)

    meta = {"collection": "orders"}



# Create your models here.