from flask import current_app
import mysql.connector

mydb=mysql.connector.connect(
        host="esilxl0nthgloe1y.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
        user="n7mmghi3uclxqy2w",
        password="qaz0vvkzw8fmdh9p",
        database="g93ov32o60ckmev5",
       	ssl_disabled=True,
)

INIT_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS Car (
    car_id INTEGER NOT NULL AUTO_INCREMENT,
    car_model VARCHAR(40) NOT NULL,
    car_brand VARCHAR(40) NOT NULL,
    engine_size INTEGER,
    car_type VARCHAR(25),
    horsepower INTEGER,
    gearbox VARCHAR(20),
    fuel VARCHAR(25),
    PRIMARY KEY (car_id),
    CHECK((engine_size >= 100) AND (engine_size <= 9000)),
    CHECK ((horsepower >= 30) AND (horsepower <= 1500)) );
    """,

    """
    CREATE TABLE IF NOT EXISTS Dealer (
    dealer_id INTEGER NOT NULL AUTO_INCREMENT,
    dealer_name VARCHAR(40) NOT NULL,
    owner_fullname VARCHAR(40) NOT NULL,
    is_central BOOL NOT NULL DEFAULT False,
    owner_mail VARCHAR(40) NOT NULL UNIQUE,
    dealer_city VARCHAR(20) NOT NULL,
    dealer_password VARCHAR(150) NOT NULL,
    dealer_phone VARCHAR(30) NOT NULL UNIQUE,
    total_income INTEGER DEFAULT 0,
    number_of_cars_sold INTEGER DEFAULT 0,
    average_point FLOAT   DEFAULT 0,
    PRIMARY KEY (dealer_id));    
    """,

    """
    CREATE TABLE IF NOT EXISTS Advertisements (
    advertisement_id INTEGER NOT NULL AUTO_INCREMENT,
    car_id INTEGER,
    dealer_id INTEGER,
    explanation VARCHAR(250),
    price INTEGER NOT NULL,
    car_year INTEGER,
    advertisement_date Timestamp default CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES Car(car_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (dealer_id) REFERENCES Dealer(dealer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (advertisement_id),
    CHECK ((price >= 5000) AND (price <= 15000000)),
    CHECK(( car_year >= 1900) AND (car_year <= 2022)));

    """,
    """
    CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER NOT NULL AUTO_INCREMENT,
    user_fullname VARCHAR(40) NOT NULL,
    user_mail VARCHAR(40) NOT NULL UNIQUE,
    user_password VARCHAR(150) NOT NULL,
    PRIMARY KEY (user_id)
    );

    """,
    """
    CREATE TABLE IF NOT EXISTS Evaluation(
    evaluation_id INTEGER NOT NULL AUTO_INCREMENT,
    user_id INTEGER,
    advertisement_id INTEGER,
    comment VARCHAR(250),
    point INTEGER,
    evaluation_date Timestamp default CURRENT_TIMESTAMP,
    PRIMARY KEY (evaluation_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (advertisement_id) REFERENCES Advertisements(advertisement_id) ON DELETE CASCADE
    ON UPDATE CASCADE,
    CHECK ((point >= 1) and (point <= 5)));    
    """,
    """
    CREATE TABLE IF NOT EXISTS Wishlist (
    user_id INTEGER NOT NULL,
    advertisement_id INTEGER NOT NULL,
	PRIMARY KEY(user_id,advertisement_id),
    wish_date Timestamp default CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (advertisement_id) REFERENCES Advertisements(advertisement_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """Insert IGNORE into Dealer(dealer_name,owner_fullname,is_central,owner_mail,dealer_city,dealer_password,dealer_phone) 
        VALUES ('Kara Central','Oguzhan Karabacak',True,'admin_dealer@gmail.com','Istanbul'
        ,'$5$rounds=535000$Rht7cY/CdJHhFMBa$tiZCqAdbeE8CaAEjulOJ1qKXgxwl5QITOPlPaEORtQ3','05056543210')"""
    
]

def initialize():
    cursor=mydb.cursor()
    for statement in INIT_STATEMENTS:
        cursor.execute(statement)
        mydb.commit()
    cursor.close()
    return mydb

if __name__=="__main__":
    initialize()
