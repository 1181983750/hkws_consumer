import datetime
import threading
import traceback
from typing import Type, Any, Dict, Union, List, TypeVar

from django.db import models
from django.db.models import QuerySet, Model
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute
from django.db.models.query_utils import DeferredAttribute
from rest_framework.serializers import ModelSerializer

from public.utils.response_result import ResponseResult


T = TypeVar('T')

# 自定义 __str__方法
class BaseModel:

    def __str__(self):
        repr_str = 'Object: {}:〔'.format(self.__class__.__name__)
        index = 0
        for k, v in self.__dict__.items():
            index += 1
            if index < len(self.__dict__.items()):
                repr_str += '{}={}, '.format(k, v)
            else:
                repr_str += '{}={}'.format(k, v)
        return repr_str + '〕'

    __repr__ = __str__


class BaseORM:
    """
    数据库模型增、删、改、查基类
    """

    def __init__(self, model: Type[models.Model]):
        self.model = model

    def add(self, add_data: Union[models.Model, Dict]) -> models.Model:
        """
        新增数据

        Args:
            add_data: 新增数据对象

        Returns:
            新增到数据库中的orm数据对象
        """
        if isinstance(add_data, models.Model):
            add_data.save()
            return add_data
        if isinstance(add_data, Dict):
            return self.model.objects.create(**add_data)
        raise Exception('添加数据的类型错误')

    def delete_by_id(self, ids: Union[str, int]) -> int:
        """
        根据id删除数据

        Args:
            ids: Union[str, int] 数据id

        Returns:
            删除数据数
        """
        return self.model.objects.filter(id=ids).delete()[0]

    def update_data_by_id(self, ids: Union[str, int], update_data: Union[Dict, models.Model]) -> models.Model:
        """
        根据id更新数据

        Args:
            ids: Union[str, int] 数据id
            update_data: Union[Dict, models.Model] 更新数据对象

        Returns:
            更新到数据库中orm数据对象
        """
        if isinstance(update_data, Dict):
            result = self.model.objects.filter(id=ids)
            result.update(**update_data)
            return result[0]
        elif isinstance(update_data, models.Model):
            update_data.save()
            return update_data
        raise Exception('更新数据的类型错误')

    def get_data_by_id(self, ids: Union[str, int]) -> models.Model:
        """
        根据id查询指定数据

        Args:
            ids: id

        Returns:

        """
        return self.model.objects.get(id=ids)

    def get_all(self) -> QuerySet[models.Model]:
        """
        查询所有数据

        Returns:

        """
        return self.model.objects.all()

    def batch_add(self, add_data_list: List[models.Model]):
        """
        批量添加

        Args:
            add_data_list: 批量添加的数据

        Returns:

        """
        return self.model.objects.bulk_create(add_data_list)

    def batch_update(self, update_data_list: List[models.Model], update_key_list: List):
        """
        批量更新数据

        Args:
            update_key_list: 批量更新的列名
            update_data_list: 批量更新的数据

        Returns:

        """
        return self.model.objects.bulk_update(update_data_list, fields=update_key_list)


