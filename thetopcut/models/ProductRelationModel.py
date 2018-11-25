from datetime import datetime
class ProductRelationModel(object):
    """ A Designer Model for creating tailor user

    Attributes:
        userid: user will be treated here as tailor if he opted isTailor flag
        productId: []
        tailorId: []
        designerId: []
        img: 
(default) created_date: current system date.
    """

    def __init__(self, userid=[], productid=[], designerid=[], tailorid=[]):
        """Return a new Car object."""
        self.userId = userid
        self.productId = productid
        self.designerId = designerid
        self.tailorId = tailorid

        
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   