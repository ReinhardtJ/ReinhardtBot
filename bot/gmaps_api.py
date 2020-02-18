import re
from collections import deque

import requests

from bot.weekdays import WeekInfo, DayInfo, HourInfo, Weekdays


class MapsLocation:
    """
    A MapsLocation represents meta-data of a google maps location, such as the Name, URL,
    Adress and other data which does presumably not change over time.

    Data such as Rating or Crowded need to be fetched every time from Google Maps
    """

    def __init__(self, url: str, full_name: str):
        self.url = url
        self.full_name = full_name


locations = {
    'fitx-adenauer': MapsLocation('https://www.google.de/maps/place/FitX+Fitnessstudio/@51.5495502,7.0786878,' \
                                  '17z/data=!3m1!4b1!4m5!3m4!1s0x47b8e7053e64b21b:0xaf67314083f991e8!8m2!3d51.5495502'
                                  '!4d7.0808765 '
                                  '?hl=de', 'FitX Gelsenkirchen-Erle'),
    'fitx-asbeck': MapsLocation('https://www.google.de/maps/place/FitX+Fitnessstudio/@51.523014,7.0663099,' \
                                '15.5z/data=!4m5!3m4!1s0x47b8e645c7f82f75:0x4338a1e7f7deee66!8m2!3d51.5237398!4d7'
                                '.071133?hl=de'
                                '&authuser=0', 'FitX Gelsenkirchen-Heßler'),
    'sgz-buer': MapsLocation(
        'https://www.google.de/maps/place/Sport-+und+Gesundheitszentrum+Buer/@51.5830114,7.0405425,'
        '17z/data=!4m5!3m4!1s0x0:0xd1508f85ba1da6b5!8m2!3d51.5830116!4d7.0427312',
        'Sport- & Gesundheitszentrum Buer'),

    'sushi-gladbeck': MapsLocation('https://www.google.com/maps/place/Do+Sushi/@51.5733989,6.9889221,'
                                   '15z/data=!4m5!3m4!1s0x0:0xccd9225ca5e829ca!8m2!3d51.5733989!4d6.9889221',
                                   "Do Sushi Gladbeck")
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


def extract_raw_week_to_week_obj(raw_week: str) -> WeekInfo:
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

    # regex for onto match a day: [1,[[ ... ]],0] OR [1,null,1]
    tokenized_days: list = re.findall(r'\[\d,\[\[.+?\]\],\d\]|\[\d,null,\d\]', raw_week)

    for day in tokenized_days:
        day: str = day[1:len(day) - 1]  # removed outer brackets TODO: write function for this operation
        day_index = int(re.search(r'\d', day)[0]) - 1  # first entry is the actual weekday as an int
        tokenized_hours: list = re.findall(r'\[\d.+?\]', day)
        if not tokenized_hours:
            week.set_day(DayInfo(day_index, is_closed=True))
        else:
            for current_hour in tokenized_hours:
                current_hour: str = current_hour[1:len(current_hour) - 1]
                tokenized_current_hour: list = re.split(r',', current_hour)
                time = int(tokenized_current_hour[0])
                crowded = int(tokenized_current_hour[1])
                week.get_day(day_index).set_hour(time, HourInfo(time, crowded, is_closed=False))

    print(week)
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


extract_raw_week_to_week_obj(extract_raw_week('sgz-buer'))
