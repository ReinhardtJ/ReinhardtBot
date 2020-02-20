import datetime
import logging
import re
import requests
from bot import weekdays


class GmapsLocation:
    """Represents meta-data of a google maps location.
    Such as the Name, URL, Address and other data which does presumably not change over time.

    Data such as Rating or 'visited' need to be fetched every time from Google Maps

    TODO: can we find a better solution instead of hard-coding the url?
    """

    location_urls = {
        'fitx-adenauer': 'https://www.google.de/maps/place/FitX+Fitnessstudio/@51.5495502,7.0786878,17z/data=!3m1!4b1!4m5!3m4!1s0x47b8e7053e64b21b:0xaf67314083f991e8!8m2!3d51.5495502!4d7.0808765?hl=de',

        'fitx-asbeck': 'https://www.google.de/maps/place/FitX+Fitnessstudio/@51.523014,7.0663099,15.5z/data=!4m5!3m4!1s0x47b8e645c7f82f75:0x4338a1e7f7deee66!8m2!3d51.5237398!4d7.071133?hl=de&authuser=0',

        'sgz-buer': 'https://www.google.de/maps/place/Sport-+und+Gesundheitszentrum+Buer/@51.5830114,7.0405425,17z/data=!4m5!3m4!1s0x0:0xd1508f85ba1da6b5!8m2!3d51.5830116!4d7.0427312',

        'sushi-gladbeck': 'https://www.google.com/maps/place/Do+Sushi/@51.5733989,6.9889221,15z/data=!4m5!3m4!1s0x0:0xccd9225ca5e829ca!8m2!3d51.5733989!4d6.9889221'
    }

    def __init__(self, location):
        self.logger = logging.getLogger(__name__)

        html = self.get_html_from_location(location)
        raw_week: str = self.raw_week_from_html(html)

        self.weekday: int = datetime.datetime.today().weekday()
        self.time_index = int(datetime.datetime.now().strftime("%H"))
        self.weekday_name: str = weekdays.WeekModel.weekday_names[self.weekday]

        self.week = self.raw_week_to_weekmodel(raw_week)
        self.current_time = self.html_to_current_hourmodel(html)

    def get_visited(self, day: str, hour: int):
        day_index: int = weekdays.WeekModel.weekday_names.index(day)
        day_info = self.week.get_day(day_index)
        hour_info = day_info.get_hour(hour)
        response: str = f'Am {day_info.name} zwischen {hour_info.time}:00 und {hour_info.time + 1}:00 ist ' \
                        f'es zu {hour_info.visited}% voll. '
        return response

    def get_current_visited(self):
        day_info = self.week.get_day(self.weekday)

        # get historical time info for the current situation for comparison
        statistic_hour_info = day_info.get_hour(self.current_time.time)
        hour_info = self.current_time
        response = f'Jetzt gerade ist es zu {hour_info.visited}% voll. ' \
                   f'Normalerweise ist es am {day_info.name} zu dieser Zeit zu {statistic_hour_info.visited}% voll.'
        return response

    def get_html_from_location(self, location: str) -> str:
        """
        :param location:
        :return:
        """
        # get raw html from google maps
        url: str = GmapsLocation.location_urls[location]
        html: str = requests.get(url, {}).text

        # pre-format a string containing only the necessary information
        html = re.sub(r'\\n|\\\"', '', html)
        # write html to text file for testing purposes
        # with open('maps_data.txt', 'r+', encoding='utf-8') as file:
        #     file.seek(0)
        #     file.write(html)
        #     file.truncate()
        return html

    def raw_week_from_html(self, html: str) -> str:
        match_week_regex = r'\[\[\[\d,\[\[\d,\d,.+?\]\],\d\]\]'
        week = re.findall(match_week_regex, html)[0]
        # with open('maps_data.txt', 'r+', encoding='utf-8') as file:
        #     file.seek(0)
        #     file.write(week)
        #     file.truncate()
        return week

    def raw_week_to_weekmodel(self, raw_week: str) -> weekdays.WeekModel:
        """Takes a html-extracted representation of a week and returns a WeekModel object built from this data.

        This raw data is received as a nested array form:
            [[hour, hour, hour,...,hour],[...],...[]]
        whereas each hour is an array with up to 5 entries representing different information about each hour:
            hour = [17,22,Normalerweise nicht zu stark besucht,,17 Uhr]

        If a location is closed at certain days, these days have a form of: [1,null,1]

        Not all hours must necessarily be represented. From observation, closing hours may be simply skipped.

        :param raw_week: a string representation of a week from a google maps html document
        :return: a WeekModel
        """

        week = weekdays.WeekModel()

        match_day_regex = r'\[\d,\[\[.+?\]\],\d\]|\[\d,null,\d\]'
        tokenized_days: list = re.findall(match_day_regex, raw_week)

        for raw_day in tokenized_days:
            raw_day: str = raw_day[
                           1:len(raw_day) - 1]  # removed outer brackets TODO: write function for this operation
            day_index = int(re.search(r'\d', raw_day)[0]) - 1  # first entry is the actual weekday as an int
            match_hour_regex = r'\[\d.+?\]'
            tokenized_hours: list = re.findall(match_hour_regex, raw_day)
            if not tokenized_hours:
                week.set_day(weekdays.DayModel(day_index, is_closed=True))
            else:
                for current_hour in tokenized_hours:
                    current_hour: str = current_hour[1:len(current_hour) - 1]
                    tokenized_current_hour: list = re.split(r',', current_hour)
                    time = int(tokenized_current_hour[0])
                    visited = int(tokenized_current_hour[1])
                    week.get_day(day_index).set_hour(time, weekdays.HourModel(time, visited, is_closed=False))

        return week

    def html_to_current_hourmodel(self, html: str) -> weekdays.HourModel:
        match_current_visited_regex = r'\],[\w\sÄÖÜäöüß]+?,\[\d{1,3},\d{1,3}\]\]'
        raw_current_day: list = re.findall(match_current_visited_regex, html)  # get token from html
        if len(raw_current_day) == 0:
            return self.week.get_day(self.weekday).get_hour(self.time_index)

        raw_current_day: str = raw_current_day[0]
        extracted_data = re.findall(r'\d+', raw_current_day)  # extract usable data

        # extracted data now in the current form: [time, visited]
        time, visited = [extracted_data[i] for i in (0, 1)]

        return weekdays.HourModel(int(time), visited)

# location = GmapsLocation('fitx-adenauer')
