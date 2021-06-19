
class PriceGenerator:

    def __init__(self, dbconnection):
        self.db = dbconnection
        self.base_url = "http://127.0.0.1:5000/"
        self.product_l = "c/"

    def gen_url(self, product_id, tag_id):
        args = f"?price={date}"
        return self.base_url + self.product_l + product_id + args

    def register(self, product_id, tag_id):
        self.db.exec("INSERT INTO items VALUES (%s, %s);", (product_id, price))

    def gen(self, product_id, tag_id):
        url = self.gen_url(product_id, price)
        self.register(product_id, price)

        return url
