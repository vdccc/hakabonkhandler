
class PriceGenerator:

    def __init__(self):
        self.base_url = "http://127.0.0.1:5000/"
        self.product_l = "c/"

    def gen_url(self, product_id, tag_id):
        query = f"?price={tag_id}"
        return self.base_url + self.product_l + product_id + query

    def gen(self, product_id, tag_id):
        url = self.gen_url(product_id, price)

        return url
