# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import locale

# using your default locale (user settings)
this_locale = locale.setlocale(locale.LC_ALL,'')
stuff = u'aäoöøuü日本語ληνιά123ÅAnñアイウエオあいうえおçciışsğg'
print('stuff=', stuff)

# using sorted-function
print("Sorted without locale:")
print("".join(sorted(stuff)))  # not using locale

print("Sorted in your locale (" + this_locale + "):")
print("".join(sorted(stuff, cmp=locale.strcoll)))

## Note: you have to have these locales precompiled on your system (try the
## command "sudo dpkg-reconfigure locales" to add locales).
nn_locale = locale.setlocale(locale.LC_ALL, 'nn_NO.UTF8'.encode('ascii','replace'))     ## will raise an exception if this locale is not available
print("Sorted in locale " + nn_locale + ':')
print("".join(sorted(stuff, cmp=locale.strcoll))) # using locale

sv_locale = locale.setlocale(locale.LC_ALL, 'sv_SE.UTF8'.encode('ascii','replace'))
print("Sorted in locale " + sv_locale + ':')
print("".join(sorted(stuff, cmp=locale.strcoll))) # using locale

jp_locale = locale.setlocale(locale.LC_ALL, 'ja_JP.UTF8'.encode('ascii','replace'))
print("Sorted in locale " + jp_locale + ':')
print("".join(sorted(stuff, cmp=locale.strcoll))) # using locale

tr_locale = locale.setlocale(locale.LC_ALL, 'tr_TR.UTF8'.encode('ascii','replace'))
print("Sorted in locale " + tr_locale + ':')
print("".join(sorted(stuff, cmp=locale.strcoll))) # using locale

fr_locale = locale.setlocale(locale.LC_ALL, 'fr_FR.UTF8'.encode('ascii','replace'))
print("Sorted in locale " + fr_locale + ':')
print("".join(sorted(stuff, cmp=locale.strcoll))) # using locale

es_locale = locale.setlocale(locale.LC_ALL, 'es_ES.UTF8'.encode('ascii','replace'))
print("Sorted in locale " + es_locale + ':')
print("".join(sorted(stuff, cmp=locale.strcoll))) # using locale

sv_locale = locale.setlocale(locale.LC_ALL, 'nn_NO.UTF8'.encode('ascii','replace'))
print(locale.nl_langinfo(locale.ABMON_1),  locale.nl_langinfo(locale.MON_1))
print(locale.nl_langinfo(locale.ABMON_2),  locale.nl_langinfo(locale.MON_2))
print(locale.nl_langinfo(locale.ABMON_3),  locale.nl_langinfo(locale.MON_3))
print(locale.nl_langinfo(locale.ABMON_4),  locale.nl_langinfo(locale.MON_4))
print(locale.nl_langinfo(locale.ABMON_5),  locale.nl_langinfo(locale.MON_5))
print(locale.nl_langinfo(locale.ABMON_6),  locale.nl_langinfo(locale.MON_6))
print(locale.nl_langinfo(locale.ABMON_7),  locale.nl_langinfo(locale.MON_7))
print(locale.nl_langinfo(locale.ABMON_8),  locale.nl_langinfo(locale.MON_8))
print(locale.nl_langinfo(locale.ABMON_9),  locale.nl_langinfo(locale.MON_9))
print(locale.nl_langinfo(locale.ABMON_10), locale.nl_langinfo(locale.MON_10))
print(locale.nl_langinfo(locale.ABMON_11), locale.nl_langinfo(locale.MON_11))
print(locale.nl_langinfo(locale.ABMON_12), locale.nl_langinfo(locale.MON_12))

## Note: there is a bug in Python 2.7 such that the setlocale() function can only
## accept ASCII-encoded strings!
jp_locale = locale.setlocale(locale.LC_ALL, 'ja_JP.UTF8'.encode('ascii','replace'))
print(locale.nl_langinfo(locale.ABMON_1),  locale.nl_langinfo(locale.MON_1))
print(locale.nl_langinfo(locale.ABMON_2),  locale.nl_langinfo(locale.MON_2))
print(locale.nl_langinfo(locale.ABMON_3),  locale.nl_langinfo(locale.MON_3))
print(locale.nl_langinfo(locale.ABMON_4),  locale.nl_langinfo(locale.MON_4))
print(locale.nl_langinfo(locale.ABMON_5),  locale.nl_langinfo(locale.MON_5))
print(locale.nl_langinfo(locale.ABMON_6),  locale.nl_langinfo(locale.MON_6))
print(locale.nl_langinfo(locale.ABMON_7),  locale.nl_langinfo(locale.MON_7))
print(locale.nl_langinfo(locale.ABMON_8),  locale.nl_langinfo(locale.MON_8))
print(locale.nl_langinfo(locale.ABMON_9),  locale.nl_langinfo(locale.MON_9))
print(locale.nl_langinfo(locale.ABMON_10), locale.nl_langinfo(locale.MON_10))
print(locale.nl_langinfo(locale.ABMON_11), locale.nl_langinfo(locale.MON_11))
print(locale.nl_langinfo(locale.ABMON_12), locale.nl_langinfo(locale.MON_12))
