from typing import List, Optional
from pydantic import BaseModel

import pandas as pd
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

import config

class BaseUser(BaseModel):
    """ Модель пользователя с базовыми полями """
    id: int
    first_name: str
    last_name: str
    online: int
    deactivated: Optional[str]


class User(BaseUser):
    """ Модель пользователя с необязательным полем дата рождения """
    bdate: Optional[str]


class Message(BaseModel):
    """ Модель сообщения """
    
    def get_wall(
        owner_id: str='',
        domain: str='',
        offset: int=0,
        count: int=10,
        filter: str='owner',
        extended: int=0,
        fields: str='',
        v: str='5.103'
    ) -> pd.DataFrame:
        """
        Возвращает список записей со стены пользователя или сообщества.

        @see: https://vk.com/dev/wall.get 

        :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
        :param domain: Короткий адрес пользователя или сообщества.
        :param offset: Смещение, необходимое для выборки определенного подмножества записей.
        :param count: Количество записей, которое необходимо получить (0 - все записи).
        :param filter: Определяет, какие типы записей на стене необходимо получить.
        :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
        :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
        :param v: Версия API.
        """
        
        query = f"{config.VK_CONFIG['domain']}/wall.get?access_token={config.VK_CONFIG['access_token']}&owner_id={owner_id}&offset={offset}&count={count}&filter={filter}&extended={extended}&fields={fields}&v={v}"
        json = get(query).json()
        
        return json


if __name__ == "__main__":
    # get_friends(74171270, 'bdate')
    s = get_wall(owner_id=-86529522)
    print(s)
    pass
    
