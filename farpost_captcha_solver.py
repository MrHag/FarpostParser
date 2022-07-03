from enum import Enum
from threading import Lock
from time import sleep
import requests
from browser import browser
from captcha_solver import captcha_solver
from request_master import request_master
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha


class SolveError(Exception):
    """Raised when the solve failed"""
    pass


class captcha_type(Enum):
    DEFAULT = 1
    PHONE = 2


class farpost_captcha_solver(captcha_solver):

    solver: TwoCaptcha

    def __init__(self, browser: browser, req_master: request_master, api_key: str):
        super().__init__(browser, req_master)
        self.solver = TwoCaptcha(api_key)

    def solve(self, req: requests.Request, type: captcha_type) -> str | None:
        brw = self.brw

        brw.open(req.url)

        print("Waiting for user")

        ret = None

        while True:

            if type == captcha_type.DEFAULT:
                if "verify" not in brw.current_url():
                    ret = brw.page_source()
                    break
                else:
                    # try:
                    #     sitekey = brw.execute_script('return /sitekey:"(.*)"/g.exec(grecap_onloaded.toString())[1]')

                    #     print(f"sitekey:{sitekey}")

                    #     reskey = self.solver.recaptcha(sitekey, brw.current_url())["code"]

                    #     print(f"reskey:{reskey}")

                    #     brw.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{reskey}"')

                    #     brw.execute_script('___grecaptcha_cfg.clients[0].L["L"].callback()')
                    # except Exception as e:
                    #     print("Error: ", e)
                    try:
                        brw.find_element_by_id("grecaptcha")
                        brw.execute_script(
                            'document.getElementById("grecap-fallback").click()')
                        while True:
                            brw.find_element_by_id("grecaptcha")
                            sleep(0.5)
                    except Exception:
                        pass

                    captcha_id = 0
                    try:
                        print("Waiting for answer")
                        base64_image = brw.execute_script(
                            'let img = [...document.getElementsByTagName("img")].filter((img)=>{ if(img.offsetParent != null) return img})[0];let canvas = document.createElement("canvas");canvas.width = img.width;canvas.height = img.height;let ctx = canvas.getContext("2d");ctx.drawImage(img, 0, 0);let dataURL = canvas.toDataURL("image/png");return dataURL')

                        # solve = self.solver.normal(base64_image, lang="ru")
                        # res = solve["code"]
                        # captcha_id = solve["captchaId"]

                        res = input("Enter: ")

                        print("Answer: ", res)

                        brw.execute_script(
                            f'[...document.getElementsByName("g-recaptcha-response")].filter((img)=>{{ if(img.offsetParent != null) return img}})[0].value = "{res}"')

                        brw.execute_script(
                            '[...document.getElementsByClassName("button")].filter((img)=>{{ if(img.offsetParent != null) return img}})[0].click()')

                    except Exception as e:
                        print("Error: ", e)
                        brw.open(req.url)

                    sleep(1)

                    is_correct = True
                    if "verify" in brw.current_url():
                        is_correct = False

                    try:
                        self.solver.report(captcha_id, is_correct)
                        print("Repost: ", str(is_correct))
                    except Exception:
                        pass

                    sleep(1)

            elif type == captcha_type.PHONE:
                # brw.wait_util(EC.url_changes(req.url))
                try:
                    captcha_id = 0
                    brw.find_element_by_class_name('bzr-captcha__image')
                    while True:
                        captcha_id = 0
                        try:
                            print("Waiting for answer")
                            base64_image = brw.execute_script(
                                'return /url\((.*)\)/g.exec(document.getElementsByTagName("style")[0].innerHTML)[1]')
                            # solve = self.solver.normal(base64_image, lang="ru")
                            # res = solve["code"]
                            # captcha_id = solve["captchaId"]
                            res = input("Enter: ")
                            print("Answer: ", res)
                            brw.execute_script(
                                f'document.getElementsByTagName("table")[0].children[0].children[0].children[2].children[0].value = "{res}"')
                            brw.execute_script(
                                'document.getElementsByClassName("captcha-button-wrap")[0].children[0].click()')
                        except Exception as e:
                            print("Error: ", e)
                            brw.open(req.url)

                        sleep(3)

                        brw.find_element_by_class_name('bzr-captcha__image')

                        if captcha_id != 0:
                            self.solver.report(captcha_id, False)
                            print("Repost: ", str(False))
                        brw.open(req.url)

                        sleep(3)

                except Exception:
                    if captcha_id != 0:
                        self.solver.report(captcha_id, True)
                        print("Repost: ", str(True))

                    if brw.current_url() == req.url:
                        ret = brw.page_source()
                        break

                    type = captcha_type.DEFAULT

        cookies = {}

        for cookie in brw.get_cookies():
            cookies[cookie["name"]] = cookie["value"]

        self.req_master.set_cookies(cookies)

        brw.delete_cookies()

        brw.open_default()

        return ret
