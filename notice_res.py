import sys

import jsonpath
import requests

from common.file_load import load_yaml_file


class FeiShuNotice:

    def send(self,job_name,build_number,result,user,build_url):
        self.res = load_yaml_file('result.yml')
        url = 'https://open.feishu.cn/open-apis/bot/v2/hook/389e6f47-3b2a-4a06-9267-42111de42f16'
        method = 'post'
        json = {
                "msg_type": "post",
                "content": {
                        "post": {
                                "zh_cn": {
                                        "title": f"{job_name}第{build_number}次测试完成",
                                        "content": [
                                            [{
                                                "tag": "text",
                                                "text": f"状态:{result}"
                                            }],
                                            [{
                                                "tag": "text",
                                                "text": f"用例总数:{self.res['total']}"
                                            }],
                                            [{
                                                "tag": "text",
                                                "text": f"成功:{self.res['passed']}"
                                            }],
                                            [{
                                                "tag": "text",
                                                "text": f"失败:{self.res['failed']}"
                                            }],
                                            [{
                                                "tag": "text",
                                                "text": f"跳过:{self.res['skipped']}"
                                            }],
                                            [{
                                                "tag": "text",
                                                "text": f"错误:{self.res['error']}"
                                            }],
                                            [{
                                                "tag": "text",
                                                "text": f"执行人:{user}"
                                            }],
                                            [{
                                                "tag": "a",
                                                "text": "查看报告",
                                                "href": f"{build_url}/allure"
                                            }],

                                        ]
                                }
                        }
                }
        }
        resp = requests.request(method=method,
                                url=url,
                                json=json)
        return resp
class WxNotice:

    def send(self,job_name,build_number,result,user,build_url):
        self.res = load_yaml_file('result.yml')
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=93cafed7-8287-4fcc-8ff8-7fa21390b959'
        method = 'post'
        json = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"#### {job_name}测试完成  \n - 任务：第{build_number}次\n - 状态：{result} \n - 用例总数: {self.res['total']} \n - 成功: {self.res['passed']} \n - 失败: {self.res['failed']} \n - 错误: {self.res['error']} \n - 跳过: {self.res['skipped']} \n - 执行人: {user}  \n[查看报告]({build_url}/allure) "
            }
        }
        resp = requests.request(method=method,
                         url=url,
                         json = json)
class DingDingNotice:
    def send(self,job_name,build_number,result,user,build_url):
        self.res = load_yaml_file('result.yml')
        url = 'https://oapi.dingtalk.com/robot/send?access_token=eda69535b902dfc3f009aba101c407cf11e1e68e758b194d4a232f42f1ad1aca'
        method = 'post'
        json = {
            "msgtype": "markdown",
            "markdown": {
                "title":f"### {job_name}测试完成",
                "text": f"### {job_name}测试完成 \n - 任务：第{build_number}次\n - 状态：{result} \n - 用例总数: {self.res['total']} \n - 成功: {self.res['passed']} \n - 失败: {self.res['failed']} \n - 错误: {self.res['error']} \n - 跳过: {self.res['skipped']} \n - 执行人: {user}  \n[查看报告]({build_url}/allure) "
            }
        }
        resp = requests.request(method=method,
                         url=url,
                         json = json)
class JenkinsStatus:
    # 1. 构造方法接收 用户名 和 token
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def send(self,build_url):
        url = f'{build_url}/api/json'
        method = 'get'
        # 2. 请求时带上 auth —— 标准、规范、公司通用写法
        resp = requests.request(
            method=method,
            url=url,
            auth=(self.username, self.token)  # 👈 这就是你要的认证
        )
        print(resp)
        return resp
# ==========================================================================

if __name__ == '__main__':
    args = sys.argv
    build_url = args[1]
    notice_type = args[2]

    # build_url = 'http://118.89.124.97:8080/job/apiautotest20260417/49'
    # notice_type = 'feishu'

    # ===================== 这里填写你自己的 Jenkins 信息 =====================
    USERNAME = "admin"          # 你的Jenkins账号
    API_TOKEN = "11fb21b7150d2dfa09eccc27eed6e260f5"  # 你的API token
    # ==========================================================================

    try:
        # ===================== 调用时传入 =====================
        resp = JenkinsStatus(USERNAME, API_TOKEN).send(build_url)
        # ======================================================

        if resp.status_code != 200:
            raise Exception(f"请求失败，状态码：{resp.status_code}")

        user = jsonpath.jsonpath(resp.json(), '$..shortDescription')[0]
        result = jsonpath.jsonpath(resp.json(), '$..result')[0]
        fullDisplayName = jsonpath.jsonpath(resp.json(), '$..fullDisplayName')[0]
        print(user)
        print(fullDisplayName)

    except Exception as e:
        print(f"获取 Jenkins 信息失败: {e}")
        user = "未知用户"
        result = "FAILURE"
        fullDisplayName = "未知任务 #1"

    job_name = fullDisplayName.split(' #')[0]
    build_number = fullDisplayName.split(' #')[1]

    if notice_type == 'wx':
        WxNotice().send(job_name, build_number, result, user, build_url)
    elif notice_type == 'dd':
        DingDingNotice().send(job_name, build_number, result, user, build_url)
    elif notice_type == 'feishu':
        FeiShuNotice().send(job_name, build_number, result, user, build_url)