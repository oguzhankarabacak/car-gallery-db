class Dealer:
    def __init__(self,dealer_id,dealer_name,owner_fullname,is_central,owner_mail,dealer_city,dealer_phone,total_income=0,number_of_cars_sold=0,average_point=0):
        self.dealer_id=dealer_id
        self.dealer_name=dealer_name
        self.owner_fullname=owner_fullname
        self.is_central=is_central if is_central != None else 0
        self.owner_mail=owner_mail
        self.dealer_city=dealer_city
        self.dealer_phone=dealer_phone
        self.total_income=total_income
        self.number_of_cars_sold=number_of_cars_sold
        self.average_point=average_point