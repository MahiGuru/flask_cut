from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
# client = MongoClient('mongodb://mongodb:27017/')
db = client.flaskCut
# listout all collections
# pprint.pprint(db.collection_names(include_system_collections=False))

# categorys = db.category
# frontViewTypes = db.frontViewType
# backViewTypes = db.backViewType