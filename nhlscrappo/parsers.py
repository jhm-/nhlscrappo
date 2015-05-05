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

from nhlscrappo import ReportType
from nhlscrappo.fetcher import ReportFetcher

class RosterParser(ReportFetcher):
    def __init__(self, season, game_num, game_type):
        super(RosterParser, self).__init__(season, game_num, game_type, \
            ReportType.Roster)
        self.rosters = {"home":{}, "away":{}}
        self.scratches = {"home":{}, "away":{}}
        self.coaches = {"home":{}, "away":{}}
        self.officials = {"refs":{}, "linesmen":{}}

    def __fill_roster_entity(self, td, players):
        tr = td.find_all("tr")
        for data in tr:
            td = data.find_all("td")
            if td[0].attrs["class"] and "heading" not in td[0].attrs["class"]:
                li = [item.string for item in td]
                stats = {"num":li[0], "pos":li[1]}
                # Remove Captain (C) and Assistant (A) adornments
                name = li[2].split("(")[0].rstrip()
                players[name] = stats

    def load_players(self):
        # The visitor team player table is the third table
        td = [data for data in self.soup.find_all("td", {"width":"50%"})][2]
        self.__fill_roster_entity(td, self.rosters["away"])
        # The home team player table is the fourth table
        td = [data for data in self.soup.find_all("td", {"width":"50%"})][3]
        self.__fill_roster_entity(td, self.rosters["home"])

    def load_scratches(self):
        # The visitor scratch table is the fifth table
        td = [data for data in self.soup.find_all("td", {"width":"50%"})][4]
        self.__fill_roster_entity(td, self.scratches["away"])
        # The home scratch table is the sixth table
        td = [data for data in self.soup.find_all("td", {"width":"50%"})][5]
        self.__fill_roster_entity(td, self.scratches["home"])
