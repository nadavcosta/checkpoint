import requests
import re
import pickle
from urls import URLS

MONTHS = {1: '01', 2: '02', 3: '03', 4: '04',
          5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12'}

MONTHS_TO_NAMES = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
                   '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October',
                   '11': 'November', '12': 'December'}

DAYS = {1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11',
        12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22',
        23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31'}


class Scraper(object):
    """"""
    "The crawler engine is responsible for fetching and locally storing content from the internet."

    VALID_YEARS = [1994] + list(range(1996, 2021))

    def __init__(self, year_start, year_end):
        # @set:
        self.base_url = URLS['base']
        self.archive_url = URLS['archive']

        self.year_start, self.year_end = self._get_valid_years(int(year_start), int(year_end))
        self.archive_text = self._get_archive_page_raw_text()
        # @init:
        self.titles = {}
        self.title_start = 'title="">'
        self.title_end = '</a>'

    def _get_valid_years(self, year_start, year_end):
        """@[_get_valid_years]
            year_start (int):
            year_end (int):
        """
        if year_start < self.VALID_YEARS[0]:
            year_start = self.VALID_YEARS[0]

        if year_end > self.VALID_YEARS[-1]:
            year_end = self.VALID_YEARS[-1]
        # @[int, int]
        return year_start, year_end

    def _generate_url(self, date):
        """[_generate_url]
        :param date (str):
        return:
            (month example) "https://www.dailymail.co.uk/home/sitemaparchive/month_201512.html"
            (day example)   "https://www.dailymail.co.uk/home/sitemaparchive/day_20151201.html"
        """
        # @[str]
        return self.base_url + date + '.html'

    def _get_archive_page_raw_text(self):
        """"""
        return requests.get(self.archive_url).text

    def _get_titles_from_page(self, raw_text):
        # @[list]
        return re.findall(self.title_start + '(.*)' + self.title_end, raw_text)

    def _does_month_exit(self, year, month):
        return re.search("month_" + year + month, self.archive_text)

    def _does_day_exit(self, year, month, day, text):
        return re.search(day + " " + month + " " + year, text)

    def set_titles(self):

        for year in range(self.year_start, self.year_end+1):
            self.titles[year] = self._add_year(str(year))
            with open('titles_' + str(year) + '.pickle', 'wb') as h:
                pickle.dump(self.titles[year], h, protocol=pickle.HIGHEST_PROTOCOL)

    def _add_year(self, year):
        """
        Args:
            year (str):
        """
        year_dict = {}
        for _, month in MONTHS.items():
            if self._does_month_exit(year=year, month=month):
                year_dict[month] = self._add_month(year=year, month=month)
        # @[dict]
        return year_dict

    def _add_month(self, year, month):
        """
        Args:
            year (str):
            month (str):
        """
        raw_text = requests.get(self._generate_url(date="month_"+year+month)).text
        month_dict = {}

        for _, day in DAYS.items():
            if self._does_day_exit(year=year, month=MONTHS_TO_NAMES[month], day=day, text=raw_text):
                month_dict[day] = self._add_day(year, month, day)
        # @[dict, ]
        return month_dict

    def _add_day(self, year, month, day):
        # generate url:
        url = self._generate_url(date="day_" + year + month + day)
        # @[list]
        return self._get_titles_from_page(raw_text=requests.get(url).text)

    def init_titles(self):
        pass

    def update_titles(self):
        pass


if __name__ == '__main__':
    scraper_ = Scraper(year_start=2008, year_end=2018)

    scraper_.set_titles()

