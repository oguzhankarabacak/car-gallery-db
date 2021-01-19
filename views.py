from flask import current_app,render_template,request,redirect,url_for,session,flash
from advertisement import Advertisement
from evaluation import Evaluation
from user import User
from flask_login import login_user
from dealer import Dealer
from functools import wraps
from car import Car
from passlib.hash import sha256_crypt
from wishlist import Wishlist


def home_page():
    db=current_app.config["db"]
    adds=[]
    adds_filter=[]
    cursor=db.cursor()
    cursor.execute("Select * from Car group by car_brand")
    datas=cursor.fetchall()
    cars_=[]
    for data in datas:
        car=Car(data[0],data[1],data[2])
        cars_.append(car)
    
    if request.method == "GET":
        query="""Select * from Advertisements order by advertisement_id desc"""
        cursor.execute(query)
        
        advertisements=cursor.fetchall()
        for advertisement in advertisements:
            query2="""Select dealer_name,dealer_city from Dealer where dealer_id="""+str(advertisement[2])
            cursor.execute(query2)
            dealer=cursor.fetchone()
            
            query3="""Select * from Car where car_id="""+str(advertisement[1])
            cursor.execute(query3)
            car=cursor.fetchone()
            
            new_add=Advertisement(ad_id=advertisement[0],dealer_name=dealer[0],city=dealer[1],price=advertisement[4],date=advertisement[6],car_model=car[1],car_brand=car[2],year=advertisement[5],
                                engine_size=car[3],car_type=car[4],horsepower=car[5],gearbox=car[6],fuel=car[7])
            adds.append(new_add)
            adds_filter.append(new_add)
        
        return render_template("index.html",advertisements=adds,cars=cars_,is_filter=None)
    else: #request.method == "POST"
        car_brands=request.form.getlist("car_brand")
        car_brands_array=[]
        for car in cars_:
           # print(car.car_brand)
            car_brands_array.append(car.car_brand)
        car_brands = tuple(car_brands_array) if len(car_brands)==0 else tuple(car_brands)
        
        car_type_=request.form.getlist("car_type")
        car_type=("sedan","coupe","hatchback","cabrio","station wagon","suv","pickup") if len(car_type_) == 0 else tuple(car_type_)

        min_price=request.form["min_price"]
        min_price= 0 if min_price == ""  else  int(min_price)

        max_price=request.form["max_price"]
        max_price= 1500000 if max_price == ""  else  int(max_price)

        min_year=request.form["min_year"]
        min_year= 1900 if min_year == ""  else  int(min_year)

        max_year=request.form["max_year"]
        max_year= 2022 if max_year == ""  else  int(max_year)

        fuel_=request.form.getlist("fuel")
        fuel=("petrol","diesel","hybrid","electric") if len(fuel_)==0 else tuple(fuel_)

        min_hp=request.form["min_horsepower"]
        min_hp=0 if min_hp == "" else int(min_hp) 

        max_hp=request.form["max_horsepower"]
        max_hp=1500 if max_hp == "" else int(max_hp) 

        min_engine=request.form["min_engine"]
        min_engine=0 if min_engine=="" else int(min_engine)

        max_engine=request.form["max_engine"]
        max_engine=8000 if max_engine == "" else int(max_engine)

        gearbox_=request.form.getlist("gearbox")
        gearbox = ("automatic","manual","semi automatic") if len(gearbox_)==0 else tuple(gearbox_)
        
        query2_f="""Select * from Advertisements,Car where Car.car_id=Advertisements.car_id and Advertisements.price BETWEEN {min_price_} AND {max_price_} and Advertisements.car_year
                BETWEEN {min_year_} AND  {max_year_} and Car.horsepower BETWEEN {min_hp_} AND {max_hp_} and Car.engine_size BETWEEN {min_engine_} AND {max_engine_} and 
                Car.car_brand IN {car_brands_} and Car.car_type IN {car_type_} and Car.fuel IN {fuel_} and Car.gearbox IN {gearbox_} order by advertisement_id desc""".format(min_price_=min_price,
                max_price_=max_price,min_year_=min_year,max_year_=max_year,min_hp_=min_hp,max_hp_=max_hp,min_engine_=min_engine,max_engine_=max_engine,
                car_brands_="('"+str(car_brands[0])+"')" if len(car_brands)==1 else car_brands,
                car_type_="('"+str(car_type[0])+"')" if len(car_type)==1 else car_type,
                fuel_="('"+str(fuel[0])+"')" if len(fuel)==1 else fuel,
                gearbox_="('"+str(gearbox[0])+"')" if len(gearbox)==1 else gearbox)
        cursor.execute(query2_f)
        advertisements_filter=cursor.fetchall()
        new_adds_filter=[]
        for adv in advertisements_filter:
            query3_f="""Select dealer_name,dealer_city from Dealer where dealer_id="""+str(adv[2])
            cursor.execute(query3_f)
            dealer_f=cursor.fetchone()
            new_add_filter=Advertisement(ad_id = adv[0],dealer_name=dealer_f[0],city=dealer_f[1],price=adv[4],date=adv[6],car_model=adv[8],car_brand=adv[9],year=adv[5],
                            engine_size=adv[10],car_type=adv[11],horsepower=adv[12],gearbox=adv[13],fuel=adv[14])
            new_adds_filter.append(new_add_filter)
        return render_template("index.html",advertisements=new_adds_filter,cars=cars_,is_filter=[1])






