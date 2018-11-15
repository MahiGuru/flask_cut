from pymongo.write_concern import WriteConcern
from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class Category(MongoModel):
    name = fields.CharField()
    description = fields.CharField(max_length=150)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'flask-cut-db'


class FrontViewType(MongoModel):
    category = fields.ReferenceField(Category)
    name = fields.CharField()
    description = fields.CharField(max_length=150)

    class Meta:
        # Text index on content can be used for text search.
        indexes = [IndexModel([('name', TEXT)])]
        write_concern = WriteConcern(j=True)
        connection_alias = 'flask-cut-db'
