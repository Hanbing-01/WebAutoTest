from common.file_load import load_yaml_file
from pages.base_page import BasePage
from paths_manager import buyer_yaml


class Login_Page(BasePage):
    # def __init__(self):
    #     super().__init__()
    #     self.page_eles = load_yaml_file(buyer_yaml)[self.__class__.__name__]

    def send_username(self,username):
        ele_info = self.page_eles['手机号输入框']
        # ele_info =  {"name": "手机号输入框", "type": "css", "value": 'input[placeholder*="请输入手机号"]:first-of-type', "timeout": 5}
        self.operate.click(ele_info)
        self.operate.send_keys(ele_info,username)
        return self

    def send_password(self,password):
        ele_info = self.page_eles['密码输入框']
        # ele_info = {"name": "密码输入框", "type": "css", "value": 'input[placeholder*="请输入密码"]:first-of-type',

        self.operate.click(ele_info)
        self.operate.send_keys(ele_info,password)
        return self

    def click_login_btn(self):
        ele_info = self.page_eles['登录']
        # ele_info = {"name": "登录", "type": "css", "value": ".uc-motion-effect__change__item", "timeout": 5}
        self.operate.click(ele_info)
        return self

    def click_agree_btn(self):
        ele_info = self.page_eles['同意并继续']
        # ele_info = {"name": "同意并继续", "type": "xpath", "value": '(//*[text()="同意并继续"])', "timeout": 5}
        self.operate.click(ele_info)
        return self

