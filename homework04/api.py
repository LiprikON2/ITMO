import requests
import time
from datetime import datetime as date

from bcolors import bcolors
import config

# backoff_factor=0.3
def get(url, params={}, timeout=5, max_retries=5, backoff_factor=1.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    call_count = 0
    delay = 0
    
    while call_count <= max_retries - 1:
        try:
            response = requests.get(url, params)
        except requests.RequestException:
            if call_count == max_retries - 1:
                raise
            response = None
            
        # if response.ok and not response.json().get('error'):
        if response:
            if response.ok:
                break
    
        # calculate next delay
        delay = min(backoff_factor * (2 ** call_count), timeout)
        
        # error happened, pause between requests
        print(f'{bcolors.WARNING}No response, delaying: {delay}{bcolors.ENDC}')
        time.sleep(delay)
        
        call_count += 1
        
    return response
        

def get_friends(user_id: str, fields = ''):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    
    query = f"{config.VK_CONFIG['domain']}/friends.get?access_token={config.VK_CONFIG['access_token']}&user_id={user_id}&fields={fields}&v={config.VK_CONFIG['version']}"
    
    json = get(query).json()
        
    return json


def get_user(ids: list, fields=''):
    user_ids = ','.join(ids)
    
    query = f"{config.VK_CONFIG['domain']}/users.get?access_token={config.VK_CONFIG['access_token']}&user_ids={user_ids}&fields={fields}&v={config.VK_CONFIG['version']}"
    json = get(query).json()
    
    return json

def get_name(id: str) -> str:
    """ Retrives name from id """
    
    # Get user info
    user_info = get_user([id])['response'][0]
    # Retrive user name from user info
    user_name = user_info['first_name'] + ' ' + user_info['last_name']
    
    return user_name


def get_ids(screen_names: list) -> list:
    users = get_user(screen_names)
    try:
        ids = [user['id'] for user in users['response']]
    except:
        print(f"{bcolors.FAIL}Some of users doesn't seem to exist{bcolors.ENDC}")
        
    # Exit if all provided screen names are invalid
    if not 'ids' in locals():
        raise SystemExit(0)
    return ids


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
    
    