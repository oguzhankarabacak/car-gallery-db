class Car:
    def __init__(self,car_id,car_model,car_brand,engine_size=None,car_type=None,horsepower=None,gearbox=None,fuel=None):
        self.car_id=car_id
        self.car_model=car_model
        self.car_brand=car_brand
        self.engine_size=engine_size
        self.car_type=car_type if car_type==None else car_type.capitalize()
        self.horsepower=horsepower
        self.gearbox=gearbox if gearbox==None else gearbox.capitalize()
        self.fuel=fuel if fuel==None else fuel.capitalize()