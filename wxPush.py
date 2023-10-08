import datetime
from typing import List

import psutil
import requests


class WeChatPush:
    """
    微信push
    """
    GET = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    """
    参数	是否必须	说明
    grant_type	是	获取access_token填写client_credential
    appid	是	第三方用户唯一凭证
    secret	是	第三方用户唯一凭证密钥，即appsecret
    """

    POST = 'https://api.weixin.qq.com/cgi-bin/message/template/send'

    def __init__(self, appid: str = "wx1ab4e2cfd023e566", appsecret: str = "37ee6e881dca3bf737db6fe4f80e7d8a",
                 template_id: str = "jVwBIbfrOsPsMeM2tphM5CurhhwmdSP6OkII2U-EqRY",
                 touser: List[str] = ["oyk0762W9r6CRK0igLwSfpmbjvpY", "oyk0765M5cO-SI5NqyaB8XS2IJvw"], first_date=datetime.date(2023, 1, 11), server: str=''):
        # 和风天气
        key = '58c587185f7f4cb4ae38646ab7265a4e'
        location = '101290101'
        weather_api = f'https://devapi.qweather.com/v7/weather/now?key={key}&location={location}'
        weather = requests.get(weather_api, verify=False).json()
        self.appid = appid
        self.appsecret = appsecret
        self.touser = touser
        self.post_json = {
            "touser": '',
            "template_id": template_id,
            "url": "http://weixin.qq.com/download",
            "topcolor": "#FF0000",
            "data": {
                "nowDate": {
                    "value": str(datetime.datetime.now())[:-7],
                    "color": "#173177"
                },
                "city": {
                    "value": "昆明",
                    "color": "#173177"
                },
                "temp": {
                    "value": f"{weather.get('now', {}).get('temp', '未知')}",
                    "color": "#173177"
                },
                "feelsLike": {
                    "value": f"{weather.get('now', {}).get('feelsLike', '未知')}",
                    "color": "#99FF00" if int(weather.get('now', {}).get('feelsLike', 0)) < 24 else "#FF3300"
                },
                "weather": {
                    "value": f"{weather.get('now', {}).get('text', '未知')}",
                    "color": "#33FFFF"
                },
                "windDir": {
                    "value": f"{weather.get('now', {}).get('windDir', '未知') + weather.get('now', {}).get('windScale') + '级'}",
                    "color": "#FF9933" if int(weather.get('now', {}).get('windScale', 0)) < 4 else "#FF3300"
                },
                "windSpeed": {
                    "value": f"{weather.get('now', {}).get('windSpeed', '未知')}",
                    "color": "#FF9933" if int(weather.get('now', {}).get('windSpeed', 0)) < 4 else "#FF3300"
                },
                "loveDate": {
                    "value": (datetime.date.today() - first_date).days,
                    "color": "#173177"
                },
                "server": {
                    "value": server,
                    "color": "#173177"
                },
                "text": {
                    "value": "正常推送",
                    "color": "#0000FF"
                }
            }

        }

    def run(self):
        response_get = requests.get(self.GET, params={'appid': self.appid, 'secret': self.appsecret}, verify=False)
        for i in self.touser:
            self.post_json['touser'] = i
            access_token = response_get.json().get('access_token')
            response_post = requests.post(self.POST, params={'access_token': access_token}, json=self.post_json,
                                          verify=False)
            print(response_post.json())

    def check(self):
        with open("pid.txt", "r") as f:
            machine_pid = int(f.read())
        try:
            if psutil.Process(machine_pid).status() == psutil.STATUS_ZOMBIE:
                WeChatPush(server='已成僵尸进程').run()
        except psutil.NoSuchProcess:
            WeChatPush(server='进程意外退出').run()
        except Exception as e:
            WeChatPush(server='检测到意外情况').run()
        else:
            WeChatPush(server='正常运行').run()
