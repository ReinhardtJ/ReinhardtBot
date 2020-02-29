import logging
import re
import requests

from bot.gmaps import gmaps_location


class DataExtractor:
    """Performs a request to a google maps location via its URL and extracts
    various data as raw string."""

    def __init__(self, should_write_data_to_file: bool = False):
        self.logger = logging.getLogger(__name__)
        self.should_write_data_to_file = should_write_data_to_file

    def raw_week_from_html(self, html: str) -> str:
        """Uses a whole google maps html-page to return just the array with
        information how visited it is as a string.

        :param html: a google maps html page as string
        :return: a string representing a week
        """
        match_week_regex = r'\[\[\[\d,\[\[\d,\d,.+?\]\],\d\]\]'
        week = re.findall(match_week_regex, html)[0]

        if self.should_write_data_to_file:
            self.write_data_to_file(week)

        return week

    def html_from_location(self, location: str) -> str:
        """Sends a request to the google maps server and returns its html.

        :param location: a location as secified in
        :return:
        """

        # get raw html from google maps
        url: str = gmaps_location.GmapsLocation.location_urls[location]
        html: str = requests.get(url, {}).text

        # pre-format a string containing only the necessary information
        html = re.sub(r'\\n|\\\"', '', html)

        # write html to text file for testing purposes
        if self.should_write_data_to_file:
            self.write_data_to_file(html)

        return html

    def write_data_to_file(self, data: str) -> None:
        with open('gmaps/maps_data.txt', 'r+', encoding='utf-8') as file:
            file.seek(0)
            file.write(data)
            file.truncate()
