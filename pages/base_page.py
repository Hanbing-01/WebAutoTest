from common.driver import DriverOperate
from common.file_load import load_yaml_file
from paths_manager import buyer_yaml



class BasePage:

    def __init__(self):
        self.operate:DriverOperate=DriverOperate.globalDriverOperate
        self.page_eles = load_yaml_file(buyer_yaml)[self.__class__.__name__]
