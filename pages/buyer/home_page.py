from pages.base_page import BasePage
from pages.buyer.login_page import Login_Page
from pages.buyer.oppo_shop import Oppo_Shop


class HomePage(BasePage):

    # def __init__(self):
    #     super().__init__()
    #     self.page_eles = load_yaml_file(buyer_yaml)[self.__class__.__name__]

    def click_User_Options_Card(self):
        ele_info = self.page_eles['点击个人选项卡']
        # ele_info = {"name":"点击个人选项卡","type":"css","value":".op-trk-event.fill","timeout":5}
        self.operate.click(ele_info)
        return self

    def click_Login_Page(self):
        ele_info = self.page_eles['点击登录']
        # ele_info = {"name":"点击登录","type":"linktext","value":"进入个人中心","timeout":5}
        self.operate.click(ele_info)
        return Login_Page()

    def click_oppo_shop(self):
        ele_info = self.page_eles['进入OPPO商城']
        # ele_info = {"name": "进入OPPO商城", "type": "xpath", "value": '(//span[text()="官方商城"]'), "timeout": 5}
        self.operate.click(ele_info)
        return Oppo_Shop()



class SearchResultPage(BasePage):
    def click_first_goods(self):
        ele_info = self.page_eles['第一个商品']
        self.operate.click(ele_info)
        # return LoginPage()