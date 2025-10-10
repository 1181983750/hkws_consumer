import base64
import json
import re
import traceback
from typing import Type, TypeVar

import requests
from requests.auth import HTTPDigestAuth

from httpAsyncClient.Config import Config
from httpAsyncClient.imageUpload.UPLOADORM import UPLOADORM
from httpAsyncClient.imageUpload.model import ImageFileds
from httpAsyncClient.models import hkws_xf_sbygxx
from public.utils.BaseOrm import BaseService
from public.utils.response_result import ResponseResult
from public.utils.sqlserver import SqlServerObject

image = TypeVar('image')


class UploadServices(BaseService):
    def __init__(self, model: Type[ImageFileds]):
        super(UploadServices, self).__init__(model=model)
        self.orm = UPLOADORM(model=model)
        self.sql_orm = SqlServerObject()


    def upload_image(self, image: image):
        """
        单一图片文件上传
        :param image: 必填 .png .jpg .gif
        :param
        :return:
        """
        picpath = f'{Config.rl_path}{image.name}'
        with open(picpath, 'wb') as pic:
            for base in image:
                pic.write(base)
        # img = Image.open(image)
        # img.save(picpath)
        # img_ser = serializer(data={"image": image})
        # img_ser.is_valid()
        # pic_obj = img_ser.save()
        try:
            self.orm.compressPicForScale(picpath, filename=image.name)
        except:
            traceback.print_exc()
            return ResponseResult('上传失败')
        else:
            print('存储成功')
        return ResponseResult(msg='存储成功', code=1)

    def upload_base64_image(self, base64_image: base64, filename: str):
        """
        base64编码上传
        :param base64_image: 编码
        :param filename: 文件名加后缀  员工id.jpg
        :return:
        """
        picpath = f'{Config.rl_path}{filename}'
        with open(picpath, 'wb') as pic:
            for c in base64_image.chunks():
                pic.write(c)
        try:
            self.orm.compressPicForScale(picpath, filename=filename)
        except Exception as e:
            traceback.print_exc()
            return ResponseResult(msg='上传失败', code=0)
        else:
            print('存储成功')
        ygid = re.sub(r'\D', '', filename)

        with open(picpath, "rb") as file:
            files = file.read()

        result_list = []
        for i in self.get_need_set_face_area_status_by_employee(ygid):
            result = self.handel_set_face_event(i['ygid'], i['ygmc'], files, i['sbip'], i['username'], i['password'])
            if result:
                hkws_xf_sbygxx.objects.filter(ygid=ygid, sbid=i['sbid'], issuccess=0).delete()
                hkws_xf_sbygxx.objects.create(ygid=ygid, sbid=i['sbid'], issuccess=1)

            result_list.append(result)
        if not all(result_list):
            return ResponseResult(msg='下发失败', code=0)
        return ResponseResult(msg='下发成功', code=1)
    @staticmethod
    def handel_set_face_event(ygid: int, ygmc: str, Pic: bytes, ip, username, password) -> bool:
        """
        此台消费机下发人脸
        @param ygid:
        @param ygmc:
        @param Pic:
        @param password:
        @param username:
        @param ip:
        @return: Boolean
        """
        boundary = "---------tyctyctyctyctyctyctyc"
        byte_pic = Pic.decode('ISO-8859-1')
        headers = {
            "Content-Type": "multipart/form-data; boundary=" + boundary,
            "Accept": "text/html, application/xhtml+xml",
            "Accept-Language": "zh-CN",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-"
        }
        send_json = json.dumps({
            "UserInfoAndRight": {
                "employeeNo": f"{ygid}",
                "deleteUser": False,
                "name": f"{ygmc}",
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
        payload = "--" + boundary + "\r\n" \
                  + "Content-Disposition: form-data; name=\"uploadStorageCloud\";\r\n" \
                  + "Content-Type: application/json\r\n" \
                  + "Content-Length: " + str(len(send_json)) + "\r\n\r\n" \
                  + send_json + "\r\n" \
                  + "--" + boundary + "\r\n" \
                  + "Content-Disposition: form-data; name=\"FacePicture\";\r\n" \
                  + "Content-Type: image/jpeg\r\n" \
                  + "Content-Length: " + str(len(byte_pic)) + "\r\n\r\n" \
                  + byte_pic + "\r\n" \
                  + "--" + boundary + "--\r\n"
        try:
            response = requests.post(f"http://{ip}/ISAPI/AccessControl/userInfoAndRight/setup?format=json",
                                          auth=HTTPDigestAuth(username, password),
                                          verify=False,
                                          data=payload,
                                          headers=headers,
                                          timeout=3)
        except Exception:
            return False

        if response.text.find("user info proc success") != -1 and response.text.find("face proc success") != -1:
            return True
        return False

    def get_need_set_face_area_status_by_employee(self, ygid):
        """
        获取需要下发的员工人脸区域状态
        @param ygid:
        @return:
        """
        sql = """
           SELECT
                a.ygid,
                b.ygdm,
                b.ygmc,
                b.pym,
                c.id AS sbid,
                c.sbip,
                username=c.userid,
                password=c.pass,
                a.issuccess 
            FROM
                hkws_xf_sbygxx a
                LEFT JOIN rs_ygxx b ON a.ygid = b.id
                LEFT JOIN hkws_xf_sbmx c ON a.sbid = c.id 
            WHERE
                a.issuccess = 0 
                AND c.ty = 0 
                AND b.sflz = 0 
                AND c.ty = 0 
                AND a.ygid=%s
        
        """
        result_set, column_list = self.sql_orm.query_data(sql, [ygid])
        data_list = [dict(zip(column_list, row)) for row in result_set]

        return data_list