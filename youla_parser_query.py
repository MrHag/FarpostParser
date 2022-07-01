import time
import requests

from youla_options import youla_options


class youla_parser_query:

    options: youla_options

    __page: int
    __city: int
    __category: int

    def __init__(self, options: youla_options):
        self.options = options
        self.__page = 0
        self.__city = 0
        self.__category = 0

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
            return None

        return req

    def current(self) -> requests.Request:
        return self.__create_query()

    @staticmethod
    def user_query(userid: str) -> requests.Request:
        return requests.Request(
            'GET', f'https://api.youla.io/api/v1/user/{userid}')

    @staticmethod
    def product_query(priductid: str) -> requests.Request:
        return requests.Request(
            'GET', f'https://api.youla.io/api/v1/product/{priductid}')
        

    def __create_query(self) -> requests.Request:
        options = self.options
        page = self.__page
        max_price = options.max_price
        min_price = options.min_price
        category = options.categories[self.__category]
        timestamp = int(time.time())

        city: str | None

        if (len(options.cities) == 0):
            city = None
        else:
            city = f"{options.cities[self.__city]}"
            

       # req_url = f"https://{host}/{city}/{category}?attributes[price][to]={max_price*100}&attributes[price][from]={min_price*100}&attributes[delivery][0]=150650"

        req_json = {
            "extensions": {
                "persistedQuery": {
                    "sha256Hash": "bf7a22ef077a537ba99d2fb892ccc0da895c8454ed70358c0c7a18f67c84517f",
                    "version": 1
                }
            },
            "operationName": "catalogProductsBoard",
            "variables": {
                "attributes": [
                    {
                        "from": min_price*100,
                        "slug": "price",
                        "to": max_price*100,
                        "value": None
                    },
                    {
                        "from": None,
                        "slug": "delivery",
                        "to": None,
                        "value": ["1"]
                    },
                    {
                        "from": None,
                        "slug": "categories",
                        "to": None,
                        "value": [category]
                    }
                ],
                "cursor": f"{{\"page\":{page},\"totalProductsCount\":{(page+1)*30},\"dateUpdatedTo\":{timestamp}}}",
                "location": {
                    "city": city,
                    "distanceMax": None,
                    "latitude": None,
                    "longitude": None
                },
            }
        }

        print(f"Page {page+1} of {self.options.pages_count}")
        if city is not None:
            print(f"City: {city}")
        print(f"Category: {category}")
        print("")

        req = requests.Request(
            'POST', 'https://api-gw.youla.io/federation/graphql', json=req_json)

        return req