def ad_detail_page(ad_id):
    if(request.method=="GET"):
        db=current_app.config["db"]
        cursor=db.cursor()
        query="""Select * from Advertisements where advertisement_id="""+str(ad_id)
        cursor.execute(query)
        advertisement=cursor.fetchone()
        if (advertisement == None):
            return redirect(url_for("home_page"))
        query_avg="""Select avg(point) from Evaluation where advertisement_id={adv_id_}""".format(adv_id_=ad_id)
        cursor.execute(query_avg)
        avg_p_d=cursor.fetchone()[0]
        avg_p="{:.2f}".format(avg_p_d) if avg_p_d != None else avg_p_d
        cursor.execute("""Select dealer_name,dealer_city,dealer_phone from Dealer where dealer_id="""+str(advertisement[2]))
        dealer=cursor.fetchone()
        cursor.execute("""Select * from Car where car_id="""+str(advertisement[1]))
        car=cursor.fetchone()
        new_add=Advertisement(dealer_id=advertisement[2],ad_id=advertisement[0],dealer_name=dealer[0],city=dealer[1],price=advertisement[4],date=advertisement[6],car_model=car[1],
                            car_brand=car[2],year=advertisement[5],
                                engine_size=car[3],car_type=car[4],horsepower=car[5],gearbox=car[6],fuel=car[7],dealer_phone=dealer[2],explanation=advertisement[3],avg_p=avg_p)

        cursor.execute("""Select * from Evaluation where advertisement_id="""+str(ad_id))
        evas=cursor.fetchall()
        eva_arr=[]
        is_wish=None
        for eva in evas:
            cursor.execute("""Select * from User where user_id="""+str(eva[1]))
            user=cursor.fetchone()
            new_eva=Evaluation(advertisement_id=eva[2],evaluation_id=eva[0],user_fullname=user[1],comment=eva[3],evaluation_date=eva[5],point=eva[4])
            eva_arr.append(new_eva)
        if session.get("user_id"):
            query_wish="""Select * from Wishlist where advertisement_id={adv_id_} and user_id={user_id_}""".format(adv_id_=ad_id,user_id_=session.get("user_id"))
            cursor.execute(query_wish)
            wish_re=cursor.fetchone()
            if wish_re:
                is_wish=True
        return render_template("detail_page.html",adv=new_add,evas=eva_arr,wish=is_wish)
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        point=request.form["point"]
        comment=request.form["comment"].strip()
        if len(comment)<10:
            flash("Your Comment cannot be less than 10 character.","danger")
            return redirect(url_for("ad_detail_page",ad_id=ad_id))
        query="""Insert into Evaluation(user_id,advertisement_id,comment,point) values(%s,%s,%s,%s)"""
        cursor.execute(query,(session.get("user_id"),ad_id,comment,point))
        db.commit()
        query2="""Select dealer_id from Advertisements where advertisement_id={ad_id_}""".format(ad_id_=ad_id)
        cursor.execute(query2)
        dealer_id=cursor.fetchone()
        query3="""Select avg(Evaluation.point),Advertisements.dealer_id from Advertisements,Evaluation
                    where Evaluation.advertisement_id=Advertisements.advertisement_id and Advertisements.dealer_id=%s
                    group by dealer_id;"""
        cursor.execute(query3,(dealer_id))
        dealer_avg_point=cursor.fetchone()[0]
        query4="""Update Dealer SET average_point={avg_point} where dealer_id={dealer_id_}""".format(avg_point = dealer_avg_point,dealer_id_ = dealer_id[0])
        cursor.execute(query4)
        db.commit()
        return redirect(url_for("ad_detail_page",ad_id=ad_id))

def register():
    db=current_app.config["db"]
    cursor=db.cursor()
    if request.method=="GET":
        if session.get("user_id") or session.get("dealer_id") or session.get("admin"):
            return redirect(url_for("home_page"))
        else:
            return render_template("register.html")
    else: #post method
        email=request.form["email"]
        fullname=request.form["fullname"].strip()
        password=request.form["password"].strip()
        password_confirm=request.form["confirm"]
        if len(fullname) < 4 :
            flash("Your Full Name cannot be less than 4 character.","danger")
            return redirect(url_for("register"))
        if len(password) < 6 :
            flash("Your password cannot be less than 6 character.","danger")
            return redirect(url_for("register"))
        if password != password_confirm:
            flash("The password could not be confirmed","danger")
            return redirect(url_for("register"))
        password_h=sha256_crypt.encrypt(password)
        query="Insert into User(user_mail,user_fullname,user_password) values(%s,%s,%s)"
        try:
            t=cursor.execute(query,(email,fullname,password_h))
            y=db.commit()
         #   print("error")
            flash("You have successfully registered, you can login.","success")
            return redirect(url_for("home_page"))
        except:
            flash("This email is registered in the system.","danger")
            return render_template("register.html",message="This email is registered in the system")        

def login_page():
    if request.method == "GET":
        if (session.get("user_id")!= None or session.get("dealer_id")!=None):  #zaten giriş yapılmış
            return redirect(url_for("home_page"))
        return render_template("login.html")
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        email=request.form["email"]
        password=request.form["password"]
        login_type=request.form["login_type"]
        if(login_type == "Dealer"):
            query_deal="""Select * from Dealer where owner_mail='{email_}'""".format(email_=email)
            cursor.execute(query_deal)
            data_d=cursor.fetchone()
            if (data_d != None):
                dealer_pass=data_d[6]
              #  print("------------------",data_d)
                if sha256_crypt.verify(password,dealer_pass) == True:
                    
                    dealer=Dealer(data_d[0],data_d[1],data_d[2],data_d[3],data_d[4],data_d[5],data_d[7],data_d[8],data_d[9],data_d[10])
                    session["logged_in"]=True
                    session['dealer_id']=dealer.dealer_id
                    if dealer.is_central == 1:
                        session["admin"]=dealer.dealer_id
                    flash("Welcome Dealer","success")
                    return redirect(url_for("home_page"))
                else:
                    flash("Invalid Password For Dealer","danger")
                    return render_template("login.html",message="Invalid Password For Dealer") 
            else:
                flash("Invalid Email For Dealer","danger")
                return render_template("login.html",message="Invalid Email For Dealer")
        elif(login_type=="User"):
            query="""Select * from User where user_mail='{email_}'""".format(email_=email)
            cursor.execute(query)
            data=cursor.fetchone()
            if data!=None:
                r_password=data[3]
                if sha256_crypt.verify(password,r_password) == True:
                    user=User(data[0],email,password,data[1])
                    session["logged_in"]=True
                    session['user_id']=user.user_id
                    flash("Welcome User","success")
                    return redirect(url_for("home_page"))
                else:
                    flash("Invalid Password For User","danger")
                    return render_template("login.html")
            else:
                flash("Invalid Email For User","danger")
                return render_template("login.html")

