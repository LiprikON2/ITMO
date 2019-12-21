import pymorphy2
import gensim
import pyLDAvis
import requests

import pandas as pd
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

from api import get, get_ids
import config

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
    # Convert screen name to id
    if owner_id != '':
        owner_id = get_ids([owner_id])[0]
    
    
    query = f"{config.VK_CONFIG['domain']}/wall.get?access_token={config.VK_CONFIG['access_token']}&owner_id={owner_id}&offset={offset}&count={count}&filter={filter}&extended={extended}&fields={fields}&v={v}"
    # json = get(query).json()
    
    code = f"""
        return API.wall.get({{
        "owner_id": '{owner_id}',
        "domain": '{domain}',
        "offset": '{offset}',
        "count": '{count}',
        "filter": '{filter}',
        "extended": '{extended}',
        "fields": '{fields}',
        "v": '{v}'
    }});
    """

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG['access_token'],
                "v": "5.103"
            }
    )
    print(response.json())
    return pd.DataFrame(response.json()['response']['items'])


if __name__ == "__main__":
    # get_friends(74171270, 'bdate')
    # s = get_wall(owner_id=-86529522)
    # print(s)
    pass

    morph = pymorphy2.MorphAnalyzer()

    # wall = get_wall(domain='leftradicalmuslesplatinum')
    # new_wall = get_wall(domain='typical_olimp')
    # wall = wall.append(new_wall, ignore_index=True)
    # new_wall = get_wall(domain='opyatmetel')
    # wall = wall.append(new_wall, ignore_index=True)

    wall = get_wall(owner_id='noize_mc', domain='noizemc')
    # wall = get_wall(owner_id='danilkaaaaaaaaaaaaaaaaaa', domain='animationdroping')
    