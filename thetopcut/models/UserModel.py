from datetime import datetime
class UserModel(object):
    """ A UserModel for creating user object

    Attributes:
        name: 
        password: 
        email: 
        mobile: 
        isTailor: 
        isDesigner: 
        img: 
(default) created_date: current system date.
    """

    def __init__(self, name, password, email, mobile, userType=[], img=[]):
        """Return a new Car object."""
        self.name = name
        self.password = password
        self.email = email
        self.mobile = mobile
        self.userType = userType
        self.img = img
        self.created_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    def to_document(self):
        return self.__dict__

   