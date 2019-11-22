import requests
import telebot
from bs4 import BeautifulSoup
import datetime

import config


# telebot.apihelper.proxy = {'https':'54.37.131.161:3128'} # main proxy
telebot.apihelper.proxy = {'https':'194.226.34.132:5555'} # secondary
# telebot.apihelper.proxy = {'https':'31.186.102.162:3128'}
# telebot.apihelper.proxy = {'https':'95.47.183.23:3128'}
# telebot.apihelper.proxy = {'https':'217.113.122.142:3128'}
# telebot.apihelper.proxy = {'https':'95.128.246.35:3128'}
bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    print(url)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})
    
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def get_day(weekday = None):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    week = datetime.date.today().isocalendar()[1]
    if not weekday:
        weekday = datetime.datetime.today().weekday()
        weekday_id = str(weekday + 1) + 'day'
        
    elif weekday == '/monday':
        weekday_id = '1day'
    elif weekday == '/tuesday':
        weekday_id = '2day'
    elif weekday == '/wednesday':
        weekday_id = '3day'
    elif weekday == '/thursday':
        weekday_id = '4day'
    elif weekday == '/friday':
        weekday_id = '5day'
    elif weekday == '/saturday':
        weekday_id = '6day'
    elif weekday == '/sunday':
       weekday_id = '7day'
       
    elif weekday == '/tommorow':
        weekday = datetime.datetime.today().weekday()
        weekday_id = str((weekday + 2) % 7) + 'day'
       
    parity = week % 2 + 1
    
    
    return {'hour': hour, 'minute': minute, 'week': week, 'parity': parity, 'weekday_id': weekday_id}
    # return {'hour': hour, 'minute': minute, 'week': week, 'weekday': weekday}

def day_off(message):
    resp = '🎉 Looks like day is day off! 🎉'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    

    
    
# MY CODE
def parse_schedule(web_page, day, message):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day['weekday_id']})
    if schedule_table:
    
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        return times_list, locations_list, lessons_list
    else:
        day_off(message)

@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    print('gettting monday')
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    
    # Prevent crash when no group is passed
    try:
        weekday, group = message.text.split()
    except ValueError:
        return
    day = get_day(weekday)
    
    web_page = get_page(group)
    # Prevent crash when no schedule is available
    try:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day, message)
    except TypeError:
        return
    
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
        


# So far its only gets today's schedule
@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    day = get_day()
    
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day, message)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')







@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # Prevent crash when no group is passed
    try:
        _, group = message.text.split()
    except ValueError:
        return
    day = get_day('tommorow')
    
    web_page = get_page(group)
    # Prevent crash when no schedule is available
    try:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day, message)
    except TypeError:
        return
    
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    # print(get_day())
    bot.polling(none_stop=True)

