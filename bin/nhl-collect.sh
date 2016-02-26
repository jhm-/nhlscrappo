#!/usr/bin/env bash
# Copyright © 2015-2016 Jack Morton <jhm@jemscout.com>
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

docroot="http://www.nhl.com/scores/htmlreports"

# For the 2007-2008 to 2014-2015 regular seasons:
# [Note that the 2012-2013 NHL lockout season was a short one (720 games)]
for i in {7..14}
do
  x=0$((i))
  y=0$((i+1))
  dir="20${x: -2}-20${y: -2}"

  echo -e "\n-> building directory $dir"
  mkdir $dir

  echo -e "-> collecting documents"
  for p in {1..1230}
  do
    n=000$((p))
    mkdir $dir/${n: -4}

    # roster
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/RO02${n: -4}.HTM" || continue
    # summary
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/GS02${n: -4}.HTM" || continue
    # events
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/ES02${n: -4}.HTM" || continue
    # face-offs
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/FS02${n: -4}.HTM" || continue
    # play-by-plays
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/PL02${n: -4}.HTM" || continue
    # shots
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/SS02${n: -4}.HTM" || continue
    # home team time-on-ice
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/TH02${n: -4}.HTM" || continue
    # visitor team time-on-ice
    wget -P $dir/${n: -4} -nc -q \
      "$docroot/20${x: -2}20${y: -2}/TV02${n: -4}.HTM" || continue
    echo -n "."
  done
done
echo -e "\n-> done"
