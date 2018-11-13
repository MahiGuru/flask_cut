import pprint

def alreadyExists(collection, title):
    print(collection.find({'title': { "$in": [title]}}).count())
    if collection.find({'title': { "$in": [title]}}).count() > 0:
        return True
    else:
        return False