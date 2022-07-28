from typing import Union, Dict, List



class ResponseResult:

    def __init__(self, msg: str = '', data: Union[Dict, List] = None, code: int = -1, **kwarg):
        self.__result = {'message': msg, 'data': data, 'code': code}
        self.__result.update(kwarg)

    def __call__(self, *args, **kwargs) -> Dict:
        return self.__result




