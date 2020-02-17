import re
from collections import deque

import requests

from bot.weekdays import WeekInfo, DayInfo, HourInfo, Weekdays


class MapsLocation:
    def __init__(self, url: str, full_name: str, weekdays_open: list):
        self.url = url
        self.full_name = full_name
        self.weekdays_open = weekdays_open


locations = {
    'fitx-adenauer': MapsLocation('https://www.google.de/maps/place/FitX+Fitnessstudio/@51.5495502,7.0786878,' \
                                  '17z/data=!3m1!4b1!4m5!3m4!1s0x47b8e7053e64b21b:0xaf67314083f991e8!8m2!3d51.5495502'
                                  '!4d7.0808765 '
                                  '?hl=de', 'FitX Gelsenkirchen-Erle', weekdays_open=Weekdays),
    'fitx-asbeck': MapsLocation('https://www.google.de/maps/place/FitX+Fitnessstudio/@51.523014,7.0663099,' \
                                '15.5z/data=!4m5!3m4!1s0x47b8e645c7f82f75:0x4338a1e7f7deee66!8m2!3d51.5237398!4d7'
                                '.071133?hl=de'
                                '&authuser=0', 'FitX Gelsenkirchen-Heßler', weekdays_open=Weekdays),
    'sgz-buer': MapsLocation(
        'https://www.google.de/maps/place/Sport-+und+Gesundheitszentrum+Buer/@51.5800968,7.0451868,'
        '14z/data=!4m5!3m4!1s0x0:0xd1508f85ba1da6b5!8m2!3d51.5830 099!4d7.0427299?hl=de',
        'Sport- & Gesundheitszentrum Buer', weekdays_open=Weekdays),

    'sushi-gladbeck': MapsLocation('https://www.google.com/maps/place/Do+Sushi/@51.5733989,6.9889221,'
                                   '15z/data=!4m5!3m4!1s0x0:0xccd9225ca5e829ca!8m2!3d51.5733989!4d6.9889221',
                                   "Do Sushi Gladbeck", weekdays_open=Weekdays[1:7])
}


def extract_raw_week(location) -> str:
    # get raw html from google maps
    url: str = locations[location].url
    ret: str = requests.get(url, {}).text

    # pre-format a string containing only the necessary information
    ret = re.sub(r'\\n|\\\"', '', ret)
    ret = re.findall(r'\[\[\d,\[\[\d,\d,,,.+\]\],\d\]\]', ret)[0]

    # write html to text file for testing purposes
    with open('maps_data.txt', 'r+', encoding='utf-8') as file:
        file.seek(0)
        file.write(ret)
        file.truncate()

    return ret


def extract_raw_week_to_week_obj(raw_week) -> WeekInfo:
    """
    Takes a html-extracted representation of a week returns a WeekInfo object built from this data.
    This raw data is received as a nested array form:
        [[hour, hour, hour,...,hour],[...],...[]]
    whereas each hour is an array with up to 5 entries representing different information about each hour:
        hour = [17,22,Normalerweise nicht zu stark besucht,,17 Uhr]

    If a location is closed at certain days, these days have a form of: [1,null,1]

    Not all hours must necessarily be represented. From observation, closing hours may be simply skipped.
    """

    week = WeekInfo()

    # step 1 - parse string

    # regex for onto match a day: [1,[[ ... ]],0] OR [1,null,1]
    tokenized_days: list = re.findall(r'\[\d,\[\[.+?\]\],\d\]|\[\d,null,\d\]', raw_week)


    for day in tokenized_days:
        day = day[1:len(day)-1] # removed outer brackets TODO: write function for this operation
        day_index = int(re.search(r'\d', day)[0]) - 1  # first entry is the actual weekday as an int
        tokenized_hours: list = re.findall(r'\[\d.+?\]', day)

        for hour in tokenized_hours:
            hour = day[1:len(day)-1]

    # extract hours
    hours_extracted = []
    for hour in hours_deque:
        # turn unformatted string into usable information
        hour_extracted = re.findall(r'[\w\s]+', hour)

        # extracted data now in the current form: [time, crowded, ...]
        time, crowded = [hour_extracted[i] for i in (0, 1)]
        hours_extracted.append(HourInfo(int(time), crowded))

    # add hours to weekdays and put in weekday object
    # week = WeekInfo()
    for day_index in range(7):
        day = DayInfo(day_index)
        for hour_index in range(24):
            day.add_hour(hours_extracted[day_index * 24 + hour_index])
        week.add_day(day)

    return week


def extract_current_hour(maps_html):
    pattern = r'\\\"[^\]]+\\\",\[[0-9]{1,3},[0-9]{1,3}\]'
    current_day_token = re.findall(pattern, maps_html)[0]  # get token from html
    extracted_data = re.findall(r'[\w\s]+', current_day_token)  # extract usable data

    # extracted data now in the current form: [info text, time, crowded] OR [time, crowded]
    if len(extracted_data) == 2:
        time, crowded = [extracted_data[i] for i in (0, 1)]
    else:
        time, crowded = [extracted_data[i] for i in (1, 2)]

    return HourInfo(int(time), crowded)


extract_raw_week_to_week_obj(extract_raw_week('sushi-gladbeck'))
