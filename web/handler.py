from flask import Flask, request, jsonify, make_response
from datetime import datetime

import db_requests
import response
from tgalert import TgAlert

app = Flask(__name__)

def itm(item_id, item_name):
    return {
        "item_id": item_id,
        "item_name": item_name,
    }

groups = {
    1: [itm(1, "Teapot"), itm(2, "Microwave"), itm(3, "Vacuum Cleaner")],
    2: [itm(4, "Big Tv"), itm(5, "Small tv"), itm(6, "Nice tv"), itm(7, "Gamer Tv")]
}

# item_id это то SKU или артикул

def bump_misses(price_tag_id):

    misses = db_requests.SQLRequestGetMisses().run(price_tag_id)

    if misses is None:
        return

    item_id = db_requests.SQLRequestItemIdFromPriceTag().run(price_tag_id)
    if item_id is None:
        return

    item_name = db_requests.SQLRequestItemName().run(item_id)
    if item_name is None:
        return

    TgAlert().send(f"Отсканило просроченный чек {price_tag_id} товара {item_name}")

    db_requests.SQLRequsetUpdateMisses().run(price_tag_id, misses + 1)


def item_seller(item, price_tag_id):

    latest_tag_date = db_requests.SQLRequestGetNewestTagDate().run(item)
    if latest_tag_date is None:
        return response.ErrorResponse(f"No tags for this item id({item})").json(), 406

    this_tag_date = db_requests.SQLRequsetGetTagDate().run(price_tag_id)
    if this_tag_date is None:
        return response.ErrorResponse(f"Unregistered tag id({price_tag_id})").json(), 406

    item_name = db_requests.SQLRequestItemName().run(item)
    if item_name is None:
        return response.ErrorResponse(f"Couldn't find name for item({item})").json(), 406

    is_miss = this_tag_date != latest_tag_date
    if is_miss:
        bump_misses(price_tag_id)

    return response.TagDateResponse(is_miss, latest_tag_date,
                                    this_tag_date, item, item_name).json(), 200


def item_customer(item, price_tag_id):
    # duble
    latest_tag_date = db_requests.SQLRequestGetNewestTagDate().run(item)
    if latest_tag_date is None:
        return response.ErrorResponse(f"No tags for this item id({item})").json(), 406

    this_tag_date = db_requests.SQLRequsetGetTagDate().run(price_tag_id)
    if this_tag_date is None:
        return response.ErrorResponse(f"Unregistered tag id({price_tag_id})").json(), 406

    is_miss = this_tag_date != latest_tag_date
    if is_miss:
        bump_misses(price_tag_id)

    return "Customer view", 200


def item_no_price_tag_id(item):

    return f"No price tag id supplied for this id({item})", 406


@app.route("/c/<int:item>", methods=["GET"])
def item(item):

    price_tag_id = request.args.get("pid")
    if price_tag_id is None:
        return item_no_price_tag_id(item)

    price_tag_id = int(price_tag_id) # кладётся здесь если ?pid=12314?seller=228

    if request.args.get("seller") is not None:
        return item_seller(item, price_tag_id)
    else:
        return item_customer(item, price_tag_id)


@app.route("/add/<int:item>", methods=["GET"])
def get_new_tag_id_get(item):

    cur_date = datetime.now()
    cur_date = cur_date.replace(microsecond=0)

    new_tag_id = db_requests.SQLInsertNewTag().run(cur_date, item)

    return response.NewTagResponse(new_tag_id, cur_date).json(), 200


@app.route("/add", methods=["POST"])
def get_new_tag_id_post():

    if 'item_id' not in request.form:
        return response.ErrorResponse("No item_id supplied in POST request").json(), 406

    item_id = request.form['item_id']

    cur_date = datetime.now()
    cur_date = cur_date.replace(microsecond=0)

    new_tag_id = db_requests.SQLInsertNewTag().run(cur_date, item_id)

    return response.NewTagResponse(new_tag_id, cur_date).json(), 200


@app.route("/add_item", methods=["POST"])
def add_new_item():
    if 'item_id' not in request.form:
        return response.ErrorResponse("No item_id field in form").json(), 406

    if 'item_name' not in request.form:
        return response.ErrorResponse("No item_name field in form").json(), 406

    item_id = request.form['item_id']
    item_name = request.form['item_name']

    db_requests.SQLInsertNewItem().run(item_id, item_name)

    return response.NewItemResponse(item_id, item_name).json(), 200


@app.route("/get_items_from_group/<int:group_id>", methods=["GET"])
def get_items_from_group(group_id):
    if group_id in groups.keys():
        return response.GetGroupResponse(groups[group_id]).json(), 200
    else:
        return response.ErrorResponse(f"No such group_id({group_id})")


@app.route("/")
def default():
    return "Unrecognized"
