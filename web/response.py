from flask import jsonify

class JSONResponse:

    def __init__(self):
        self.body = None

    def json(self):
        return jsonify(self.body)


class ErrorResponse(JSONResponse):

    def __init__(self, what):
        self.body = {
            "error": True,
            "what": what,
        }

class OkResponse(JSONResponse):

    def __init__(self):
        self.body = {
            "error": False,
        }

class TagDateResponse(OkResponse):

    def __init__(self, is_outdated, latest_tag_date, this_tag_date, item_id, item_name):
        self.body = {
            "error": False,
            "outdated": is_outdated,
            "latest_tag_date": latest_tag_date,
            "this_tag_date": this_tag_date,
            "item_id": item_id,
            "item_name": item_name
        }

class NewTagResponse(OkResponse):

    def __init__(self, tag_id, tag_date):
        self.body = {
            "error": False,
            "new_tag_id": tag_id,
            "new_tag_date": tag_date
        }

class NewItemResponse(OkResponse):

    def __init__(self, item_id, item_name):
        self.body = {
            "error": False,
            "item_id": item_id,
            "item_name": item_name
        }
