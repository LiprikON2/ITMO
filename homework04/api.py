import requests
import time
from datetime import datetime as date
from typing import List, Optional, Tuple, Dict

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
        

def get_friends(user_id: int, fields = '') -> List[dict]:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    
    query = f"{config.VK_CONFIG['domain']}/friends.get?access_token={config.VK_CONFIG['access_token']}&user_id={user_id}&fields={fields}&v={config.VK_CONFIG['version']}"
    
    json = get(query).json()
    
    # When user profile is private json doesn't have 'response' field
    if 'error' in json:
        return json
    return json['response']['items']


def get_user(ids: List[any], fields='') -> Dict:
    """ Retrives user info from id """
    
    # Convert list to comma separated string
    user_ids = ','.join(str(id) for id in ids)
    
    query = f"{config.VK_CONFIG['domain']}/users.get?access_token={config.VK_CONFIG['access_token']}&user_ids={user_ids}&fields={fields}&v={config.VK_CONFIG['version']}"
    json = get(query).json()
    # When user profile doesn't exist json doesn't have 'response' field
    if 'error' in json:
        print(f"{bcolors.FAIL}The user doesn't seem to exist{bcolors.ENDC}")
        return json
    
    return json['response']


def get_name(id: int) -> str:
    """ Retrives user name from id """
    
    # Get user info
    user_info = get_user([id])[0]
    # Retrive user name from user info
    user_name = user_info['first_name'] + ' ' + user_info['last_name']
    
    return user_name


def get_ids(screen_names: List[str]) -> List[int]:
    """ Converts screen names to ids """
    
    # Check if community id is passed
    for screen_name in screen_names:
        
        if str(screen_name)[0] == '-':
            return screen_names

    users = get_user(screen_names)
    try:
        ids = [user['id'] for user in users]
    except:
        print(f"{bcolors.FAIL}Some of users doesn't seem to exist{bcolors.ENDC}")
        
    # Exit if all provided screen names are invalid
    if not 'ids' in locals():
        # Exit program
        raise SystemExit(0)
    return ids

if __name__ == "__main__":
    pass
    
    