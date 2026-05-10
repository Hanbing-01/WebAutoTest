import os
import threading
from typing import List

import allure
import pytest
import time

from PIL import Image
from common.driver import DriverOperate
from common.file_load import load_yaml_file, write_yaml
from common.logger import GetLogger
from actions.user_login_action import User_Login_Action
from paths_manager import project_path, common_yaml

GLOBAL_START_TIME = time.time()

def pytest_collection_modifyitems(config:"Config",items:List["Item"]):
    # items对象是pytest收集到的所有用例对象
    # 获取pytest.ini中的addopts值
    try:
        addopts = config.getini('addopts')
        if "--dist=each" in addopts:
            # 此时说明你要用的是多进程并发，我要得到当前的worker_id
            worker_id = config.workerinput.get('workerid')
        else:
            worker_id = None
    except:
        worker_id = None
    for item in items:
        # item就代表了一条用例
        if worker_id:
            item.originalname = item.originalname.encode('utf-8').decode("unicode-escape")+worker_id
            item._nodeid = item._nodeid.encode('utf-8').decode("unicode-escape")+worker_id
        else:
            item._nodeid = item._nodeid.encode('utf-8').decode("unicode-escape")


@pytest.fixture(scope='session',autouse=True)
def aalogger_init(worker_id):
    GetLogger.get_logger(worker_id).info('日志初始化成功')

@pytest.fixture(scope='session',autouse=True)
def get_common_info():
    return load_yaml_file(common_yaml)

@pytest.fixture(scope='session',autouse=True)
def init_driver(get_browser,worker_id,get_common_info):
    remote_url = get_common_info.get('remote_url')
    DriverOperate.globalDriverOperate = DriverOperate(browser=get_browser, remote_url=remote_url)
    OPPOHost = get_common_info['OPPOHost']
    DriverOperate.globalDriverOperate.get(OPPOHost)
    UserName = get_common_info['UserName']
    UserPwd = get_common_info['UserPwd']
    if worker_id == 'master' or worker_id == 'gw0':
        User_Login_Action().user_login(UserName[0],UserPwd[0])
    else:
        index = int(worker_id[2:])
        User_Login_Action().user_login(UserName[index], UserPwd[index])
    DriverOperate.globalDriverOperate.switch_to_default()
    yield
    DriverOperate.globalDriverOperate.quit()
    for img in os.listdir(f'{project_path}/video'):
        if img.startswith(worker_id):
            os.remove(f'{project_path}/video/{img}')


@pytest.fixture(scope='function',autouse=True)
def case_setup(worker_id):
    # 创建线程
    # target表示该线程要执行的动作，只写函数名称就行
    # args指的是这个要执行的函数执行时所需要的参数
    thd = threading.Thread(target=shot,args=(DriverOperate.globalDriverOperate,worker_id))
    thd.start()


@pytest.fixture(scope='function',autouse=True)
def case_teardown(worker_id,get_common_info):
    yield
    global shot_flag
    shot_flag = False
    # 完成当前用例临时图片的拼接，形成gif动态图
    img_list = [] # 存储很多个图片名称
    # 图片命名gw0_0.png/gw0_1.png/gw0_2.png
    for img in os.listdir(f'{project_path}/video'):
        if img.startswith(worker_id) and img.endswith('.png'):
            img_list.append(img)

    # 从目录得到的所有图片名称排序可能是不对的，拼接gif必须按照顺序来
    # 针对img_list中的图片名称进行排序
    img_list.sort(key=lambda name: int(name.split('_')[1][:-4]))

    # 要做图片拼接，需要用到一个库：pillow
    # pip install pillow -i https://pypi.douban.com/simple
    first_img = Image.open(f'{project_path}/video/{img_list[0]}')
    eles_img = [] # 存储除了第一张图片以外的其他图片的二进制对象
    for img in img_list[1:]:
        cur_img = Image.open(f'{project_path}/video/{img}')
        eles_img.append(cur_img)
    # 完成拼接
    first_img.save(f'{project_path}/video/{worker_id}record.gif',
                   append_images=eles_img,
                   duration=300,#每隔多长时间播放一张图片，单位是毫秒
                   save_all=True,
                   loop=1,# 表示循环播放次数
                   )

    # 将生成的gif动态图放入到allure测试报告之中
    with open(f'{project_path}/video/{worker_id}record.gif',mode='rb') as f:
        allure.attach(f.read(),attachment_type=allure.attachment_type.GIF)

    DriverOperate.globalDriverOperate.close_windows_until_only_one()

    OPPOHost = get_common_info['OPPOHost']
    DriverOperate.globalDriverOperate.get(OPPOHost)
    DriverOperate.globalDriverOperate.switch_to_default()

@pytest.hookimpl(tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield # 得到用例执行之后的对象
    res = outcome.get_result() # 获取当前用例执行结果状态
    if res.when == 'call' and res.failed:
        # 做截图
        # 因为我要把截图放在allure的测试报告上，所以这里截图需要得到截图的二进制对象
        img = DriverOperate.globalDriverOperate.get_screenshot_as_png()
        # 加到allure测试报告上
        allure.attach(img,'失败截图',attachment_type=allure.attachment_type.PNG)

# 这是pytest的一个自带的钩子函数，名称是固定的
# 可以用来定义命令行参数
def pytest_addoption(parser):
    parser.addoption('--browsers',action='store')


@pytest.fixture(scope='session',autouse=True)
def get_browser(request,worker_id):
    # 得到--browsers对应的chrome,edge
    browsers = request.config.getoption('--browsers')
    if browsers:
        # 将得到的browsers转成列表
        browsers_list = browsers.split(',') # ['chrome','edge']
        if worker_id == 'master':
            return browsers_list[0]
        else:
            # gw0/gw1/gw2/gw3
            index = int(worker_id[2:])
            return browsers_list[index]
    else:
        return 'chrome'

# dr代表全局操作对象
# worker_id代表当前进行id，写他主要是因为多进程并发为了区分不同进程下的截图
def shot(dr,worker_id):
    # 图片命名gw0_0.png/gw0_1.png/gw0_2.png
    # 图片命名gw1_0.png/gw1_1.png/gw1_2.png
    # 每次截图开始前，都去清除当前进程下的临时图片及gif动态图
    for img in os.listdir(f'{project_path}/video'):
        if img.startswith(worker_id):
            os.remove(f'{project_path}/video/{img}')

    global shot_flag # 全局变量，用来标识每条用例截图的开始和结束
    shot_flag=True
    i=0 # 用来给图片命名顺
    while shot_flag:
        # 只要shot_flag为True，那么这个循环就会一直截图
        # 调用全局对象的截图方法，生成临时图片
        try:
            dr.get_screenshot_as_file(f'{project_path}/video/{worker_id}_{i}.png')
            time.sleep(0.3)
            i+=1
        except:
            return

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """统计测试结果"""
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed+failed+error+skipped
    duration = time.time() - GLOBAL_START_TIME
    print('total times:', duration, 'seconds')
    write_yaml('result.yml',{"total":total,"passed":passed,"failed":failed,"skipped":skipped,"error":error})