from flask import Flask,current_app,session
import mysql.connector
# from dbinit import INIT_STATEMENTS
import dbinit
import views



def create_app():
    app = Flask(__name__)
    app.add_url_rule("/",view_func=views.home_page,methods=["GET","POST"])
    app.add_url_rule("/ad_detail/<int:ad_id>",view_func=views.ad_detail_page,methods=["GET","POST"])
    app.add_url_rule("/register",view_func=views.register,methods=["GET","POST"])
    app.add_url_rule("/login",view_func=views.login_page,methods=["GET","POST"])
    app.add_url_rule("/dealer",view_func=views.dealer_page)
    app.add_url_rule("/logout",view_func=views.logout)
    app.add_url_rule("/dealer/<int:dealer_id>",view_func=views.dealer_detail_page)
    app.add_url_rule("/myadvertisements/",view_func=views.my_advertisement)
    app.add_url_rule("/updateAdd/<int:ad_id>",view_func=views.update_add,methods=["GET","POST"])
    app.add_url_rule("/deleteAdd/<int:ad_id>",view_func=views.delete_add)
    app.add_url_rule("/soldAdd/<int:ad_id>",view_func=views.sold_add)
    app.add_url_rule("/myComments",view_func=views.my_comments)
    app.add_url_rule("/deleteComment/<int:eva_id>",view_func=views.delete_comment)
    app.add_url_rule("/newadvertisement",view_func=views.new_advertisement,methods=["GET","POST"])
    app.add_url_rule("/changeUserinfo",view_func=views.change_user_info,methods=["GET","POST"])
    app.add_url_rule("/adminpanel",view_func=views.admin_page)
    app.add_url_rule("/newDealer",view_func=views.new_dealer,methods=["GET","POST"])
    app.add_url_rule("/admin_dealer",view_func=views.admin_dealer,methods=["GET","POST"])
    app.add_url_rule("/deleteDealer/<int:dealer_id>",view_func=views.delete_dealer)
    app.add_url_rule("/admin_advertisement",view_func=views.admin_advertisements)
    app.add_url_rule("/adminComments",view_func=views.admin_comments)
    app.add_url_rule("/admin_user_comment/<int:user_id>",view_func=views.admin_user_comments,methods=["GET","POST"])
    app.add_url_rule("/adminUser",view_func=views.admin_users)
    app.add_url_rule("/deleteUser/<int:user_id>",view_func=views.delete_user)
    app.add_url_rule("/updateInfoDealer/<int:dealer_id>",view_func=views.update_info_dealer,methods=["GET","POST"])
    app.add_url_rule("/addNewCar",view_func=views.add_new_car,methods=["GET","POST"])
    app.add_url_rule("/carStock",view_func=views.car_stock)
    app.add_url_rule("/deleteCar/<int:car_id>",view_func=views.delete_car)
    app.add_url_rule("/dealerinfo",view_func=views.show_dealer_info)
    app.add_url_rule("/updateCar/<int:car_id>",view_func=views.update_car,methods=["GET","POST"])
    app.add_url_rule("/updateComment/<int:eva_id>",view_func=views.change_comment,methods=["GET","POST"])
    app.add_url_rule("/addfavorite/<int:adv_id>",view_func=views.add_favorite)
    app.add_url_rule("/myfavoritelist",view_func=views.user_favorite_list)
    app.add_url_rule("/deletefromfavorite/<int:ad_id>",view_func=views.delete_from_favorite)
    

    app.config.from_object("settings")
    app.config["db"]=dbinit.initialize()
    # cursor=mydb.cursor()
    # for statement in INIT_STATEMENTS:
    #     cursor.execute(statement)
    #     mydb.commit()
    return app


app=create_app()  

if __name__ == "__main__":
    app.run()