def dealer_page():
    db=current_app.config["db"]
    dealers_=[]
    cursor=db.cursor()
    query="""Select * from Dealer"""
    cursor.execute(query)
    datas=cursor.fetchall()
    for data in datas:
        de=Dealer(data[0],data[1],data[2],data[3],data[4],data[5],data[7])
        dealers_.append(de)
       # print(de)
    return render_template("dealer.html",dealers=dealers_)

def dealer_detail_page(dealer_id):
    db=current_app.config["db"]
    add=[]
    cursor=db.cursor()
    query="""Select * from Advertisements where dealer_id={dealer_id_} order by advertisement_id desc""".format(dealer_id_=dealer_id)
    cursor.execute(query)
    datas=cursor.fetchall()
    for advertisement in datas:
        query2="""Select dealer_name,dealer_city from Dealer where dealer_id="""+str(dealer_id)
        cursor.execute(query2)
        dealer=cursor.fetchone()
        
        query3="""Select * from Car where car_id="""+str(advertisement[1])
        cursor.execute(query3)
        car=cursor.fetchone()
        
        new_add=Advertisement(ad_id=advertisement[0],dealer_name=dealer[0],city=dealer[1],price=advertisement[4],date=advertisement[6],car_model=car[1],car_brand=car[2],year=advertisement[5],
                            engine_size=car[3],car_type=car[4],horsepower=car[5],gearbox=car[6],fuel=car[7])
        add.append(new_add)
    
    
    return render_template("index.html",advertisements=add)

