import sqlite3
import json
from fastapi import FastAPI
from pydantic import BaseModel

con = sqlite3.connect("cars.db")
cur = con.cursor()
cur.execute("""create table if not exists cars (id int, make text, model text, color text, year year, licence_plate 
text, location text, seller_name text, purchase_price float, is_sold bool, selling_price float, buyers_name text, 
date_of_sale date, image_url text)""")

con.commit()

# '''
# cur.execute("""insert into cars values ('01', 'BMW', 'M3', 'Red', '2020', 'YX26 SZZ', 'Birmingham', 'Fred Bigman',
# '10000.50', 'False', '15000,75', 'Tony Soprano', '26-05-1995', "")""")
# cur.execute("""insert into cars values ('02', 'Ford', 'Wrangler', 'Blue', '2018', 'YX26 SZG', 'Colchester', 'Ted Bundy',
# '10000.50', 'False', '15000,75', 'Tony Soprano', '28-05-1995', "")""")
# cur.execute("""insert into cars values ('03', 'Volkswagon', 'Golf', 'Black', '2021', 'YX46 SZZ', 'London', 'Obama',
# '10000.50', 'False', '15000,75', 'Tony Soprano', '27-05-1995', "")""")
# '''
#cur.execute("select * from cars where licence_plate is 'YX26 SZZ'")


res = cur.fetchall()
print(res)
con.commit()
con.close()

nextid = 4

app = FastAPI()


class Car(BaseModel):
    id: int
    make: str
    model: str
    color: str
    year: int
    license_plate: str
    location: str
    seller_name: str
    purchase_price: float
    is_sold: bool
    selling_price: float
    buyers_name: str
    date_of_sale: str
    image_url: str


@app.post("/newcar")
def api_newcar(car: Car):
    global nextid
    cur.execute(f"insert into cars values ('{car.id}', '{car.make}', '{car.model}', '{car.color}', '{car.year}', '{car.license_plate}', '{car.location}', '{car.buyers_name}', '{car.purchase_price}', '{car.is_sold}', '{car.selling_price}', '{car.buyers_name}', '{car.date_of_sale}', '{car.image_url}')")
    nextid += 1
    return car

@app.get("/cars")
def api_get_cars():
    cur.execute(f"select * from cars")
    res = cur.fetchall()
    print(res)

@app.get("/car")
def api_get_car_by_licence(licence: str):
    cur.execute(f"select * from cars where licence = '{licence}'")
    res=cur.fetchall()
    print(res)

@app.update("/sell")
def api_sell_car(car: Car):
    car.is_sold = True
    car.purchase_price = car.selling_price
    car.selling_price = (car.purchase_price * 1.5)
    car.seller_name = car.buyers_name
    car.buyers_name = ""
    cur.execute(f"Update cars set is_sold = True where id = {car.id}")
    cur.execute(f"Update cars set purchase_price = {car.purchase_price} where id = {car.id}")
    cur.execute(f"Update cars set selling_price = {car.selling_price} where id = {car.id}")
    cur.execute(f"Update cars set seller_name = {car.seller_name} where id = {car.id}")
    cur.execute(f"Update cars set buyers_name = {car.buyers_name} where id ={car.id}")


