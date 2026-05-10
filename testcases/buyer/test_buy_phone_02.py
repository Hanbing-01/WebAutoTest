import allure
import pytest

from actions.buy_goods_action import BuyerOrderActions
from common.driver import DriverOperate
from common.file_load import load_yaml_file
from paths_manager import buy_phone_yaml

@allure.epic("oppo商城")
@allure.feature("购买商品_02")
class TestBuyNow_02:

    # pay_types = ['在线支付','货到付款']
    # receive_times = ['任意时间','仅工作日','仅休息日']
    colors = load_yaml_file(buy_phone_yaml)['BUY_PHONE']['colors']
    versions = load_yaml_file(buy_phone_yaml)['BUY_PHONE']['versions']
    @pytest.mark.parametrize('color', colors)
    @pytest.mark.parametrize('version', versions)
    def test_buy_phone_02(self,color,version):
        allure.dynamic.title(f'{color}与{version}')
        BuyerOrderActions().buy_now(color,version)
        # 完成断言
        flag = DriverOperate.globalDriverOperate.page_contains('收货地址')
        assert flag