# noinspection PyBroadException
class BaseService:
    """
    所有业务逻辑类基类, 包括单一数据的曾、删、改、查，查询所有数据 和 批量数据的新增、修改
    """

    def __init__(self, model: Type[models.Model]):
        self.orm = BaseORM(model)

    def add(self,
            add_data: Union[Dict, models.Model],
            serializer: Type[ModelSerializer] = None,
            get_model_obj: bool = False) -> Union[Dict, models.Model]:
        """
        新增数据

        Args:
            get_model_obj: bool 是否获取数据model对象，若为True则函数直接返回添加后的数据库model数据对象
            serializer: Type[ModelSerializer]  序列化器
            add_data:Union[Dict, models.Model]  新增数据对象

        Returns:

        """
        try:
            result = self.orm.add(add_data=add_data)
        except Exception:
            traceback.print_exc()
            return ResponseResult(msg='添加数据失败失败数据:{}'.format(add_data), code=0)()

        if get_model_obj:
            return result

        if not result:
            result = self.manually_serialize(data=add_data, serializer=serializer)
        else:
            result = self.manually_serialize(data=result, serializer=serializer)
        # if not serializer:
        #     result = result.__dict__
        #     del result['_state']
        # else:
        #     if not result:
        #         result = serializer(instance=add_data)
        #     result = serializer(instance=result).data
        return ResponseResult(msg='添加成功', code=1, data=result)()

    def delete_by_id(self, ids: Union[str, int]) -> Dict:
        """
        根据id删除数据

        Args:
            ids: Union[str, int] 数据id

        Returns:

        """

        try:
            result = self.orm.delete_by_id(ids=ids)
        except Exception:
            traceback.print_exc()
            return ResponseResult(msg='删除数据失败', code=0)()

        return ResponseResult(msg='成功删除{}条数据'.format(result), code=1)()

    def update_data(self, update_data_dict: Union[Dict, models.Model],
                    ids: Union[str, int] = 0,
                    serializer: Type[ModelSerializer] = None,
                    get_model_obj: bool = False) -> Union[Dict, models.Model]:
        """
        根据id或已经查询到的数据orm对象更新数据，当更具id查询时update_data类型为dict,当更具已经查询到的数据orm对象更新时id可以不传

        Args:
            get_model_obj: bool 是否获取数据model对象，若为True则函数直接返回跟新后的数据库model数据对象
            serializer: Type[ModelSerializer] 序列化器
            ids: Union[str, int] 数据id
            update_data: Union[Dict, models.Model] 更新数据对象

        Returns:
            更新后的数据
        """
        try:
            result = self.orm.update_data_by_id(ids=ids, update_data=update_data_dict)
        except Exception:
            traceback.print_exc()
            return ResponseResult(msg='更新数据失败', code=0)()

        if get_model_obj:
            return result

        result = self.manually_serialize(data=result, serializer=serializer)
        # if serializer:
        #     result = serializer(instance=result).data
        # else:
        #     result = result.__dict__
        #     del result['_state']
        return ResponseResult(msg='数据更新成功', code=1, data=result)()

    def get_data_by_id(self, ids: Union[str, int], serializer: Type[ModelSerializer] = None,
                       get_model_obj: bool = False) -> Union[Dict, models.Model]:
        """
        根据id查询指定数据

        Args:
            get_model_obj: bool 是否获取数据model对象，若为True则函数直接返回查询到的model数据对象
            serializer: Type[ModelSerializer] 序列化器
            ids: Union[str, int] 数据id

        Returns:

        """
        try:
            result = self.orm.get_data_by_id(ids=ids)
        except self.orm.model.DoesNotExist:
            return ResponseResult(msg='查询失败，没有id为[{}]的数据'.format(ids), code=0)()

        if get_model_obj:
            return result

        result = self.manually_serialize(data=result, serializer=serializer)
        # if not serializer:
        #     result = result.__dict__
        #     del result['_state']
        # else:
        #     result = serializer(instance=result).data
        return ResponseResult(msg='查询成功', code=1, data=result)()

    def get_all(self, serializer: Type[ModelSerializer] = None,
                get_model_obj: bool = False) -> Union[Dict, List[models.Model]]:
        """
        获取所有

        Args:
            get_model_obj: bool 是否获取数据model对象，若为True则函数直接返回查询到的model数据列表对象
            serializer: Type[ModelSerializer] 序列化器

        Returns:

        """
        try:
            result = self.orm.get_all()
        except Exception:
            traceback.print_exc()
            return ResponseResult(msg='查询失败', code=0)()

        if get_model_obj:
            result_list = []
            for i in result:
                result_list.append(i)
            return result_list

        result = self.manually_serialize(data=result, serializer=serializer)
        # if not serializer:
        #     result_list = []
        #     for i in result:
        #         i = i.__dict__
        #         del i.__dict__['_state']
        #         result_list.append(i)
        #     return ResponseResult(msg='查询成功', code=1, data=result_list)()
        # result = serializer(instance=result, many=True).data
        return ResponseResult(msg='查询成功', code=1, data=result)()

    def batch_add(self,
                  add_data_list: List[models.Model],
                  serializer: Type[ModelSerializer] = None,
                  get_model_obj: bool = False) -> Union[List[models.Model], Dict]:
        """
        批量添加数据

        Args:
            add_data_list: List[models.Model] 批量添加数据，只能是模型类型不能和单条添加时一样的字段类型
            serializer: Type[ModelSerializer] 序列化器
            get_model_obj: bool 是否获取数据model对象，若为True则函数直接返回查询到的model数据列表对象

        Returns:
            数据字典列表或model数据列表
        """
        try:
            result = self.orm.batch_add(add_data_list=add_data_list)
        except Exception:
            return ResponseResult(msg='批量添加失败', code=0)()

        if get_model_obj:
            return result

        result = self.manually_serialize(data=result, serializer=serializer)

        # if not serializer:
        #     result_list = []
        #     for i in result:
        #         i = i.__dict__
        #         del i['_state']
        #         result_list.append(i)
        #     return ResponseResult(msg='批量添加成功', code=1, data=result_list)()
        # result = serializer(instance=result, many=True).data
        return ResponseResult('批量添加成功', code=1, data=result)()

    def batch_update(self,
                     update_data_list: List[models.Model],
                     update_key_list: List,
                     serializer: Type[ModelSerializer] = None,
                     get_model_obj: bool = False) -> Union[List[models.Model], Dict]:
        """
        批量更新数据

        Args:
            update_data_list: List[models.Model] 更新数据的model列表
            update_key_list: List 更新字段列表
            serializer: Type[ModelSerializer] 序列化器
            get_model_obj: 是否获取model对象

        Returns:

        """

        try:
            result = self.orm.batch_update(update_data_list=update_data_list, update_key_list=update_key_list)
        except Exception:
            traceback.print_exc()
            return ResponseResult(msg='批量更新失败', code=0)()

        if get_model_obj:
            return result

        return_result = self.manually_serialize(data=update_data_list, serializer=serializer)
        # if not serializer:
        #     result_list = []
        #     for i in result:
        #         i = i.__dict__
        #         del i['_state']
        #         result_list.append(i)
        #     return ResponseResult(msg='批量更新条数据成功', code=1, data=result_list)()
        # result = serializer(instance=result, many=True).data
        return ResponseResult(msg='批量更新{}条数据成功'.format(result), code=1, data=return_result)()


    def manually_serialize(self, data: Union[List[models.Model], QuerySet[models.Model], models.Model],
                           serializer: Type[ModelSerializer]):
        """
        如果有序列化器则用序列化器序列化数据，如果没有序列化器则手动序列化数据

        Args:
            data: Union[List[models.Model], QuerySet[models.Model], models.Model] 查询出来的数据
            serializer: Type[ModelSerializer] 序列化器

        Returns:
            result: List or Dict
        """
        if serializer:
            if isinstance(data, List):
                result = serializer(instance=data, many=True).data
                return result
            if isinstance(data, QuerySet):
                if len(data) > 1:
                    result = serializer(instance=data, many=True).data
                    return result
                result = serializer(instance=data).data
                return result
            if data:
                result = serializer(instance=data).data
                return result

        if isinstance(data, List) or isinstance(data, QuerySet):
            if len(data) > 1:
                result = []
                for i in data:
                    i = i.__dict__
                    del i['_state']
                    result.append(i)
                return result
            if data:
                result = data[0].__dict__
                del result['_state']
                return result

        if data:
            result = data.__dict__
            del result['_state']
            return result




