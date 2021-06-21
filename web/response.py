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

class TagDateResponse(JSONResponse):

    def __init__(self, is_outdated, latest_tag_date, this_tag_date):
        self.body = {
            "error": False,
            "outdated": is_outdated,
            "latest_tag_date": latest_tag_date,
            "this_tag_date": this_tag_date,
        }

class NewTagResponse(JSONResponse):

    def __init__(self, tag_id, tag_date):
        self.body = {
            "error": False,
            "new_tag_id": tag_id,
            "new_tag_date": tag_date
        }
