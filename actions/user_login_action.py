import time

from pages.buyer.home_page import HomePage
from pages.buyer.login_page import Login_Page
from common.driver import DriverOperate

class User_Login_Action:

    def user_login(self,username,password):

        HomePage().click_User_Options_Card().click_Login_Page()
        ele_info = {"name": "iframe", "type": "css", "value": "iframe[id^='heytap_popper_login']", "timeout": 5}
        iframe = DriverOperate.globalDriverOperate.find_element(ele_info)
        DriverOperate.globalDriverOperate.switch_to_frame(iframe)
        Login_Page().send_username(username).send_password(password).click_login_btn().click_agree_btn()
        time.sleep(10)
        # 链式调用

if __name__ == '__main__':

    User_Login_Action().user_login('15996293871','hanbing11111')