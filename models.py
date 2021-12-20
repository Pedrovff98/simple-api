from mongoengine import Document, StringField, FloatField, ReferenceField


class Product(Document):
    name = StringField(required=True, allow_none=False)
    price = FloatField(required=True, allow_none=False)
    category = ReferenceField('Category', required=True, allow_none=False)


class Category(Document):
    name = StringField(requerid=True, allow_nome=False)
    status = StringField(required=True, allow_nome=False)



