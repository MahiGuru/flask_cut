from datetime import datetime
class TailorModel(object):
    """ A Tailor Model for creating tailor user

    Attributes:
        userid: user will be treated here as tailor if he opted isTailor flag
        name: name or shop name 
        desc:
        contactNumber: // shop number
        alternateNumber: // alternate number
        address: 
        landmark: 
        pincode: 
        location: {
            type: {},
            coordinates: [] // lat, longitude
        },
        products: [] - list out all id which he opted from products,
        designers: [] - list out all the designer that he choosen,
        img: 
(default) created_date: current system date.
    """

    def __init__(self, userid, name, desc, contactNumber, alternateNumber, address, landmark, pincode, locationObj, products, designers, img):
        """Return a new Car object."""
        self.userid = userid
        self.name = name
        self.desc = desc 
        self.contactNumber = contactNumber 
        self.alternateNumber = alternateNumber
        self.address = address
        self.landmark = landmark
        self.pincode = pincode
        self.location = locationObj
        self.products = products
        self.designers = designers
        self.img = img
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   