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

from nhlscrappo import ReportType
from nhlscrappo.fetcher import ReportFetcher

class RosterParser(ReportFetcher):
    """Parse the roster report and fill appropriate fields"""

    def __init__(self, season, game_num, game_type):
        super(RosterParser, self).__init__(season, game_num, game_type, \
            ReportType.Roster)

        self.rosters = {"home": {}, "away": {}}
        """Player rosters {"home/away": {name: {"num", "pos"}}}"""

        self.scratches = {"home": {}, "away": {}}
        """Healthy scratches {"home/away": {name: {"num", "pos"}}}"""
        
        self.coaches = {"home": {}, "away": {}}
        """Team coaches {"home/away": name}"""
        
        self.officials = {"refs": {}, "linesmen": {}}
        """Game officials {"refs/linesmen": {number: name}}"""

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

    def load_coaches(self):
        td = [data for data in self.soup.find_all("td", {"width":"50%"})]
        # The coaches tables are the seventh and eigth tables
        for i, cell in enumerate(td[6:8]):
            keys = ["home", "away"]
            tr = cell.find_all("tr")
            self.coaches[keys[i]] = tr[0].find("td").string

    def __get_num(self, s):
        s = s.replace("#", "").strip()
        return int(s) if s.isdigit() else -1

    def __num_name(self, s):
        s = s.split(" ")
        if len(s) > 1:
            num = self.__get_num(s[0])
            name = " ".join(si.strip() for si in s[1:])
        else:
            num = __get_num(s) if "#" in s else -1
            name = s if num == -1 else ""
        return num, name

    def __make_dict(self, o):
        d = {}

        for oi in o:
            num, name = self.__num_name(oi)
            if num in d:
                num = max(d.keys() + 1)
            d[num] = name
            return d

    def load_officials(self):
        td = [data for data in self.soup.find_all("td", {"width":"100%"})]
        tr = [cell for cell in td[2].find_all("tr", {"valign":"top","id":""})]
        ltd = [cell for cell in tr[0].find_all("td", {"align":"left"})]
        referees = [ref.string for ref in ltd[0].find_all("td")]
        self.officials["refs"] = self.__make_dict(referees)
        # English format:
        if referees:
            linesmen = [lm.string for lm in ltd[3].find_all("td")]
            self.officials["linesmen"] = self.__make_dict(linesmen)
        # French format:
        else:
            referees = [ltd[0].string, ltd[1].string]
            self.officials["refs"] = self.__make_dict(referees)
            ltd = [cell for cell in tr[0].find_all("td", {"align":"center"})]
            linesmen = [ltd[5].string, ltd[6].string]
            self.officials["linesmen"] = self.__make_dict(linesmen)

class ShotParser(ReportFetcher):
    """Parse the shot summary report and fill appropriate fields"""

    def __init__(self, season, game_num, game_type):
        super(ShotParser, self).__init__(season, game_num, game_type, \
            ReportType.Shots)

        self.shots = {"away": {}, "home": {}}
        """
        Player shot summary statistics
        {"home/away": {name: {period: {"EV", "PP", "SH", "TOT"}}}}
        """

    def __make_list(self, i):
        keys = ["EV", "PP", "SH", "TOT"]

        j = [k for k in i.find_all("td")]
        # l is a list of 5 entities, with the first being the period and the
        # remaining 4 corresponding to the above keys
        l = [p.string for p in j]
        l = [u.replace(u"\xa0", u"") for u in l]
        # A "TOT" rather than a number signifies the end of the statistics for
        # this player
        if l[0] == "TOT":
            return None
        # Create a list where the first entity is the period and the second
        # entity is a dictionary containing the stats
        return  [l[0], dict(zip(keys, l[1:]))]

    def __period_dict(self, stat):
        summary = {}

        # Create a dictionary and assign statistics to a keyed period number
        for split in stat:
            split[0] = "4" if split[0] == "OT" else split[0]
            summary[int(split[0])] = split[1]
        return summary

    def __fill_shots_entity(self, table):
        player_names = []
        player_stats = []
        pstat = []

        tr = [cell for cell in table[3].find_all("tr")]
        # The first list we generate is for the player names
        for i in tr:
            if not i.attrs:
                ptd = [cell for cell \
                    in i.find_all("td", {"align":"center", "class":""})]
                if len(ptd) > 2:
                    name = " ".join([ptd[1].string, ptd[2].string])
                    player_names.append(name)
        # The second list we generate is for the player statistics
        for i in tr:
            evenColor = [cell for cell \
                in i.find_all("tr", {"class":"evenColor"})]
            oddColor = [cell for cell \
                in i.find_all("tr", {"class":"oddColor"})]
            if oddColor:
                for line in oddColor:
                    p = self.__make_list(line)
                    if p is not None:
                        pstat.append(p)
                    else:
                        player_stats.append(self.__period_dict(pstat))
                        pstat = []
            if evenColor:
                for line in evenColor:
                    p = self.__make_list(line)
                    if p is not None:
                        pstat.append(p)
                    else:
                        player_stats.append(self.__period_dict(pstat))
                        pstat = []
        # Zip the two lists together into a dictionary
        return dict(zip(player_names, player_stats))

    def load_shots(self):
        td = [data for data in self.soup.find_all("td", {"width":"50%"})]
        # 4 is visitor, 5 is home
        table = [cell for cell in td[4].find_all("table")]
        self.shots["away"] = self.__fill_shots_entity(table)
        table = [cell for cell in td[5].find_all("table")]
        self.shots["home"] = self.__fill_shots_entity(table)


class TOIParser(ReportFetcher):
    """Parse the time-on-ice data"""

    def __init__(self, season, game_num, game_type, report_type):
        super(TOIParser, self).__init__(season, game_num, game_type, \
            report_type)
        self.players = {"name": {}}
        """
        Player time-on-ice statistics
        {name: {period: {"shift", "start of shift", "end of shift", "event"}}}
        """

class HomeTOIParser(TOIParser):
    """Parse the time-on-ice data for the home team and fill appropriate fields"""

    def __init__(self, season, game_num, game_type):
        super(HomeTOIParser, self).__init__(season, game_num, game_type, \
            ReportType.HomeTOI)


class VisitorTOIParser(TOIParser):
    """Parse the time-on-ice-data for the visiting team and fill appropriate fields"""

    def __init__(self, season, game_num, game_type):
        super(VisitorTOIParser, self).__init__(season, game_num, game_type, \
            ReportType.VisitorTOI)
