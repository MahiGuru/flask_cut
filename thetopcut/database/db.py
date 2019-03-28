import os
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
# client = MongoClient('mongodb://mongodb:27017/')
db = client.flaskCut
# listout all collections
# pprint.pprint(db.collection_names(include_system_collections=False))

# Collection referencess
col_category = db.categorys
col_frontViewType = db.frontViewTypes
col_backViewType = db.backViewTypes
col_clothType = db.clothTypes
col_occassionType = db.occassionTypes
col_bodyType = db.bodyTypes
col_products = db.products
col_users = db.users
col_tailors = db.tailors
col_tailorProductRelation = db.tailorProductRelations
col_designerProductRelation = db.designerProductRelations
col_userType = db.userTypes
col_designers = db.designers
col_rating = db.ratings
col_likes = db.likes