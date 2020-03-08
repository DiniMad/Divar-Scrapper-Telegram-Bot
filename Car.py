class Car:
    def __init__(self, token, title, price, city, district, image_url):
        self.token = token
        self.title = title
        self.price = price
        self.city = city
        self.__district = district
        self.image_url = image_url

    def __str__(self):
        return f"[{self.title}]({self.link})\n\n[{self.address}]" \
               f"({self.image_url})\n\n_{self.price}_"

    @property
    def link(self):
        return f"https://divar.ir/v/{self.token}"

    @property
    def address(self):
        return f"{self.city} - {self.district}"

    @property
    def district(self):
        return self.__district if self.__district else ""

    @district.setter
    def district(self, value):
        self._district = value
