import os
from typing import Type

from PIL import Image

from httpAsyncClient.imageUpload.model import ImageFileds
from public.utils.BaseOrm import BaseORM


class UPLOADORM(BaseORM):
    def __init__(self, model: Type[ImageFileds]):
        super(UPLOADORM, self).__init__(model=model)
        self.model = model

<<<<<<< HEAD
    def compressPicForScale(self,picpath: str, desFileSize: int=200, filename: str=None):
=======
    def compressPicForScale(self, picpath: str, desFileSize: int = 200, filename: str = None):
>>>>>>> master
        """
        压缩图片到200kb
        :param picpath: 必传 路径地址
        :param desFileSize: 默认200kb
        :param filename: 可选
        :return:
        """

        img = Image.open(picpath)  # 返回一个Image对象
        # os模块中的path目录下的getSize()方法获取文件大小，单位字节Byte
        size = os.path.getsize(picpath) / 1024  # 计算图片大小即KB
        # size的两个参数
        width, height = img.size[0], img.size[1]
        # if size > 600:
        #     img.save(picpath, quality=8)
        #     size = os.path.getsize(picpath) / 1024
        # 压缩宽高 不牺牲画质,每次压缩会被不断覆盖
        while size > desFileSize:
            width, height = round(width * 0.9), round(height * 0.9)
            print(width, height)
            img = img.resize((width, height), Image.ANTIALIAS)
            img.save(picpath)
            size = os.path.getsize(picpath) / 1024
        # 压缩完成 quality 是设置压缩比 保持宽高 牺牲画质
        # img.save(picpath, quality=5)
        img.save(picpath)
        img.close()
<<<<<<< HEAD



=======
>>>>>>> master
