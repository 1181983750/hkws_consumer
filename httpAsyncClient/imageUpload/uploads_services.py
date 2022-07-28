import base64
import traceback
from typing import Type, TypeVar

from httpAsyncClient.Config import Config
from httpAsyncClient.imageUpload.UPLOADORM import UPLOADORM
from httpAsyncClient.imageUpload.model import ImageFileds
from public.utils.BaseOrm import BaseService
from public.utils.response_result import ResponseResult

image = TypeVar('image')


class UploadServices(BaseService):
    def __init__(self, model: Type[ImageFileds]):
        super(UploadServices, self).__init__(model=model)
        self.orm = UPLOADORM(model=model)

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
        :param filename: 文件名加后缀
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
            return ResponseResult(msg='上传失败')
        else:
            print('存储成功')

        return ResponseResult(msg='存储成功', code=1)
