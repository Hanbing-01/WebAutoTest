import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.file_load import load_yaml_file
from pages.base_page import BasePage
from paths_manager import buyer_yaml



class Phone_Details(BasePage):
    # def __init__(self):
    #     super().__init__()
    #     self.page_eles = load_yaml_file(buyer_yaml)[self.__class__.__name__]
    def click_agree(self):
        ele_info = self.page_eles['点击同意']
        # ele_info = {"name":"点击同意,"type": "xpath", "value": '//span[text()="同意"]/parent::button', "timeout": 5}
        if self.operate.is_element_exist(ele_info):
            self.operate.click(ele_info)
        return self


    def close_cookie_msg(self):
        ele_info = self.page_eles['关闭cookie提示']
        # ele_info = {"name":"关闭cookie提示,"type": "css", "value": '.v-icon.notranslate.close-icon.close.v-icon--link.mdi.mdi-window-close.theme--light', "timeout": 5}
        if self.operate.is_element_exist(ele_info):
            self.operate.click(ele_info)
        return self
    def select_green(self):
        ele_info = self.page_eles['选择青色']
        # ele_info = {"name":"选择青色","type": "xpath", "value": '//*[text()="乘风青"]/ancestor::button', "timeout": 5}
        self.operate.click(ele_info)
        return self
    def select_white(self):
        ele_info = self.page_eles['选择白色']
        # ele_info = {"name":"选择白色","type": "xpath", "value": '//*[text()="乘风青"]/ancestor::button', "timeout": 5}
        self.operate.click(ele_info)
        return self
    def select_twelve(self):
        ele_info = self.page_eles['选择12GB']
        # ele_info = {"name":"选择12GB","type": "xpath", "value": '//*[text()="12GB+256GB"]/ancestor::button', "timeout": 5}
        self.operate.click(ele_info)
        return self


    def select_sixteen(self):
        ele_info = self.page_eles['选择16GB']
        # ele_info = {"name":"选择16GB","type": "xpath", "value": '// span[contains(text(), "买 1 年送 1 年")] / ancestor::button', "timeout": 5}
        self.operate.click(ele_info)
        return self
    def select_other(self):
        ele_info = self.page_eles['选择其他']
        # ele_info = {"name":"选择其他","type": "xpath", "value": '// span[contains(text(), "买 1 年送 1 年")] / ancestor::button', "timeout": 5}
        self.operate.click(ele_info)
        return self

    def order_now(self):
        ele_info = self.page_eles['立即购买']
        # ele_info = {"name":"立即购买","type": "xpath", "value": '// p[text() = "立即购买"] / ancestor::button', "timeout": 5}
        self.operate.click(ele_info)
        time.sleep(10)
        return self