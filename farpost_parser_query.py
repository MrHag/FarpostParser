import time
import requests
from farpost_options import farpost_options


class farpost_parser_query:

    options: farpost_options

    __page: int
    __city: int
    __category: int
    __price_min: int
    __price_max: int

    def __init__(self, options: farpost_options):
        self.options = options
        self.__page = 0
        self.__city = 0
        self.__category = 0
        self.__price_min = options.min_price
        self.__price_max = self.__price_min + self.options.price_step

        if len(self.options.cities)==0:
            self.__city = -1

    def next(self) -> requests.Request | None:
        req = self.__create_query()

        self.__page += 1

        if self.__page == self.options.pages_count:
            self.__page = 0
            self.__category += 1
            
        if self.__category == len(self.options.categories):
            self.__category = 0
            self.__city += 1

        if self.__city == len(self.options.cities):
            self.__city = 0
            if len(self.options.cities) == 0:
                self.__city = -1
                
            self.__price_min += self.options.price_step
            self.__price_max += self.options.price_step

        if self.__price_max > self.options.max_price:
            self.__price_min = self.options.min_price
            self.__price_max = self.__price_min
            return None

        return req

    def current(self) -> requests.Request:
        return self.__create_query()

    @staticmethod
    def user_query(userid: str) -> requests.Request:
        return requests.Request(
            'GET', f'https://www.farpost.ru/user/{userid}/')

    @staticmethod
    def product_query(productid: str) -> requests.Request:
        return requests.Request(
            'GET', f'https://www.farpost.ru/{productid}')

    @staticmethod
    def phone_query(productid: str) -> requests.Request:
        return requests.Request(
            'GET', f'https://www.farpost.ru/bulletin/{productid}/ajax_contacts?paid=1&ajax=1')
        

    def __create_query(self) -> requests.Request:
        options = self.options
        page = self.__page
        max_price = self.__price_max
        min_price = self.__price_min
        category = options.categories[self.__category]

        if (len(options.cities) == 0):
            city = ""
        else:
            city = f"{options.cities[self.__city]}/"          
        category = f"{category}/"

        req_url = f"https://www.farpost.ru/{city}{category}?_lightweight=1&ajax=1&async=1&page={page}&status=actual&condition%5B%5D=used&price_min={min_price}&price_max={max_price}"

        print(f"Page {page+1} of {self.options.pages_count}")
        if city != "":
            print(f"City: {city}")
        print(f"Category: {category}")
        print(f"Price: {min_price} - {max_price}")
        print("")

        req = requests.Request('GET', req_url)
        return req