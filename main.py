import json

import requests
from requests.auth import HTTPDigestAuth

def request():
    print('发送请求')


    send_json_str = json.dumps({
        "UserInfoAndRight": {
            "employeeNo": "199811",
            "deleteUser": False,
            "name": "童羿诚",
            "userType": "normal",
            "Valid": {
                "enable": False,
                "beginTime": "1970-01-01T00:00:00+00:00",
                "endTime": "2037-12-31T23:59:59+00:00",
            },
            "password": "123456",
            "RightPlan": [
                {
                    "doorNo": 1
                }
            ],
            "localUIRight": False,
            "userVerifyMode": "face",
            "FaceInfo": {
                "List": [
                    {
                        "FDID": "1",
                        "faceID": 1,
                        "faceName": "FacePicture"
                    }
                ],
            }
        },
    })

    boundary = "--------------7e13971310878"
    headers = {"Content-Type": "multipart/form-data; boundary=" + boundary,
               "Accept": "text/html, application/xhtml+xml",
               "Accept-Language": "zh-CN",
               "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "Keep-Alive",
               "Cache-Control": "no-"}
    file1 = open("static_files/images/199811.jpg", "rb")
    byte_pic = file1.read().decode('ISO-8859-1')

    payload = "--" + boundary + "\r\n" \
              + "Content-Disposition: form-data; name=\"uploadStorageCloud\";\r\n" \
              + "Content-Type: application/json\r\n" \
              + "Content-Length: " + str(len(send_json_str)) + "\r\n\r\n" \
              + send_json_str + "\r\n" \
              + "--" + boundary + "\r\n" \
              + "Content-Disposition: form-data; name=\"FacePicture\";\r\n" \
              + "Content-Type: image/jpeg\r\n" \
              + "Content-Length: " + str(len(byte_pic)) + "\r\n\r\n" \
              + byte_pic \
              + "\r\n--" + boundary + "--\r\n"

    resp = requests.post('http://172.17.18.224/ISAPI/AccessControl/userInfoAndRight/setup?format=json', data=payload,
                         timeout=10, headers=headers, auth=HTTPDigestAuth('admin', 'a1111111'))

    print(resp.text)
    file1.close()



request()