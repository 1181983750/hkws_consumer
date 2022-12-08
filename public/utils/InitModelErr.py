from django.db.models import Model

class InitModelErr(Exception):
    def __init__(self, model: Model, *args):
        self.__msg = '{} 模型初始化创建失败'.format(model)
        self.__msg += str(args)

    def __str__(self):
        return self.__msg