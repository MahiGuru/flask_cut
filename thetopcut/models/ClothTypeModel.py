from datetime import datetime
class ClothTypeModel(object):
    """A Cloth model for creating cloth type

    Attributes:
        type: A name representing the Front View Type.
        desc: The description will tell you about the type.
        img: copied image names from upload folder 
        created_date: current system date.
    """

    def __init__(self, name, desc, categoryId, img):
        """Return a new Car object."""
        self.type = name
        self.desc = desc
        self.img = img
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   