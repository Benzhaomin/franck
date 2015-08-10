# Franck 0.5.0 (2015/08/10)
  - Switched from Flask to Bottle [franck-http]
  - Rewrote the CLI module [franck-cli]
  - API: api.video() now returns None if no video is found at the given url [franck]

# Franck 0.4.0 (2015/07/23)
  - File naming and structure overhaul
  - Added tests [franck]
  - Added logging [franck][franck-http]
  - Pure CSS responsive grid [franck-http]
  - Display videos inline in a <video> tag [franck-http]

# Franck 0.3.0 (2015/07/15)
  - Switch to git
  - Support for jv.com's new design
  - Added a parser, uses BeautifulSoup, no more parsing inside model/
  - Added a crawler

# Franck 0.2.0 (2014/10/18)
  - FIX: cached config files now include the subpath to prevent collisions. All existing cache is now invalid.
  - Added news page support. Some videos in news are from third-party sources, we ignore those.

# Franck 0.1.0 (2014/10/03)
  - First alpha version.
