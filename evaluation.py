class Evaluation:
    def __init__(self,advertisement_id,evaluation_id,user_fullname,comment,evaluation_date=None,point=None,car_model=None,car_brand=None):
        self.evaluation_id=evaluation_id
        self.user_fullname=user_fullname
        self.comment=comment
        self.evaluation_date=str(evaluation_date).split()[0]
        self.point=point
        self.car_model=car_model
        self.car_brand=car_brand
        self.advertisement_id=advertisement_id
