import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.file_load import load_yaml_file
from pages.base_page import BasePage
from pages.buyer.phone_detail import Phone_Details
from paths_manager import buyer_yaml



class Oppo_Shop(BasePage):
    # def __init__(self):
    #     super().__init__()
    #     self.page_eles = load_yaml_file(buyer_yaml)[self.__class__.__name__]
    def click_select(self):
        ele_info = self.page_eles['点击搜索框']
        # ele_info = {"name":"点击搜索框","type": "css", "value": 'input[placeholder*="OPPO好物狂欢节额"]:first-of-type', "timeout": 5}
        self.operate.click(ele_info)
        return self

    def click_phone(self):
        ele_info = self.page_eles['立即抢购']
        # ele_info = {"name":"立即抢购","type": "css", "value": 'input[placeholder*="OPPO好物狂欢节额"]:first-of-type', "timeout": 5}
        self.operate.click(ele_info)
        time.sleep(7)
        return Phone_Details ()