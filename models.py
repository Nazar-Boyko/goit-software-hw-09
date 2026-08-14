from mongoengine import Document
from mongoengine.fields import ListField, StringField,DateField,ReferenceField,BooleanField

class Authors(Document):

    fullname = StringField(required = True)
    born_date = DateField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, required=True)
    quote = StringField(required = True)
