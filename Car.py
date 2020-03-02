class Car:
    def __init__(self, token, title, price, city, district, image_url):
        self.token = token
        self.title = title
        self.price = price
        self.city = city
        self.district = district
        self.image_url = image_url

    def link(self):
        return f"https://divar.ir/v/{self.token}"
