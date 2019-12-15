import requests
import time
from datetime import datetime as date

import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    call_count = 0
    delay = 1

    while call_count < max_retries:
        response = requests.get(url, params)
        if response.ok:
            break
        # error happened, pause between requests
        time.sleep(delay)

        # calculate next delay
        delay = min(timeout * backoff_factor, timeout)
        call_count += 1
        
    print('max_retries:', max_retries, 'call_count:', call_count, 'backoff_factor:', backoff_factor)
    return response
        
        


def get_friends(user_id, fields = 'bdate', vk_command = 'friends.get'):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    
    query = f"{config.VK_CONFIG['domain']}/{vk_command}?access_token={config.VK_CONFIG['access_token']}&user_id={user_id}&fields={fields}&v={config.VK_CONFIG['version']}"
    json = get(query).json()
    
    if 'error' in json:
        print('error occured =(')
    
    # print(json)
    # json = get('https://httpbin.org/error', max_retries=3, backoff_factor=0)
    return json


def get_user(user_ids, fields=''):
    query = f"{config.VK_CONFIG['domain']}/users.get?access_token={config.VK_CONFIG['access_token']}&user_ids={user_ids}&fields={fields}&v={config.VK_CONFIG['version']}"
    json = get(query).json()
    
    if 'error' in json:
        print('error occured =(')
    return json
    

def get_mutual(source_uid, target_uid):
    query = f"{config.VK_CONFIG['domain']}/friends.getMutual?access_token={config.VK_CONFIG['access_token']}&source_uid={source_uid}&target_uid={target_uid}&v={config.VK_CONFIG['version']}"
    json = get(query).json()
    
    if 'error' in json:
        print('error occured =(')
    return json

def get_group(group_ids):
    
    query = f"{config.VK_CONFIG['domain']}/groups.getById?access_token={config.VK_CONFIG['access_token']}&group_ids={group_ids}&v={config.VK_CONFIG['version']}"
    json = get(query).json()
    
    if 'error' in json:
        print('error occured =(')
    return json
    


def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE


if __name__ == "__main__":
    # get_friends(74171270, 'bdate')
    pass