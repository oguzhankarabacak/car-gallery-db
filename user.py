
class User:
    def __init__(self,user_id,mail,user_fullname,password=None):
        self.user_id=user_id
        self.mail=mail
        self.password=password
        self.user_fullname=user_fullname
    
    def get_id(self):
        return self.user_id
    
    