
Changes
=======


1.6 (2019-08-27)
----------------

- Drop support for old Python and Django versions.
  This enables support for new Django versions
  which do not have Python 2 compatibility shims.
- Add continuous delivery via Jazzband.
- Add SCM versioning via setuptools_scm.


1.5 (2018-10-10)
----------------

- Add support for Django 1.11. *Thanks, Martin Bächtold*
- Drop support for Python 2.6. *Thanks, Martin Bächtold*
- Add support for categories, rrule, exrule, rrdate, exdate. *Thanks, Armin Leuprecht*
- Fix a documentation typo. *Thanks, Giorgos Logiotatidis*
- Add documentation and testing around recurring events. *Thanks, Christian Ledermann*
- Remove tests for Django versions < 1.8 *Thanks, Christian Ledermann*


1.4 (2016-05-08)
----------------

- Django up to 1.9 is supported.
- Added new `ttl` parameter. *Thanks, Diaz-Gutierrez*
- Added support for Python 3. *Thanks, Ben Lopatin*
- Fixed LAST-MODIFIED support. *Thanks, Brad Bell*


1.3 (2014-11-26)
----------------

- Django up to 1.7 is supported.
- Added a new `file_name` parameter. *Thanks, browniebroke*
- Added support for the `ORGANIZER` field. *Thanks, browniebroke*


1.2 (2012-12-12)
----------------

- Removed support for Django 1.2. It should still work, but it's not supported.
- We now require icalendar 3.1.
- Added support for the `GEO` field. *Thanks, null_radix!*


1.1 (2012-10-26)
----------------

- Fixed issues running tests on Django 1.2 and Django 1.5.


1.0 (2012-05-06)
----------------

- Initial Release
