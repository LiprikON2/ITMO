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
        return


def get_day(weekday = None):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    # Get serial number of a week
    week = datetime.date.today().isocalendar()[1]
    
    # If weekday is not specified, get today's week_id
    if not weekday:
        weekday = datetime.datetime.today().weekday()
        weekday_id = str(weekday + 1) + 'day'
        
    elif weekday in '/monday':
        weekday_id = '1day'
    elif weekday in '/tuesday':
        weekday_id = '2day'
    elif weekday in '/wednesday':
        weekday_id = '3day'
    elif weekday in '/thursday':
        weekday_id = '4day'
    elif weekday in '/friday':
        weekday_id = '5day'
    elif weekday in '/saturday':
        weekday_id = '6day'
    elif weekday in '/sunday':
       weekday_id = '7day'
    
    elif weekday in '/tomorrow':
        weekday_num = datetime.datetime.today().weekday()
        weekday_id = str((weekday_num + 2) % 7) + 'day'
        # check if week cycles from Sunday to Monday
        if weekday_num + 2 > 7:
            week += 1
    else: 
        print(weekday)
    
    parity = week % 2
    
    
    return {'hour': hour, 'minute': minute, 'week': week, 'parity': parity, 'weekday_id': weekday_id}
    # return {'hour': hour, 'minute': minute, 'week': week, 'weekday': weekday}


def day_off(message):
    resp = '🎉 Looks like the day is day off! 🎉'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    

@bot.message_handler(commands=['tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    
    # Prevent crash when no group is passed
    try:
        weekday, group = message.text.split()
    except ValueError:
        return
    day = get_day(weekday)
    
    web_page = get_page(group, day['parity'])
    # Prevent crash when no schedule is available
    try:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day, message)
    except TypeError:
        day_off(message)
        return
    
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
        


# So far its only gets today's schedule
@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    weekdays = ('1day', '2day', '3day', '4day', '5day', '6day', '7day')
    today = get_day()
    # friday = 4 (5day)
    index = weekdays.index(today['weekday_id'])
    
    # Prevent crash when no group or no week number is passed
    try:
        _, group = message.text.split()
    except ValueError:
        return
    day_offset = 0
    
    while day_offset < 15:
        
        day = get_day(weekdays[index + day_offset])
        web_page = get_page(group)
        # Prevent crash when no schedule is available
        try:
            times_lst, locations_lst, lessons_lst = \
                parse_schedule(web_page, day, message)
        except TypeError:
            day_offset += 1
        else:
            break
        
    else:
        resp = 'Looks like there is no classes in the next 15 days O_o'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return
    
    resp = ''
    # for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
    
    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    
    # Prevent crash when no group or no week number is passed
    try:
        weekday, parity, group = message.text.split()
    except ValueError:
        return
    
    resp = ''
    for weekday in weekdays:
        resp += '\n\n------------------------- <b>{}</b> -------------------------\n\n'.format(weekday.upper())
        day = get_day(weekday)
        web_page = get_page(group, parity)
        # Prevent crash when no schedule is available
        try:
            times_lst, locations_lst, lessons_lst = \
                parse_schedule(web_page, day, message)
        except TypeError:
            resp += '                          🎉 Day off 🎉'
            continue
        
        
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)

