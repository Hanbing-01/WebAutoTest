import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from common.logger import GetLogger




# 自定义封装一个点击元素直到成功的显式等待条件
def click_success(locator): # locator = (By.ID,'XXXX')
    def _predicate(driver):
        try:
            element = driver.find_element(*locator)
            element.click()
            return True
        except:
            print('点击报错了')
            return False
    return _predicate


class DriverOperate:

    # 利用类属性定义一个全局的核心操作对象，他的赋值未来必须在conftest中完成
    globalDriverOperate = None

    # 这个类将会封装我们所有的和之前的所有动作
    # 在之后我们的这个框架，将会调用该类对象提供的各种动作来实现操作
    # remote_url是selenium grid注册中心的接口地址
    def __init__(self, browser='chrome', remote_url=None):
        self.logger = GetLogger.get_logger()
        self.browser = browser.lower()
        if remote_url:
            # 要执行selenium grid方式
            if self.browser == 'chrome':
                options = webdriver.ChromeOptions()

            elif self.browser == 'firefox':
                options = webdriver.FirefoxOptions()

            elif self.browser == 'edge':
                options = webdriver.EdgeOptions()

            elif self.browser == 'ie':
                options = webdriver.IeOptions()

            elif self.browser == 'safari':
                options = webdriver.safari.options.Options()

            else:
                self.logger.error(f'{self.browser} 浏览器不支持')
                raise BaseException(f'{self.browser} 浏览器不支持')
            options.page_load_strategy = 'eager'  # 页面较快
            self.driver = webdriver.Remote(remote_url, options=options)
        else:
            if self.browser == 'chrome':
                options = webdriver.ChromeOptions()
                self.driver = webdriver.Chrome(options=options)
            elif self.browser == 'firefox':
                options = webdriver.FirefoxOptions()
                self.driver = webdriver.Firefox(options=options)
            elif self.browser == 'edge':
                options = webdriver.EdgeOptions()
                self.driver = webdriver.Edge(options=options)
            elif self.browser == 'ie':
                options = webdriver.IeOptions()
                self.driver = webdriver.Ie(options=options)
            elif self.browser == 'safari':
                options = webdriver.safari.options.Options()
                self.driver = webdriver.Safari(options=options)
            else:
                self.logger.error(f'{self.browser} 浏览器不支持')
                raise BaseException(f'{self.browser} 浏览器不支持')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.logger.info(f'{self.browser} 启动成功')

    def get(self,url):
        self.driver.get(url)
        self.logger.info(f'{url} 打开成功')

    def find_element(self,ele_info):
        # ele_info = {"name":"登录链接","type":"linktext","value":"登录","timeout":5}
        # ele_info的数据格式是我们自行设计的，代表某个元素的基本信息,timeout可以不写，默认5秒超时
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout',5)
        locator = self.get_by(ele_info)
        # 使用显式等待来完成元素定位
        try:
            wait = WebDriverWait(driver=self.driver,timeout=timeout)
            element = wait.until(expected_conditions.presence_of_element_located(locator))
            self.logger.info(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位成功')
            return element
        except BaseException as e:
            self.logger.exception(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位失败')
            raise BaseException(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位失败:{e}')

    def find_elements(self,ele_info):
        # ele_info = {"name":"登录链接","type":"linktext","value":"登录","timeout":5}
        # ele_info的数据格式是我们自行设计的，代表某个元素的基本信息,timeout可以不写，默认5秒超时
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout',5)
        locator = self.get_by(ele_info)
        # 使用显式等待来完成元素定位
        try:
            wait = WebDriverWait(driver=self.driver,timeout=timeout)
            element_list = wait.until(expected_conditions.presence_of_all_elements_located(locator))
            self.logger.info(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位成功{len(element_list)}个')
            return element_list
        except BaseException as e:
            self.logger.exception(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位失败')
            raise BaseException(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位失败:{e}')
    def get_by(self,ele_info):
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout',5)
        if type == 'id':
            locator = (By.ID,value)
        elif type == 'name':
            locator = (By.NAME, value)
        elif type == 'classname':
            locator = (By.CLASS_NAME, value)
        elif type == 'tagname':
            locator = (By.TAG_NAME, value)
        elif type == 'linktext':
            locator = (By.LINK_TEXT, value)
        elif type == 'partiallinktext':
            locator = (By.PARTIAL_LINK_TEXT, value)
        elif type == 'css':
            locator = (By.CSS_SELECTOR, value)
        elif type == 'xpath':
            locator = (By.XPATH, value)
        else:
            self.logger.error(f'定位类型{type} 不支持')
            raise BaseException(f'定位类型{type} 不支持')
        return locator

    def click(self,ele_info):
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout',5)
        locator = self.get_by(ele_info)
        try:
            wait = WebDriverWait(driver=self.driver,timeout=timeout)
            wait.until(click_success(locator))
            self.logger.info(f'点击元素【{name}】,通过【{type}】,值是【{value}】,点击成功')
        except BaseException as e:
            self.logger.exception(f'点击元素【{name}】,通过【{type}】,值是【{value}】,点击失败')
            raise BaseException(f'点击元素【{name}】,通过【{type}】,值是【{value}】,点击失败:{e}')
    def send_keys(self,ele_info,text,is_clear=True):
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout',5)
        element = self.find_element(ele_info)
        try:
            if is_clear:
                element.clear()
            element.send_keys(text)
            self.logger.info(f'向元素【{name}】,通过【{type}】,值是【{value}】,输入【{text}】成功')
        except BaseException as e:
            self.logger.exception(f'向元素【{name}】,通过【{type}】,值是【{value}】,输入【{text}】失败')
            raise BaseException(f'向元素【{name}】,通过【{type}】,值是【{value}】,输入【{text}】失败:{e}')

    def switch_to_window(self,index=1):
        """
        切换新窗口
        :param index:默认是1,表示切换到第2个窗口
        :return:
        """
        try:
            window_handles = self.driver.window_handles
            self.driver.switch_to.window(window_handles[index])
            self.logger.info(f'切换到第{index+1}个新窗口成功')
        except BaseException as e:
            self.logger.exception(f'切换到第{index+1}个新窗口失败')
            raise BaseException(f'切换到第{index+1}个新窗口失败:{e}')

    def switch_to_frame(self,frame):
        """
        切换iframe
        :param frame:
        :return:
        """
        try:
            self.driver.switch_to.frame(frame)
            self.logger.info(f'切换到iframe:【{frame}】成功')
        except BaseException as e:
            self.logger.exception(f'切换到iframe:【{frame}】失败')
            raise BaseException(f'切换到iframe:【{frame}】失败:{e}')

    def switch_to_default(self):
        self.driver.switch_to.default_content()
        self.logger.info(f'切换到默认页面成功')
    def switch_to_parent(self):
        self.driver.switch_to.parent_frame()
        self.logger.info(f'切换到父级frame成功')

    def page_contains(self,text,timeout=5):
        try:
            wait = WebDriverWait(driver=self.driver,timeout=timeout)
            wait.until(lambda d:text in d.page_source)
            self.logger.info(f'判断页面包含【{text}】成功')
            return True
        except BaseException as e:
            self.logger.exception(f'判断页面包含【{text}】失败')
            return False

    def is_element_exist(self,ele_info):
        """
        判断元素是否存在
        :param ele_info:
        :return:
        """
        # try:
        #     self.find_element(ele_info)
        #     return True
        # except BaseException as e:
        #     return False
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout', 5)
        locator = self.get_by(ele_info)
        # 使用显式等待来完成元素定位
        try:
            wait = WebDriverWait(driver=self.driver, timeout=timeout)
            element = wait.until(expected_conditions.presence_of_element_located(locator))
            self.logger.info(f'定位元素【{name}】,通过【{type}】,值是【{value}】,定位成功')
            return True
        except:
            return False

    def move_to_element(self,ele_info):
        name = ele_info['name']
        type = ele_info['type']
        value = ele_info['value']
        timeout = ele_info.get('timeout',5)
        element = self.find_element(ele_info)
        action = ActionChains(self.driver)
        try:
            action.move_to_element(element).perform()
            self.logger.info(f'光标移动到元素【{name}】,通过【{type}】,值是【{value}】,成功')
        except BaseException as e:
            self.logger.exception(f'光标移动到元素【{name}】,通过【{type}】,值是【{value}】,失败')
            raise BaseException(f'光标移动到元素【{name}】,通过【{type}】,值是【{value}】,失败:{e}')
    def get_text(self,ele_info):
        element = self.find_element(ele_info)
        text = element.text
        self.logger.info(f'获取元素【{ele_info["name"]}】的文字是:{text}')
        return text
    def get_attribute(self,ele_info,attr_name):
        element = self.find_element(ele_info)
        value = element.get_attribute(attr_name)
        self.logger.info(f'获取元素【{ele_info["name"]}】的属性【{attr_name}】是:{value}')
        return value

    def get_screenshot_as_file(self,filename):
        try:
            self.driver.get_screenshot_as_file(filename)
            self.logger.info(f'截图成功,保存文件【{filename}】')
        except BaseException as e:
            self.logger.exception(f'截图失败')
            raise BaseException(f'截图失败')

    def get_screenshot_as_png(self):
        return self.driver.get_screenshot_as_png()

    def quit(self):
        self.driver.quit()

    def close_windows_until_only_one(self):
        # 关闭多余窗口只剩下一个
        window_handles = self.driver.window_handles # [1,2,3,4]
        # 把第一个留下，从第二个窗口开始遍历逐个关闭
        for i in range(1,len(window_handles)):
            self.driver.switch_to.window(window_handles[i])
            self.driver.close()
        self.driver.switch_to.window(window_handles[0])

    # def switch_to_frame(self, iframe_name):
    #     iframe = self.driver.find_element(
    #         By.CSS_SELECTOR,
    #         iframe_name
    #     )
    #     self.driver.switch_to.frame(iframe)
    # def back_to_default_content(self):
    #     self.driver.switch_to.default_content()

# 以上方法 如果还需要用到其他操作 再到这里追加

if __name__ == '__main__':
    operate = DriverOperate(browser='chrome')
    operate.get('https://www.oppo.com/cn/')
    # ele_info = {"name": "oppo商城", "type": "linktext", "value": "官方商城", "timeout": 5}
    # operate.click(ele_info)

    ele_info = {"name":"登陆图标","type":"css","value":".op-trk-event.fill","timeout":5}
    operate.click(ele_info)
    ele_info = {"name": "账号登录链接", "type": "css", "value": ".sign-in.op-trk-event", "timeout": 15}
    operate.click(ele_info)
    ele_info = {"name": "iframe", "type": "css", "value": "iframe[id^='heytap_popper_login']", "timeout": 5}
    iframe = operate.find_element(ele_info)
    operate.switch_to_frame(iframe)
    ele_info = {"name": "用户名输入框", "type": "css", "value": 'input[placeholder*="请输入手机号"]:first-of-type', "timeout": 5}
    operate.click(ele_info)
    operate.send_keys(ele_info,'15996293871')
    ele_info = {"name": "密码输入框", "type": "css", "value": 'input[placeholder*="请输入密码"]:first-of-type',
                "timeout": 5}
    operate.send_keys(ele_info, 'hanbing11111')
    ele_info = {"name": "点击登录", "type": "css", "value": ".uc-motion-effect__change__item", "timeout": 5}
    operate.click(ele_info)
    ele_info = {"name": "同意并继续", "type": "xpath", "value": '(//*[text()="同意并继续"])', "timeout": 5}
    operate.click(ele_info)
    operate.switch_to_default()
    time.sleep(10)
