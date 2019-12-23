from datetime import datetime as date
from statistics import median
from typing import Optional
import argparse

from api import get_friends, get_ids, get_name
from api_models import User
from bcolors import bcolors


def age_predict(user_id: str) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """

    json = get_friends(user_id, 'bdate')

    name = get_name(user_id)

    # Exit user profile is not avalible
    if 'error' in json:
        print(f"{bcolors.FAIL}{name}'s profile is private{bcolors.ENDC}")
        # Exit
        raise SystemExit(0)

    curr_date = date.now()

    deltas = []
    # Cycle through user friends
    for friend in json:

        try:
            birthday = friend['bdate']
            birthday_date = date.strptime(birthday, '%d.%m.%Y')
            delta = curr_date - birthday_date
            deltas.append(delta.days / 365)

        except:
            pass
    try:
        # Calculate average age across user friend
        age_avg = round(median(deltas), 1)
        print(f"{bcolors.OKGREEN}I predict {bcolors.OKBLUE}{name}'s{bcolors.OKGREEN} age as {bcolors.ENDC}{age_avg}")
        return age_avg
    except:
        print(
            f"{bcolors.FAIL}{name} does not have friends with accessible birthday{bcolors.ENDC}")
        return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=str, help="VK user id or screen name")

    args = parser.parse_args()

    id = get_ids(args.id.split())[0]
    age_predict(id)