def logout():
    dealer_id=session.get("dealer_id")
    user_id=session.get("user_id")
    admin=session.get("admin")
    if dealer_id != None:
        session.pop('dealer_id')
        if admin != None:
            session.pop("admin")
        flash("You have successfully logged out.","info")
        return redirect(url_for('home_page'))
    elif user_id != None:
        session.pop('user_id')
        flash("You have successfully logged out.","info")
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page'))


  
def login_required_dealer(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get("dealer_id") != None:
            return f(*args,**kwargs)
        else:  
            flash("Please Dealer login","danger")
            return redirect(url_for("login_page"))
    return decorated_function

def login_required_user(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get("user_id") != None or session.get("admin") != None:
            return f(*args,**kwargs)
        else: 
            flash("Please User login","danger")
            return redirect(url_for("login_page"))
    return decorated_function

@login_required_dealer
def my_advertisement():
    add=[]
    dealer_id=session.get("dealer_id")
    db=current_app.config["db"]
    advertisemets_=[]
    cursor=db.cursor()
    query="""Select * from Advertisements where dealer_id='{dealer_id_}' order by advertisement_id desc """.format(dealer_id_=dealer_id)
    cursor.execute(query)
    advertisements=cursor.fetchall()
    for advertisement in advertisements:
        query2="""Select dealer_name,dealer_city from Dealer where dealer_id="""+str(advertisement[2])
        cursor.execute(query2)
        dealer=cursor.fetchone()
        query3="""Select * from Car where car_id="""+str(advertisement[1])
        cursor.execute(query3)
        car=cursor.fetchone()
        new_add=Advertisement(ad_id=advertisement[0],dealer_name=dealer[0],city=dealer[1],price=advertisement[4],date=advertisement[6],car_model=car[1],car_brand=car[2],year=advertisement[5],
                            engine_size=car[3],car_type=car[4],horsepower=car[5],gearbox=car[6],fuel=car[7])
        add.append(new_add)
    return render_template("myadvertisements.html",advertisements=add)

@login_required_dealer
def update_add(ad_id):
    if request.method == "GET":
        db=current_app.config["db"]
        cursor=db.cursor()
        try:
            query="""Select car_id,dealer_id,price,car_year,explanation from Advertisements where advertisement_id='{ad_id_}'""".format(ad_id_=ad_id)
            cursor.execute(query)
            add=cursor.fetchone()
            if (session.get('dealer_id')!=add[1] or add == None) and session.get('admin') != 1:
                return redirect(url_for("my_advertisement"))
            else:
                cursor2=db.cursor()
                query2="""Select car_model,car_brand from Car where car_id='{car_id_}'""".format(car_id_=add[0])
                cursor2.execute(query2)
                car=cursor2.fetchone()
                add_f=Advertisement(car_brand=car[1],car_model=car[0],price=add[2],year=add[3],explanation=add[4])
                return render_template("update.html",advertisement=add_f)
        except:
            flash("No Advertisement","danger")
            return redirect(url_for("my_advertisement"))
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        year=request.form["year"]
        price=request.form["price"]
        explanation=request.form["explanation"].strip()
        if len(explanation)<20:
            flash("Your Explanation cannot be less than 20 character.","danger")
            return redirect(url_for('update_add',ad_id=ad_id))
      #  print(explanation)
        query="""Update Advertisements SET car_year=%s,price=%s,explanation=%s where advertisement_id=%s"""
        cursor.execute(query,(year,price,explanation,ad_id))
        db.commit()
        flash("Advertisement has been updated successfully.","primary")
        if (session.get("admin")):
            return redirect(url_for("admin_page"))
        return redirect(url_for("my_advertisement"))

@login_required_dealer
def delete_add(ad_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select dealer_id from Advertisements where advertisement_id='{ad_id_}'""".format(ad_id_=ad_id)
    try:
        cursor.execute(query)
        add=cursor.fetchone()
        if (session.get('dealer_id')!=add[0] or add == None) and session.get('admin') != 1:
            return redirect(url_for("my_advertisement"))
        else:
            query2="""Delete from Advertisements Where advertisement_id = %s """
            cursor.execute(query2,(ad_id,))
            db.commit()
            flash("Advertisement has been deleted successfully.","primary")
            if (session.get("admin")):
                return redirect(url_for("admin_page"))
            return redirect(url_for("my_advertisement"))
    except:
            flash("No advertisement.","danger")
            return redirect(url_for("my_advertisement"))

@login_required_dealer
def sold_add(ad_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select dealer_id,price from Advertisements where advertisement_id='{ad_id_}'""".format(ad_id_=ad_id)
    try:
        cursor.execute(query)
        add=cursor.fetchone()
        if session.get('dealer_id')!=add[0] or add == None:
            return redirect(url_for("my_advertisement"))
        else:
            query2="""Delete from Advertisements Where advertisement_id = %s """
            cursor.execute(query2,(ad_id,))
            db.commit()
            query3="""Update Dealer SET total_income=(total_income+%s),number_of_cars_sold=(number_of_cars_sold+1) where dealer_id=%s"""
            cursor.execute(query3,(add[1],add[0]))
            db.commit()
            flash("Congratulations! We hope you sell more.","success")
            return redirect(url_for("my_advertisement"))
    except:
        flash("No advertisement.","danger")
        return redirect(url_for("my_advertisement"))

@login_required_user
def my_comments():
    db=current_app.config["db"]
    cursor=db.cursor()
    cursor2=db.cursor()
    user_id=session.get("user_id")
    query="""Select Evaluation.advertisement_id,Evaluation.comment,Evaluation.point,Evaluation.evaluation_date,
                User.user_fullname,Evaluation.evaluation_id from Evaluation inner join User on Evaluation.user_id=User.user_id 
                where User.user_id={user_id_}""".format(user_id_=user_id)
    cursor.execute(query)
    datas=cursor.fetchall()
   # print(datas)
    evas=[]
    for eva in datas:
        query2="""Select Advertisements.advertisement_id,Car.car_model,Car.car_brand from Advertisements inner join Car 
                on Advertisements.car_id=Car.car_id where Advertisements.advertisement_id='{ad_id_}' """.format(ad_id_=eva[0])
        cursor2.execute(query2)
        car=cursor2.fetchone()
      #  print(eva[0])
        eva_=Evaluation(eva[0],eva[5],eva[4],eva[1],eva[3],eva[2],car[1],car[2])
        evas.append(eva_)
     #   print(eva[5],eva[4],eva[1],eva[3],eva[2],car[1],car[2])
    return render_template("mycomments.html",evaluations=evas)

@login_required_user
def delete_comment(eva_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    user_id=session.get("user_id")
    query="""Select user_id from Evaluation where evaluation_id={eva_id_}""".format(eva_id_=eva_id)
  #  print(query)
    cursor.execute(query)
    data=cursor.fetchone()
    if (data==None or data[0] != user_id) and session.get("admin") != 1:
        return redirect(url_for("my_comments"))
    else:
        query2="""Delete from Evaluation Where evaluation_id ={eva_id_} """.format(eva_id_=eva_id)
        cursor.execute(query2)
        db.commit()
        flash("Comment has been deleted successfully.","primary")
        if (session.get("admin")):
            return redirect(url_for("admin_page"))
        return redirect(url_for("my_comments"))

@login_required_dealer
def new_advertisement():
    db=current_app.config["db"]
    cursor=db.cursor()
    cars_=[]
    dealer_id=session.get("dealer_id")
    if request.method=="GET":
        query="""Select car_id,car_model,car_brand from Car"""
        cursor.execute(query)
        datas=cursor.fetchall()
        for data in datas:
            car=Car(car_id=data[0],car_model=data[1],car_brand=data[2])
            cars_.append(car)
        return render_template("newadvertisement.html",cars=cars_)
    else:  #post request
        year=request.form["year"]
        price=request.form["price"]
        car_id=request.form["car_name"]
        explanation=request.form["explanation"].strip()
        if len(explanation) < 20:
            flash("Your Explanation cannot be less than 20 character.","danger")
            return redirect(url_for("new_advertisement"))
        query2="""Insert into Advertisements(car_id,dealer_id,explanation,price,car_year) values(%s,%s,%s,%s,%s)"""
        cursor.execute(query2,(car_id,session.get('dealer_id'),explanation,price,year))
        db.commit()
        flash("Congratulations! Your advertisement has been published.","success")
        return redirect(url_for('my_advertisement'))

@login_required_user
def change_user_info():
    user_id=session.get("user_id")
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select * from User where user_id={user_id_}""".format(user_id_=user_id)
  #  print(query)
    cursor.execute(query)
    data=cursor.fetchone()
 #   print(data[2])
    if request.method=="GET":
        user_=User(user_id=user_id,mail=data[2],user_fullname=data[1],password=data[3])
        return render_template("change_info.html",user=user_)
    else:
        password=request.form["old_password"]
        user_fullname=request.form["user_fullname"].strip()
        new_password2=request.form["new_password"]
        new_password = new_password2.strip() if len(new_password2)>0 else new_password2
        if len(user_fullname)<4:
            flash("User Name cannot be less than 4 character.","danger")
            return redirect(url_for("change_user_info"))
        if len(new_password2)>0:
            if len(new_password)<6:
                flash("New Password cannot be less than 6 character.","danger")
                return redirect(url_for("change_user_info"))     
        if (sha256_crypt.verify(password,data[3])):
            query2="""Update User SET user_password='{pass_}',user_fullname='{name_}' where user_id={user_id_}""".format(pass_=sha256_crypt.encrypt(new_password),
                    name_=user_fullname,user_id_=user_id)  if len(new_password) != 0 else """Update User SET user_fullname='{name_}' where user_id={user_id_}""".format(name_=user_fullname,
                    user_id_=user_id)
            cursor.execute(query2)        
            db.commit()
            flash("Your password has been changed successfully.","primary")
            return redirect(url_for("login_page"))
        else:
            flash("Your password is wrong!","danger")
            return redirect(url_for("change_user_info"))

def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get("admin") != None:
            return f(*args,**kwargs)
        else:  #eğer sayfayı görmek istiyorsan giriş yap
            flash("Please Central Car Dealer login","danger")
            return redirect(url_for("login_page"))
    return decorated_function

@login_required_admin
def admin_page():
    return render_template("admin_page.html")

@login_required_admin
def new_dealer():
    if request.method=="GET":
        return render_template("newdealer.html")
    else:
        dealer_name=request.form["dealer_name"].strip()
        owner_fullname=request.form["owner_fullname"].strip()
        mail=request.form["mail"].strip()
        city=request.form["city"]
        phone=request.form["phone"]
        f_password=request.form["password"].strip()
        if len(f_password)<6:
            flash("Password cannot be less than 6 character.","danger")
            return redirect(url_for("new_dealer"))
        if len(dealer_name)<4:
            flash("Dealer name cannot be less than 4 character.","danger")
            return redirect(url_for("new_dealer"))
        if len(owner_fullname)<4:
            flash("Owner name cannot be less than 4 character.","danger")
            return redirect(url_for("new_dealer"))
        password=sha256_crypt.encrypt(request.form["password"])
      #  print(dealer_name,mail,city,phone,password)
        db=current_app.config["db"]
        cursor=db.cursor()
        query="""Insert into Dealer(dealer_name,owner_fullname,owner_mail,dealer_city,dealer_password,dealer_phone,total_income,number_of_cars_sold,average_point) values 
                ('{dealer_name_}','{owner_fullname_}','{mail_}','{city_}','{password_}','{phone_}',0,0,0)""".format(dealer_name_=dealer_name,owner_fullname_=owner_fullname,mail_=mail,
                city_=city,phone_=phone,password_=password)
      #  print(query)
        try:
            cursor.execute(query)
            db.commit()
            flash("Congratulations! Dealer has been registered.","success")
            return redirect(url_for("admin_page"))
        except:
            flash("Dealer cannot registered.Try Again check phone number and email","danger")
            return redirect(url_for("new_dealer"))

@login_required_admin
def admin_dealer():
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select * from Dealer"""
    cursor.execute(query)
    datas=cursor.fetchall()
    dealers_=[]
    for data in datas:
        dealer=Dealer(dealer_id=data[0],dealer_name=data[1],owner_fullname=data[2],is_central=data[3],owner_mail=data[4],
            dealer_city=data[5],dealer_phone=data[7],total_income=data[8],number_of_cars_sold=data[9],average_point=data[10])
        dealers_.append(dealer)
    return render_template("admin_dealer.html",dealers=dealers_)

@login_required_admin
def delete_dealer(dealer_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select is_central from Dealer where dealer_id='{dealer_id_}' """.format(dealer_id_=dealer_id)
    cursor.execute(query)
    data=cursor.fetchone()
    if data[0]==1:
        return redirect(url_for("admin_dealer"))
    else:
        query2="""Delete from Dealer where dealer_id='{dealer_id_}'""".format(dealer_id_=dealer_id)
        try:
            cursor.execute(query2)
            db.commit()
            flash("Dealer has been deleted succesfully.","primary")
            return redirect(url_for("admin_dealer"))
        except:
            flash("This dealer has advertisements, so you cannot delete this Dealer. First please delete the Advertisements belonging to the dealer.","danger")
            return redirect(url_for("admin_dealer"))
    
@login_required_admin
def admin_advertisements():
    add=[]
    db=current_app.config["db"]
    advertisemets_=[]
    cursor=db.cursor()
    query="""Select * from Advertisements order by advertisement_id desc """
    cursor.execute(query)
    advertisements=cursor.fetchall()
    for advertisement in advertisements:
        query2="""Select dealer_name,dealer_city from Dealer where dealer_id="""+str(advertisement[2])
        cursor.execute(query2)
        dealer=cursor.fetchone()
        query3="""Select * from Car where car_id="""+str(advertisement[1])
        cursor.execute(query3)
        car=cursor.fetchone()
        new_add=Advertisement(ad_id=advertisement[0],dealer_name=dealer[0],city=dealer[1],price=advertisement[4],date=advertisement[6],car_model=car[1],car_brand=car[2],year=advertisement[5],
                            engine_size=car[3],car_type=car[4],horsepower=car[5],gearbox=car[6],fuel=car[7],from_admin=1)
        add.append(new_add)
    return render_template("myadvertisements.html",advertisements=add)

@login_required_admin
def admin_comments():
    db=current_app.config["db"]
    cursor=db.cursor()
    cursor2=db.cursor()
    query="""Select Evaluation.advertisement_id,Evaluation.comment,Evaluation.point,Evaluation.evaluation_date,User.user_fullname,Evaluation.evaluation_id
            from Evaluation inner join User on Evaluation.user_id=User.user_id order by Evaluation.evaluation_id desc"""
    cursor.execute(query)
    datas=cursor.fetchall()
    evas=[]
    for eva in datas:
        query2="""Select Advertisements.advertisement_id,Car.car_model,Car.car_brand from Advertisements inner join Car 
                on Advertisements.car_id=Car.car_id where Advertisements.advertisement_id='{ad_id_}' """.format(ad_id_=eva[0])
        cursor2.execute(query2)
        car=cursor2.fetchone()
      #  print(eva[0])
        eva_=Evaluation(eva[0],eva[5],eva[4],eva[1],eva[3],eva[2],car[1],car[2])
        evas.append(eva_)
     #   print(eva[5],eva[4],eva[1],eva[3],eva[2],car[1],car[2])
    return render_template("mycomments.html",evaluations=evas)


@login_required_admin
def admin_user_comments(user_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select Evaluation.advertisement_id,Evaluation.comment,Evaluation.point,Evaluation.evaluation_date,
                User.user_fullname,Evaluation.evaluation_id from Evaluation inner join User on Evaluation.user_id=User.user_id 
                where User.user_id={user_id_}""".format(user_id_=user_id)
                
    cursor.execute(query)
    #print(query)
    datas=cursor.fetchall()
    evas=[]
    for eva in datas:
        query2="""Select Advertisements.advertisement_id,Car.car_model,Car.car_brand from Advertisements inner join Car 
                on Advertisements.car_id=Car.car_id where Advertisements.advertisement_id='{ad_id_}' """.format(ad_id_=eva[0])
        cursor.execute(query2)
        car=cursor.fetchone()
     #   print(eva[0])
        eva_=Evaluation(eva[0],eva[5],eva[4],eva[1],eva[3],eva[2],car[1],car[2])
        evas.append(eva_)
    return render_template("mycomments.html",evaluations=evas)

@login_required_admin
def admin_users():
    db=current_app.config["db"]
    cursor=db.cursor()
    query="""Select * from User"""
    cursor.execute(query)
    datas=cursor.fetchall()
    users=[]
    for data in datas:
        user_=User(data[0],data[2],data[1],data[3])
        users.append(user_)
    return render_template("admin_users.html",users=users)

@login_required_user
def delete_user(user_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    if session.get("admin") != None:
        query="""Delete from User Where user_id = {user_id_} """.format(user_id_=user_id)
        try:
            cursor.execute(query)
            db.commit()
            flash("User Deleted","info")
            return redirect(url_for("home_page"))
        except:
            flash("User Cannot Deleted","danger")
            return redirect(url_for("home_page")) 
    if session.get("user_id") != None:
        query2="""Select user_password,user_id from User where user_id={user_id_}""".format(user_id_=user_id)
        cursor.execute(query2)
        data=cursor.fetchone()
        if data[1] == session.get("user_id"):
            query="""Delete from User Where user_id = {user_id_} """.format(user_id_=user_id)
            try:
                session.pop('user_id')
                cursor.execute(query)
                db.commit()
                flash("User Deleted","info")
                return redirect(url_for("home_page"))
            except:
                flash("User Cannot Deleted","danger")
                return redirect(url_for("home_page")) 
            
        else:
            return redirect(url_for("change_user_info"))



@login_required_dealer
def update_info_dealer(dealer_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    if request.method=="GET":
        if session.get("admin") != None:
            query="""Select * from Dealer where dealer_id={dealer_id_}""".format(dealer_id_=dealer_id)
            try:
                cursor.execute(query)
                data=cursor.fetchone()
                dealer_=Dealer(dealer_id=data[0],dealer_name=data[1],owner_fullname=data[2],is_central=data[3],owner_mail=data[4],dealer_city=data[5],
                            dealer_phone=data[7])
                return render_template("update_info_dealer.html",dealer=dealer_)
            except:
                return redirect(url_for("admin_dealer"))
        else:
            query="""Select * from Dealer where dealer_id={dealer_id_}""".format(dealer_id_=dealer_id)
            try:
                cursor.execute(query)
                data=cursor.fetchone()
                if session.get("dealer_id") == data[0]:
                 #   print("aynı dealer ")
                    dealer_=Dealer(dealer_id=data[0],dealer_name=data[1],owner_fullname=data[2],is_central=data[3],owner_mail=data[4],dealer_city=data[5],
                            dealer_phone=data[7])
                    return render_template("update_info_dealer.html",dealer=dealer_)
                else:
                 #   print("aynı dealer değil")
                    return redirect(url_for("home_page"))
            except:
               # flash("Cannot Updated 33","danger")
                return redirect(url_for("home_page"))
    else :
        # dealer_name=request.form["dealer_name"]
        # dealer_fullname=request.form["owner_fullname"]
        # dealer_phone=request.form["phone"]
        # new_password=request.form["new_password"]
        # password=request.form["old_password"]
        if session.get("admin") != None:
            dealer_name=request.form["dealer_name"].strip()
            dealer_fullname=request.form["owner_fullname"].strip()
            dealer_phone=request.form["phone"]
            new_password2=request.form["new_password"]
            new_password = new_password2.strip() if len(new_password2)>0 else new_password2
            if len(dealer_name)<2:
                 flash("Dealer Name cannot be less than 2 character.","danger")
                 return redirect(url_for("update_info_dealer",dealer_id=dealer_id))
            if len(dealer_fullname)<4:
                flash("Dealer Name cannot be less than 4 character.","danger")
                return redirect(url_for("update_info_dealer",dealer_id=dealer_id))
            if len(new_password2)>0:
                if len(new_password)<6:
                    flash("New Password cannot be less than 6 character.","danger")
                    return redirect(url_for("update_info_dealer",dealer_id=dealer_id))
            query="""Update Dealer SET dealer_name='{dealer_name_}',owner_fullname='{dealer_fullname_}',dealer_phone='{dealer_phone_}' where dealer_id={dealer_id_}""".format(dealer_name_=dealer_name,
                    dealer_fullname_=dealer_fullname,dealer_phone_=dealer_phone,dealer_id_=dealer_id) if len(new_password) == 0 else """Update Dealer SET dealer_name='{dealer_name_}',
                    owner_fullname='{dealer_fullname_}',dealer_phone='{dealer_phone_}',dealer_password='{new_password_}' where dealer_id={dealer_id_}""".format(dealer_name_=dealer_name,
                    dealer_fullname_=dealer_fullname,dealer_phone_=dealer_phone,new_password_=sha256_crypt.encrypt(new_password),dealer_id_=dealer_id)
          #  print(query)
            try:
                cursor.execute(query)
                db.commit()
                flash("Updated Successfully","success")
                return redirect(url_for("admin_page"))
            except:
                flash("Updated Not Successfully","danger")
                return redirect(url_for("admin_page"))

        else:
            if (dealer_id != session.get("dealer_id")):
                return redirect(url_for("home_page"))
            else:
                dealer_name=request.form["dealer_name"].strip()
                dealer_fullname=request.form["owner_fullname"].strip()
                dealer_phone=request.form["phone"]
                new_password2=request.form["new_password"]
                new_password = new_password2.strip() if len(new_password2)>0 else new_password2
                old_password=request.form["old_password"]
                if len(dealer_name)<2:
                    flash("Dealer Name cannot be less than 2 character.","danger")
                    return redirect(url_for("update_info_dealer",dealer_id=dealer_id))
                if len(dealer_fullname)<4:
                    flash("Dealer Name cannot be less than 4 character.","danger")
                    return redirect(url_for("update_info_dealer",dealer_id=dealer_id))
                if len(new_password2)>0:
                    if len(new_password)<6:
                        flash("New Password cannot be less than 6 character.","danger")
                        return redirect(url_for("update_info_dealer",dealer_id=dealer_id))
                query="""Select dealer_password from Dealer where dealer_id={dealer_id_}""".format(dealer_id_=dealer_id)
                try:
                    cursor.execute(query)
                    data=cursor.fetchone()
                    if sha256_crypt.verify(old_password,data[0]):  #success
                        query2="""Update Dealer SET dealer_name='{dealer_name_}',owner_fullname='{dealer_fullname_}',dealer_phone='{dealer_phone_}' where dealer_id={dealer_id_}""".format(dealer_name_=dealer_name,
                                dealer_fullname_=dealer_fullname,dealer_phone_=dealer_phone,dealer_id_=dealer_id) if len(new_password) == 0 else """Update Dealer SET dealer_name='{dealer_name_}',
                                owner_fullname='{dealer_fullname_}',dealer_phone='{dealer_phone_}',dealer_password='{new_password_}' where dealer_id={dealer_id_}""".format(dealer_name_=dealer_name,
                                dealer_fullname_=dealer_fullname,dealer_phone_=dealer_phone,new_password_=sha256_crypt.encrypt(new_password),dealer_id_=dealer_id)
                        #  print(query2)
                        try:
                            cursor.execute(query2)
                            db.commit()
                            flash("Updated Successfully","success")
                            return redirect(url_for("home_page"))
                        except:
                            flash("Updated Not Successfully","danger")
                            return redirect(url_for("home_page"))
                    else:
                        flash("Wrong Password","danger")
                        return redirect(url_for("home_page"))
                except:
                    flash("Updated Not Successfully","danger")
                    return redirect(url_for("home_page"))

@login_required_admin
def add_new_car():
    if request.method=="GET":
        return render_template("newcar.html")
    else:
        car_brand=request.form["car_brand"].strip()
        car_model=request.form["car_model"].strip()
        car_type=request.form["car_type"]
        gearbox=request.form["gearbox"]
        fuel=request.form["fuel"]
        engine=request.form["engine_size"].strip()
        horsepower=request.form["horsepower"].strip()
        if len(car_brand)==0 or len(car_model)==0 or len(engine)==0 or len(horsepower)==0:
            flash("Fields cannot be empty.","danger")
            return redirect(url_for("add_new_car"))
        else:
            db=current_app.config["db"]
            cursor=db.cursor()
            query="""Select * from Car Where car_model='{car_model_}' and car_brand= '{car_brand_}' and car_type='{car_type_}' and gearbox='{gearbox_}' and 
                    fuel='{fuel_}' and engine_size={engine_size_} and horsepower={horsepower_}""".format(car_model_=car_model.lower().capitalize(),car_brand_=car_brand.lower().capitalize(),
                    car_type_=car_type,gearbox_=gearbox,fuel_=fuel,engine_size_=engine,horsepower_=horsepower)
            cursor.execute(query)
            data=cursor.fetchone()
            if data != None:
                flash("There are cars with these features in stock.")
                return redirect(url_for("admin_page"))
            else:
                query2="""Insert into Car(car_model,car_brand,engine_size,car_type,horsepower,gearbox,fuel) values(%s,%s,%s,%s,%s,%s,%s)"""
                try:
                    cursor.execute(query2,(car_model.lower().capitalize(),car_brand.lower().capitalize(),engine,car_type,horsepower,gearbox,fuel))
                    db.commit()
                    flash("Car has been Added","success")
                    return redirect(url_for("admin_page"))
                except:
                    flash("Car has not been Added","danger")
                    return redirect(url_for("add_new_car"))

@login_required_dealer
def car_stock():
    db=current_app.config["db"]
    cursor=db.cursor()
    query="Select * from Car"
    cursor.execute(query)
    datas=cursor.fetchall()
    cars_=[]
    for data in datas:
        car=Car(car_id=data[0],car_model=data[1],car_brand=data[2],engine_size=data[3],car_type=data[4],horsepower=data[5],gearbox=data[6],fuel=data[7])
        cars_.append(car)
    return render_template("car_stock.html",cars=cars_)

@login_required_admin
def delete_car(car_id):
    db=current_app.config["db"]
    cursor=db.cursor()
    query="Delete from Car where car_id={car_id_}".format(car_id_=car_id)
    try:
        cursor.execute(query)
        db.commit()
        flash("Delete Car Successfully","success")
        return redirect(url_for("admin_page"))
    except:
        flash("There are advertisements with this car. You must delete the advertisements first.","danger")
        return redirect(url_for("car_stock"))

@login_required_dealer
def show_dealer_info():
    db=current_app.config["db"]
    cursor=db.cursor()
    query="Select * from Dealer where dealer_id={dealer_id_}".format(dealer_id_=session.get("dealer_id"))
    try:
        cursor.execute(query)
        data=cursor.fetchone()
        dealer_=Dealer(dealer_id=data[0],dealer_name=data[1],owner_fullname=data[2].capitalize(),is_central=data[3],owner_mail=data[4],dealer_city=data[5],dealer_phone=data[7],
                        total_income=data[8],number_of_cars_sold=data[9],average_point=data[10])
        return render_template("show_dealer_info.html",dealer=dealer_)
    except:
        flash("Error","danger")
        return redirect(url_for("home_page"))


@login_required_admin
def update_car(car_id):
    if request.method=="GET":
        db=current_app.config["db"]
        cursor=db.cursor()
        query="Select * from Car where car_id={car_id_}".format(car_id_=car_id)
        cursor.execute(query)
        data=cursor.fetchone()
        car_=Car(car_id=data[0],car_model=data[1],car_brand=data[2],engine_size=data[3],car_type=data[4],horsepower=data[5],gearbox=data[6],fuel=data[7])
        return render_template("update_car.html",car=car_)
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        car_type=request.form["car_type"]
        engine_size=request.form["engine"]
        horsepower=request.form["horsepower"]
        fuel=request.form["fuel"]
        gearbox=request.form["gearbox"]
        query="""Update Car SET engine_size='{engine_size_}',car_type='{car_type_}',horsepower='{horsepower_}',gearbox='{gearbox_}', fuel='{fuel_}' 
                where car_id={car_id_}""".format(engine_size_=engine_size,car_type_=car_type,horsepower_=horsepower,gearbox_=gearbox,fuel_=fuel,car_id_=car_id)
        try:
            cursor.execute(query)
            db.commit()
            flash("Car has been updated successfully","success")
            return redirect(url_for("car_stock"))
        except:
            flash("Update is Error ","danger")
            return redirect(url_for("car_stock"))

@login_required_user
def change_comment(eva_id):
    if session.get("admin") != None:
        return redirect(url_for("admin_comments"))
    db=current_app.config["db"]
    cursor=db.cursor()
    user_id=session.get("user_id")
    query="""Select user_id,advertisement_id,comment,point from Evaluation where evaluation_id={eva_id_}""".format(eva_id_=eva_id)
    cursor.execute(query)
    data=cursor.fetchone()
    if request.method=="GET":
        if (data==None or data[0] != user_id) and session.get("admin") != 1:
            return redirect(url_for("my_comments"))
        else:
            cursor2=db.cursor()
            query5="""Select Car.car_brand,Car.car_model from Advertisements inner join Car on Advertisements.car_id=Car.car_id 
                        where Advertisements.advertisement_id={adv_id_} """.format(adv_id_=data[1])
            cursor2.execute(query5)
            car=cursor2.fetchone()
            eva_=Evaluation(advertisement_id=data[1],evaluation_id=eva_id,user_fullname=None,comment=data[2],point=data[3],car_model=car[1],car_brand=car[0])
            return render_template("change_comment.html",evaluation=eva_)
    else:
        cursor3=db.cursor()
        comment_form=request.form["comment"].strip()
        point_form=request.form["point"]
        if len(comment_form) < 20:
            flash("Your Comment cannot be less than 5 character.","danger")
            return redirect(url_for("change_comment",eva_id=eva_id))
        query_update="""Update Evaluation SET comment='{comment_}',point={point_} where evaluation_id={eva_id_}""".format(comment_=comment_form,point_=point_form,eva_id_=eva_id)
        try:
            cursor3.execute(query_update)
            db.commit()
            flash("Your Comment is Changed","success")
            return redirect(url_for("my_comments"))
        except:
            flash("An error occurred.","danger")
            return render_template("change_comment.html",evaluation=eva_)

@login_required_user
def add_favorite(adv_id):
    if session.get("admin") != None:
        flash("Please user login","danger")
        return redirect(url_for("ad_detail_page",ad_id=adv_id))
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        user_id=session.get("user_id")
        query="""Insert into Wishlist(user_id,advertisement_id) values({user_id_},{adv_id_})""".format(user_id_=user_id,adv_id_=adv_id)
        try:
            cursor.execute(query)
            db.commit()
            flash("This advertisement has been added your Favorite List.","success")
            return redirect(url_for("ad_detail_page",ad_id=adv_id))
        except:
            flash("This advertisement has not been added your Favorite List.","danger")
            return redirect(url_for("ad_detail_page",ad_id=adv_id))
      

@login_required_user
def user_favorite_list():
    if session.get("admin") != None:
        return redirect(url_for("admin_comments"))
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        user_id=session.get("user_id")
        query="""Select Advertisements.advertisement_id,Wishlist.wish_date,Car.car_brand,Car.car_model,Advertisements.price,Advertisements.car_year
                from Advertisements 
                inner join Car ON Advertisements.car_id=Car.car_id
                inner join Wishlist ON Wishlist.advertisement_id=Advertisements.advertisement_id
                where Wishlist.user_id={user_id_}""".format(user_id_=user_id)
       # try:
        cursor.execute(query)
        datas=cursor.fetchall()
        wish_arr=[]
        for data in datas:
            wish_=Wishlist(user_id=user_id,adv_id=data[0],date=data[1],car_brand=data[2],car_model=data[3],car_price=data[4],car_year=data[5])
            wish_arr.append(wish_)
        return render_template("favorite_list.html",wish_list=wish_arr)
        # except:
        #     return redirect(url_for("home_page"))

@login_required_user
def delete_from_favorite(ad_id):
    if session.get("admin") != None:
        return redirect(url_for("admin_comments"))
    else:
        db=current_app.config["db"]
        cursor=db.cursor()
        user_id=session.get("user_id")
        query2="""Delete from Wishlist Where advertisement_id ={adv_id_} and user_id={user_id_}""".format(adv_id_=ad_id,user_id_=user_id)
        try:
            cursor.execute(query2)
            db.commit()
            flash("Delete Successfully","success")
            return redirect(url_for("user_favorite_list"))
        except:
            flash("Delete Error","danger")
            return redirect(url_for("user_favorite_list"))