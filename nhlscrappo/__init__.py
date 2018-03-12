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

from enum import Enum

__version__ = "0.1.0-alpha"

class ReportType(Enum):
    Summary = "GS"
    Roster = "RO"
    Events = "ES"
    FaceOffs = "FS"
    Plays = "PL"
    Shots = "SS"
    HomeTOI = "TH"
    AwayTOI = "TV"

class GameType(Enum):
    Regular = 2
    Playoff = 3

class PlayType(Enum):
    Shot = "SHOT"
    Goal = "GOAL"
    BlockedShot = "BLOCK"
    MissedShot = "MISS"
    Hit = "HIT"
    Faceoff = "FAC"
    Giveaway = "GIVE"
    Takeaway = "TAKE"
    Penalty = "PENL"
    Stoppage = "STOP"
    PeriodStart = "PSTR"
    PeriodEnd = "PEND"
    ShootoutEnd = "SOC"
    GameEnd = "GEND"

class PlayerStrength
    Even = "EV"
    PowerPlay = "PP"
    Shorthand = "SH"
    
    
