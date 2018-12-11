from datetime import datetime
class TailorProductRelationModel(object):
    """ A Designer Model for creating tailor user

    Attributes:
        userid: user will be treated here as tailor if he opted isTailor flag
        productId: int
        tailorId: int
(default) created_date: current system date.
    """

    def __init__(self, userid, productid, tailorid):
        """Return a new Car object."""
        self.userId = userid
        self.productId = productid
        self.tailorId = tailorid

        
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   