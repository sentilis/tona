from pydantic import BaseModel
from pydantic.utils import GetterDict
from typing import Any, Optional
import peewee

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class PydanticBaseModel(BaseModel):

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class PydanticHTTPResponseModel(BaseModel):
    message: Optional[str] = None
    payload: Optional[Any] = None
    meta: Optional[Any] = None