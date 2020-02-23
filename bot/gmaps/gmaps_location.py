import datetime
import logging
import re

from bot.gmaps import gmaps_data_mining as mining
from bot.gmaps import weekdays


class GmapsLocation:
    """Represents meta-data of a google maps location.
    Such as the Name, URL, Address and other data which does presumably not change over time.

    Data such as Rating or 'visited' need to be fetched every time from Google Maps

    TODO: can we find a better solution instead of hard-coding the url?
    """

    location_urls = {
        'ge-fitx-erle': 'https://www.google.de/maps/place/FitX+Fitnessstudio/@51.5495502,7.0786878,17z/data=!3m1!4b1!4m5!3m4!1s0x47b8e7053e64b21b:0xaf67314083f991e8!8m2!3d51.5495502!4d7.0808765?hl=de',

        'ge-fitx-heßler': 'https://www.google.de/maps/place/FitX+Fitnessstudio/@51.523014,7.0663099,15.5z/data=!4m5!3m4!1s0x47b8e645c7f82f75:0x4338a1e7f7deee66!8m2!3d51.5237398!4d7.071133?hl=de&authuser=0',

        'buer-sgz': 'https://www.google.de/maps/place/Sport-+und+Gesundheitszentrum+Buer/@51.5830114,7.0405425,17z/data=!4m5!3m4!1s0x0:0xd1508f85ba1da6b5!8m2!3d51.5830116!4d7.0427312',
        
        'pb-innenstadt': 'https://www.google.com/maps/place/Neptunbrunnen/@51.7182793,8.7548976,226m/data=!3m1!1e3!4m5!3m4!1s0x47ba4c966c50ea83:0x1ea56e5da0f2f191!8m2!3d51.7181414!4d8.7552519',

        'pb-fitnessloft': 'https://www.google.com/maps/place/FitnessLOFT+Paderborn/@51.717339,8.7484284,538m/data=!3m2!1e3!4b1!4m5!3m4!1s0x47ba4c97db86e3b5:0x4f2a06c7421cd342!8m2!3d51.717339!4d8.7506171',

        'pb-fit4u': 'https://www.google.com/maps/place/F4U+Paderborn/@51.7341796,8.77477,538m/data=!3m1!1e3!4m5!3m4!1s0x0:0x79e8386e8d99c69c!8m2!3d51.7341798!4d8.7769584'
    }

    location_names_as_list = list(location_urls.keys())

    def __init__(self, location):
        self.logger = logging.getLogger(__name__)

        # get and run data extractor
        dextractor = mining.DataExtractor()
        html = dextractor.html_from_location(location)
        raw_week: str = dextractor.raw_week_from_html(html)

        self.weekday: int = datetime.datetime.today().weekday()
        self.time_index = int(datetime.datetime.now().strftime("%H"))
        self.weekday_name: str = weekdays.WeekModel.weekday_names[self.weekday]

        self.week = self.raw_week_to_weekmodel(raw_week)
        self.current_time = self.html_to_current_hourmodel(html)

    def get_visited(self, day_index: int, hour: int) -> str:
        """
        Generates a readable message of how visited this location.
        :param day_index: Which day we are looking for (0 = Monday, 1 = Tuesday,
        etc.)
        :param hour: Which hour are we looking for
        :return: A message
        """
        day_info = self.week.get_day(day_index)
        hour_info = day_info.get_hour(hour)
        response: str = f'Am {day_info.name} zwischen {hour_info.time}:00 ' \
                        f'und {hour_info.time + 1}:00 ist es zu ' \
                        f'{hour_info.visited}% voll. '
        return response

    def get_current_visited(self):
        day_info = self.week.get_day(self.weekday)

        # get historical time info for the current situation for comparison
        statistic_hour_info = day_info.get_hour(self.current_time.time)
        hour_info = self.current_time
        response = f'Jetzt gerade ist es zu {hour_info.visited}% voll. ' \
                   f'Normalerweise ist es am {day_info.name} zu dieser Zeit ' \
                   f'zu {statistic_hour_info.visited}% voll.'
        return response

    def raw_week_to_weekmodel(self, raw_week: str) -> weekdays.WeekModel:
        """Takes a html-extracted representation of a week and returns a
        WeekModel object built from this data.

        This raw data is received as a nested array form:
            [[hour, hour, hour,...,hour],[...],...[]]
        whereas each hour is an array with up to 5 entries representing
        different information about each hour:
            hour = [17,22,Normalerweise nicht zu stark besucht,,17 Uhr]

        If a location is closed at certain days, these days have a form of:
        [1,null,1]

        Not all hours must necessarily be represented. From observation,
        closing hours may be simply skipped.

        :param raw_week: a string representation of a week from a google maps
        html document
        :return: a WeekModel
        """

        week = weekdays.WeekModel()

        # programmatically extract information top-down
        match_day_regex = r'\[\d,\[\[.+?\]\],\d\]|\[\d,null,\d\]'
        tokenized_days: list = re.findall(match_day_regex, raw_week)

        for raw_day in tokenized_days:

            raw_day: str = self.clip_string(raw_day)
            day_index = int(re.search(r'\d', raw_day)[0]) - 1
            match_hour_regex = r'\[\d.+?\]'
            tokenized_hours: list = re.findall(match_hour_regex, raw_day)

            # if we can't find any hour tokens for this day, assume this das is closed
            if not tokenized_hours:
                week.set_day(weekdays.DayModel(day_index, is_closed=True))
            else:
                for current_hour in tokenized_hours:

                    current_hour: str = self.clip_string(current_hour)
                    tokenized_current_hour: list = re.split(r',', current_hour)
                    time = int(tokenized_current_hour[0])
                    visited = int(tokenized_current_hour[1])
                    hour_model = weekdays.HourModel(time, visited, is_closed=False)

                    current_day = week.get_day(day_index)
                    current_day.set_hour(time, hour_model)

        return week

    def html_to_current_hourmodel(self, html: str) -> weekdays.HourModel:
        """Takes a full google maps html-page and returns a HourModel object
        of how visited a place is right now (= was at the time the html was
        requested).

        :param html: a raw html document
        :return: a HourModel
        """
        match_current_visited_regex = r'\],[\w\sÄÖÜäöüß]+?,\[\d{1,3},\d{1,3}\]\]'
        raw_current_day: list = re.findall(match_current_visited_regex, html)  # get token from html
        if len(raw_current_day) == 0:
            return self.week.get_day(self.weekday).get_hour(self.time_index)

        raw_current_day: str = raw_current_day[0]
        extracted_data = re.findall(r'\d+', raw_current_day)  # extract usable data

        # extracted data now in the current form: [time, visited]
        time, visited = [extracted_data[i] for i in (0, 1)]

        return weekdays.HourModel(int(time), visited)

    def clip_string(self, string: str) -> str:
        """Removes the first and last character in a string."""
        return string[1:len(string) - 1]

# location = GmapsLocation('fitx-adenauer')
