from datetime import datetime
class CategoryModel(object):
    """A Category model for creating category obj

    Attributes:
        name: A name representing the category.
        desc: The description will tell you about the category.
        img: copied image names from upload folder 
        created_date: current system date.
    """

    def __init__(self, name, desc, img):
        """Return a new Car object."""
        self.name = name
        self.desc = desc
        self.img = img
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   