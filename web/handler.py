from flask import Flask, request, jsonify, make_response
from datetime import datetime

import db_requests
import response

app = Flask(__name__)
print("starting...")
def bump_misses(price_tag_id):

    misses = db_requests.SQLRequestGetMisses().run(price_tag_id)

    if misses is None:
        return

    db_requests.SQLRequsetUpdateMisses().run(price_tag_id, misses + 1)


def item_seller(item, price_tag_id):

    latest_tag_date = db_requests.SQLRequestGetNewestTagDate().run(item)
    if latest_tag_date is None:
        return response.ErrorResponse(f"No tags for this item id({item})").json(), 406

    this_tag_date = db_requests.SQLRequsetGetTagDate().run(price_tag_id)
    if this_tag_date is None:
        return response.ErrorResponse(f"Unregistered tag id({price_tag_id})").json(), 406

    is_miss = this_tag_date != latest_tag_date
    if is_miss:
        bump_misses(price_tag_id)

    return response.TagDateResponse(is_miss, latest_tag_date, this_tag_date).json(), 200


def item_customer(item, price_tag_id):
    
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


@app.route("/f/<int:item>", methods=["GET"])
def get_new_tag_id(item):

    cur_date = datetime.now()
    cur_date = cur_date.replace(microsecond=0)

    new_tag_id = db_requests.SQLInsertNewTag().run(cur_date, item)

    return response.NewTagResponse(new_tag_id, cur_date).json(), 200


@app.route("/")
def default():
    return "Unrecognized"
