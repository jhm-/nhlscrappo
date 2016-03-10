# Copyright (c) 2015-2016 Jack Morton <jhm@jemscout.com>
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

import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
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

    def __random_user_agent(self):
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, " \
                "like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 " \
                "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "\
                "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like " \
                "Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, " \
                "like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like " \
                "Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like " \
                "Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, " \
                "like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like " \
                "Gecko) Chrome/19.0.1063.0 Safari/536.3",\
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3" \
                " (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like " \
                "Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, " \
                "like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like " \
                "Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, " \
                "like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like " \
                "Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like " \
                "Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like " \
                "Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, " \
                "like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
        return random.choice(user_agent_list)

    def __load_html(self, url):
        if "http://" in url:
            req = Request(url, headers = {
                "User-Agent": self.__random_user_agent(), \
                "Accept": "text/html,application/xhtml+xml,application/" \
                    "xml;q=0.9,*/*;q=0.8", \
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", \
                "Accept-Encoding": "none", \
                "Accept-Language": "en-US,en;q=0.8", \
                "Connection": "keep-alive"})
            with urlopen(req) as handle:
                html = handle.read()
                handle.close()
        else:
            with open(url, "r") as handle:
                html = handle.read()
                handle.close()
        return BeautifulSoup(html.decode("utf-8"), "lxml")

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
