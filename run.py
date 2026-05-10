import os

import pytest

if __name__ == '__main__':
    pytest.main()

    # 这个是直接打开测试报告，仅仅用于本地自己看
    os.system('allure serve report/data')