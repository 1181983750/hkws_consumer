# Creation time: 2022/6/7 10:02
# The author: Tiger_YC

from django.db import models

from public.utils.UploadRestricted import RestrictedFileField


class ImageFileds(models.Model):
    # imgs = models.ImageField()
    image = RestrictedFileField(upload_to='images/', max_length=100, content_types=['image/jpeg', 'image/gif', 'image/bmp', 'image/tiff', 'image/jpg', 'image/png'], max_upload_size=5242880, null=True, )
