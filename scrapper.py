from http.server import HTTPServer
import threading
from farpost_core import farpost_core
from youla_config import InvalidConfigException
from db import db
from request_master import request_master
from web_server import Serv
from browser import browser, browser_type

try:

    core_type = farpost_core

    print("Loading config...")
    try:
        cfg = core_type.config_type("config.json")

    except InvalidConfigException:
        print("Config is bad")
        exit(0)

    brw_type: browser_type

    match cfg.browser_type:
        case "chrome": brw_type = browser_type.CHROME
        case "firefox": brw_type = browser_type.FIREFOX
        case _: exit(0)

    print("Starting HTTP server...")
    httpd = HTTPServer(('127.0.0.1', 3536), Serv)
    threading.Thread(target=httpd.serve_forever).start()

    print("Checking browser...")
    brw = browser(brw_type, cfg.browser_path, "http://127.0.0.1:3536")
    brw.check_browser()

    print("Connect to database...")
    database = db('database.db', core_type.SQL)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}
    req_master = request_master(headers)

    print("Start parsing...")

    core = core_type(database, cfg, brw, req_master)

    core.start()

except Exception as e:
    print("ERROR: ", e)
    raise NotImplementedError()
finally:
    try:
        print("http")
        if httpd:
            httpd.server_close()
        print("brw")
        if brw:
            brw.quit()
    except NameError:
        pass
    input("Program on pause...")
    print("ok")

# database = db('database.db', farpost_core.SQL)

# databaseold = db('databaseold.db', [])

# users = databaseold.execute(f"SELECT * FROM users").fetchall()

# users_len = len(users)

# for i, us in enumerate(users):
#     print(f"{i} of {users_len}\n")
#     user_pack = {'id': us[0], 'user_id': us[1], 'offers_count': us[2], 'phone': re.sub('\D', '', us[3]), 'is_scammed': 1}
#     q = '"'
#     sql = f"INSERT INTO users({','.join(user_pack.keys())}) VALUES ({','.join([f'{q}{p}{q}' for p in user_pack.values()])})"
#     try:
#         database.execute(sql)
#     except IntegrityError:
#             pass

#     user_db_id = us[0]

#     offers = databaseold.execute(f"SELECT * FROM ads WHERE \"user_id\" = \"{user_db_id}\"").fetchall()
#     off_count = len(offers)
#     for j, ad in enumerate(offers):
#         offer_pack = {'id': ad[0], 'views': ad[1], 'user_id': user_db_id}
#         sql = f"INSERT INTO offers({','.join(offer_pack.keys())}) VALUES ({','.join([f'{q}{p}{q}' for p in offer_pack.values()])})"
#         try:
#             database.execute(sql)
#         except IntegrityError:
#             pass
# try:
#     database.confirm()
# except IntegrityError:
#             pass


# for us in databaseold.execute(f"SELECT * FROM users").fetchall():
#     user = farpost_user.from_pack({'id': us[1], 'offers_count': us[2], 'phone': re.sub('\D', '', us[3]), 'is_scammed': 1})

#     # try:
#         database.save_object(user)
#     # except IntegrityError:
#     #     pass

#     for ad in databaseold.execute(f"SELECT * FROM ads WHERE \"user_id\" = \"{us[0]}\"").fetchall():
#         offer = farpost_offer.from_pack({'id': ad[0], 'views': ad[1], 'user_id': user.id})
#         # try:
#         #     database.save_object(offer)
#         # except IntegrityError:
#         #     pass