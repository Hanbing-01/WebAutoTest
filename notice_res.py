import sys

import jsonpath
import requests

from common.file_load import load_yaml_file


class FeiShuNotice:

    def send(self,job_name,build_number,result,user,build_url):
        self.res = load_yaml_file('result.yml')
        url = 'https://open.feishu.cn/open-apis/bot/v2/hook/b78ec614-0108-4a81-b752-6c4fe1d32eda'
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
    def send(self,build_url):
        url = f'{build_url}/api/json'
        method = 'get'
        resp = requests.request(method=method,url=url)
        return resp
if __name__ == '__main__':
    args = sys.argv # 表示获取终端执行时传递的参数
    build_url = args[1]
    notice_type = args[2] # 通知类型，是飞书还是钉钉还是企微
    # job_name = 'apiautotest20230805'
    # build_number = 3
    # build_url = 'http://192.168.0.188:8080/job/apiautotest20230805/3'
    resp = JenkinsStatus().send(build_url)
    user = jsonpath.jsonpath(resp.json(),'$..shortDescription')[0]
    result = jsonpath.jsonpath(resp.json(), '$..result')[0]
    fullDisplayName = jsonpath.jsonpath(resp.json(),'$..fullDisplayName')[0]
    # apiautotest20230805 #3
    job_name = fullDisplayName.split(' #')[0]
    build_number = fullDisplayName.split(' #')[1]
    if notice_type == 'wx':
        WxNotice().send(job_name,build_number,result,user,build_url)
    elif notice_type == 'dd':
        DingDingNotice().send(job_name,build_number,result,user,build_url)
    elif notice_type == 'feishu':
        FeiShuNotice().send(job_name,build_number,result,user,build_url)