class DictToModel:
    """
    字典转换为model类


    示例：

        d_dict = {...}

        dtm = DictToModel(dict_data=d_dict, model_class=Message)

        mode: Message = dtm.format_dict_data_to_model(get_model_obj=True)

        mode.save()

        dic: Dict = dtm.format_dict_data_to_model()

        m = Message(**dic)

    """

    def __init__(self, dict_data: Dict, model_class: Type[Model]):
        self.__dict_data = dict_data
        self.__model_class = model_class

    def format_dict_data_to_model(self, get_model_obj: bool = False) -> T:
        """
        格式化字典数据为model实例或者model可接收类型字典

        Args:
            get_model_obj (): 是否获取model实体 默认False返回model可接收字典， 为True返回model实体

        Returns:
            model实体或model可接收字典   也就是填补没有传进来的所有字段
        """
        result = {}

        dict_data = self.__format_dict_data(data_dict=self.__dict_data) #扁平化字典
        model_dict = self.__get_model_dict()
        for k, v in model_dict.items():
            if isinstance(v, models.ForeignKey):
                if v.null:
                    result[k] = dict_data.get(k) if dict_data.get(k) else None
                else:
                    result[k] = dict_data.get(k, 0)  #上下同理  js:写法 k||0
            elif isinstance(v, models.SmallIntegerField) or isinstance(v, models.IntegerField):
                if v.null:
                    result[k] = dict_data.get(k, None)
                else:
                    result[k] = dict_data.get(k, v.default)
            elif isinstance(v, models.CharField) or isinstance(v, models.TextField):
                if v.null:
                    result[k] = dict_data.get(k, None)
                else:
                    result[k] = dict_data.get(k, v.default)
            elif isinstance(v, models.DateTimeField):
                if v.null:
                    result[k] = dict_data.get(k, None)
                else:
                    result[k] = dict_data.get(k, datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
            elif isinstance(v, models.DecimalField):
                if v.null:
                    result[k] = dict_data.get(k, None)
                else:
                    result[k] = dict_data.get(k, 0)
            elif isinstance(v, models.BooleanField):
                if v.null:
                    result[k] = dict_data.get(k, None)
                else:
                    result[k] = dict_data.get(k, None)
        if get_model_obj:
            return self.__model_class(**result)  #如果要模型对象 就通过上面填补完的字典拆包转模型 model()
        else:
            return result    #不要的话就返回表模型里所有字段字典 方便更改

    def __format_dict_data(self, data_dict: Dict) -> Dict:
        """
        将外部给的字典进行扁平化，将所有字典中的数据放入同一层

        Args:
            data_dict (): 前端给到后端的字典数据

        Returns:

        """
        result = {}
        for k, v in data_dict.items():
            if isinstance(v, Dict):
                recursion_dict = self.__format_dict_data(data_dict=v)
                result.update(recursion_dict)
            else:
                result[k] = v
        return result

    def __get_model_dict(self):
        """
        获取model中的所有字段属性并存入字典中用于后续判断字段类型以及从获取前端传来的字典的数据

        Returns:
        字段名：字段类型
        """
        result = {}
        for k, v in self.__model_class.__dict__.items():
            if k in result or k == 'id':
                continue
            if isinstance(v, DeferredAttribute) or isinstance(v, ForeignKeyDeferredAttribute):
                result[k] = v.field #将整个字段对象存入字典value
        return result

# if __name__ == '__main__':
#     import os
#     import django
#
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Channels.settings')
#     django.setup()
#     from Message.models import Message
#
# d_dict = {
#     "data": {
#         "data": {
#             "client_msg_id": 15,
#             "date": 1652691598,
#             "duration": 0,
#             "file_height": 0,
#             "file_size": 0,
#             "file_width": 0,
#             "local_url": "",
#             "message_id": 0,
#             "msg_type": "txt",
#             "remote_url": "",
#             "room_id": "",
#             "send": 1,
#             "thumbnail": "",
#             "to": 3,
#             "txt": "哦哦哦哦哦"
#         },
#         "group_id": 0,
#         "send": {
#             "avatar": '''https://img2.baidu.com/it/u=2032522698,
#             1357816476&fm=253&fmt=auto&app=138&f=JPEG?w=400&h=400''',
#             "id": 1,
#             "identity": "",
#             "isSelect": False,
#             "isTop": False,
#             "phone": "",
#             "socket_id": "",
#             "userName": "散打哥"
#         },
#         "to": 3
#     },
#     "tip": 1
# }
#
#     m = Message()
#     dtm = DictToModel(dict_data=d_dict, model_class=Message)
#     # md: Message = dtm.format_dict_data_to_model(get_model_obj=True)
#     md: Dict = dtm.format_dict_data_to_model()
#     print(md)
