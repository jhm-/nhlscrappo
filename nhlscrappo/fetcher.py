# Copyright (c) 2015 Jack Morton <jhm@jemscout.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bs4 import BeautifulSoup
from urllib.request import urlopen
import nhlscrappo.constants as C
from nhlscrappo import GameType, ReportType

class ReportFetcher(object):
    """Responsible for fetching and validating the report fields"""

    __docroot = "http://www.nhl.com/"

    def __init__(self, season, game_num, game_type, report_type):
        self.season = season
        self.game_num = game_num
        self.game_type = game_type
        self.report_type = report_type
        self.soup = None

    def __load_html(self, url):
        if "http://" in url:
            with urlopen(url) as handle:
                html = handle.read()
                handle.close()
        else:
            with open(url, "r") as handle:
                html = handle.read()
                handle.close()
        return BeautifulSoup(html.decode("utf-8"))

    def make_soup(self, local = None):
        if local:
            soup = self.__load_html(local)
        else:
            url = self.__docroot + "scores/htmlreports/" + str(self.season) + \
                str(self.season + 1) + "/" + self.report_type.value + "0" + \
                str(self.game_type.value) + ("%04i" % self.game_num) + ".HTM"
            self.soup = self.__load_html(url)
        return self.soup

    @property
    def season(self):
        return self._season

    @season.setter
    def season(self, value):
        if not isinstance(value, int):
            raise TypeError("season must be of type int")
        if value < C.MIN_SEASON or value > C.MAX_SEASON:
            raise ValueError("Only seasons starting from " + \
                str(C.MIN_SEASON) + " until " + str(C.MAX_SEASON) + \
                " are supported")
        self._season = int(value)

    @property
    def game_num(self):
        return self._game_num

    @game_num.setter
    def game_num(self, value):
        if not isinstance(value, int):
            raise TypeError("game_num must be of type int")
        self._game_num = value

    @property
    def game_type(self):
        return self._game_type

    @game_type.setter
    def game_type(self, value):
        if value in GameType:
            self._game_type = value
        else:
            raise TypeError("game_type must be of type GameType")

    @property
    def report_type(self):
        return self._report_type

    @report_type.setter
    def report_type(self, value):
        if value in ReportType:
            self._report_type = value
        else:
            raise TypeError("report_type must be of type ReportType")

    @property
    def soup(self):
        return self._soup

    @soup.setter
    def soup(self, value):
        if value is not None and not isinstance(value, BeautifulSoup):
            raise TypeError("soup must be of type BeautifulSoup")
        self._soup = value