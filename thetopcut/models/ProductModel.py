from datetime import datetime
class ProductModel(object):
    """ A Product Model for creating Product with info

    Attributes:
        designerId:
        name:
        desc :
        frontTypes :  // [...Ids]
        backTypes:  // [...Ids]
        occassionTypes:  // [...Ids]
        clothTypes:  // [...Ids]
        bodyTypes:  // [...Ids]
        img: // [...Ids]
(default) created_date: current system date.
    """

    def __init__(self, name, desc, designerId=None, frontTypes=[], backTypes=[], occassionTypes=[], clothTypes=[], bodyTypes=[], img=[]):
        """Return a new Car object."""
        self.name = name
        self.desc = desc 
        self.designerId = designerId
        self.frontTypes = frontTypes 
        self.backTypes = backTypes
        self.occassionTypes = occassionTypes
        self.clothTypes = clothTypes
        self.bodyTypes = bodyTypes
        self.img = img
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   