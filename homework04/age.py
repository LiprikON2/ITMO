from datetime import datetime as date
from statistics import median
from typing import Optional



from api import get_friends
from api_models import User



def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    
    json = get_friends(user_id, 'bdate')
    curr_date = date.now()
    
    deltas = []
    for i in range(len(json['response']['items'])):
        
        try:
            birthday = json['response']['items'][i]['bdate']
            birthday_date = date.strptime(birthday, '%d.%m.%Y')
            delta = curr_date - birthday_date
            deltas.append(delta.days / 365)
            
        except:
            pass
    try:
        age_avg = round(median(deltas), 1)
        return age_avg
    except:
        return 'Не получилось! :('
        
    


if __name__ == "__main__":
    age = age_predict(74171270)
    # age = age_predict(1)
    print(age)
