from flask import Flask
from flask import request

from dbconnection import DBConnection
from price_url_generator import PriceGenerator

app = Flask(__name__)

@app.route("/c/<int:item>", methods=["GET"])
def item(item):

    con = DBConnection()

    print_date = request.args.get("pdate")
    if not print_date:
        return "no date param, skipping :P"

    print(f"Got print date: {print_date}")

    actual_print_date = con.exec("SELECT last_modified FROM prices WHERE item_id = %s", item)
    if not actual_print_date:
        return f"product {item} not found"

    actual_print_date_ts = actual_print_date[0].timestamp()
    print("typeof", type(actual_print_date_ts))

    print(f"Got actual print date: {actual_print_date_ts}")

    if actual_print_date != print_date:
        print("Date mismatch, price tag is outdated")
        return f"{item} : {print_date} != {actual_print_date_ts}"



#    guessed_price = request.args.get("price") 
#    if not guessed_price:
#        return f"Здесь должна будет быть позиция: {item}"
#
#    con = DBConnection()
#    res = con.exec("SELECT * FROM items WHERE item_id = %s;", item)
#    
#    if res:
#        return "True price: " + str(res[1]) + f"; Guessed price: {guessed_price}"
#    else:
#        return f"Product: {item} is not on the list"

@app.route("/")
def default():
    return "Unrecognized"
