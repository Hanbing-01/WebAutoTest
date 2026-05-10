from common.driver import DriverOperate
from pages.buyer.oppo_shop import Oppo_Shop
from pages.buyer.home_page import HomePage
from actions.user_login_action import User_Login_Action
from common.driver import DriverOperate
from pages.buyer.phone_detail import Phone_Details


class BuyerOrderActions:

    def buy_now(self, color, version):
        HomePage().click_oppo_shop()
        DriverOperate.globalDriverOperate.switch_to_window()
        Oppo_Shop().click_phone()
        DriverOperate.globalDriverOperate.switch_to_window(2)
        Phone_Details().click_agree().close_cookie_msg()
        if color == 'green':
            Phone_Details().select_green()
        else:
            Phone_Details().select_white()
        if version == '12GB':
            Phone_Details().select_twelve()
        else:
            Phone_Details().select_sixteen()

        # Phone_Details().select_other().order_now()
        Phone_Details().order_now()


# if __name__ == '__main__':
#     DriverOperate.globalDriverOperate = DriverOperate(browser='chrome')
#     DriverOperate.globalDriverOperate.get('https://www.oppo.com/cn/')
#     User_Login_Action().user_login('15996293871', 'hanbing11111')
#     DriverOperate.globalDriverOperate.switch_to_default()
#     BuyerOrderActions().buy_now(color, version)