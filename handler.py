from flask import Flask, request, jsonify, make_response

from dbconnection import DBConnection
from price_url_generator import PriceGenerator

app = Flask(__name__)

def bump_misses(price_tag_id):

    con = DBConnection()

    misses = con.exec("SELECT misses FROM prices WHERE id = %s", (price_tag_id,))
    if misses is None:
        return

    misses = misses[0]

    con.exec("UPDATE prices SET misses = (%s) WHERE id = (%s);",
            (misses + 1, price_tag_id), fetch=False)

def item_seller(item, price_tag_id):

    con = DBConnection()
    
    latest_price_tag_date = con.exec("SELECT date FROM prices WHERE item_id = %s ORDER BY date DESC;",
            (item,))

    if latest_price_tag_date is None:
        no_item_res = {
                "result": "No such item",
                "error": True
                }

        return make_response(jsonify(no_item_res), 406)
    else:
        latest_price_tag_date = latest_price_tag_date[0]

    this_price_tag_date = con.exec("SELECT date FROM prices WHERE id = %s;", (price_tag_id,))

    if this_price_tag_date is None:
        no_price_tag = {
                "result": "Unregistered price tag",
                "error": True
                }

        return make_response(jsonify(no_price_tag, 406))
    else:
        this_price_tag_date = this_price_tag_date[0]

    is_miss = this_price_tag_date == latest_price_tag_date
    if is_miss:
        bump_misses(price_tag_id)
    
    response = {
            "outdated": is_miss,
            "latest_tag_date": latest_price_tag_date,
            "this_tag_date": this_price_tag_date,
            "error": False,
            }

    return make_response(jsonify(response), 200) 

def item_customer(item, price_tag_id):
    
    bump_misses(price_tag_id)

    return make_response("Customer view", 200)

def item_no_price_tag_id(item):

    return f"No price tag id supplied for item {item}"

@app.route("/c/<int:item>", methods=["GET"])
def item(item):

    price_tag_id = int(request.args.get("pid"))
    if price_tag_id is None:
        return item_no_price_tag_id(item)

    if request.args.get("seller") is not None:
        return item_seller(item, price_tag_id)
    else:
        return item_customer(item, price_tag_id)

@app.route("/")
def default():
    return "Unrecognized"
