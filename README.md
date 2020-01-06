![logo](nhlscrappo-logo.png)

# NHL Game Summary Web Scraping Library

NHLscrappo is a scraping library for Real Time Shot System (RTSS) reports, which
are hosted on NHL.com. Data from these reports are stored in various objects
that are designed to be polled and integrated into a relational database, such
as SQL. RTSS reports contain game-by-game summaries on players, plays and more.
NHLscrappo does not itself have the capacity for any statistical analysis.

**This is a legacy project!**
The NHL now provides a public API, which negates the need for this libray. No
longer do we have to scrape the RTSS files. You can find more information
about this undocumented API
[here.](https://www.kevinsidwar.com/iot/2017/7/1/the-undocumented-nhl-stats-api)

## Requirements

The only requirements are python wih the
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) library, best installed
using [pip](https://pypi.python.org/pypi/pip).

## License

Released under the [MIT license](LICENSE)
