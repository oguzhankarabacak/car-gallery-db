class Advertisement:
    def __init__(self,dealer_id=None,ad_id=None,dealer_name=None,city=None,price=None,car_model=None,car_brand=None,date=None,year=None,engine_size=None,car_type=None,horsepower=None,gearbox=None,fuel=None,dealer_phone=0,explanation=None,from_admin=None,avg_p=None):
        self.ad_id=ad_id
        self.dealer_name=dealer_name
        self.city=city
        self.car_brand=car_brand
        self.car_model=car_model
        self.horsepower=horsepower
        self.car_type=car_type.capitalize() if car_type!=None else car_type
        self.gearbox=gearbox.capitalize() if gearbox!=None else gearbox
        self.year=year
        self.engine_size=engine_size
        self.fuel=fuel.capitalize() if fuel!=None else fuel
        self.price=price
        self.dealer_phone=dealer_phone
        self.date=str(date).split()[0]
        self.dealer_id=dealer_id
        self.explanation=explanation
        self.from_admin=from_admin
        self.avg_point=avg_p
