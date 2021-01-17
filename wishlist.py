class Wishlist:
    def __init__(self,user_id,adv_id,date,car_brand,car_model,car_price,car_year):
        self.user_id=user_id
        self.adv_id=adv_id
        self.date=str(date).split()[0]
        self.car_brand=car_brand
        self.car_model=car_model
        self.car_price=car_price
        self.car_year=car_year