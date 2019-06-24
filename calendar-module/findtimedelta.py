import datetime as dt
import pytz
dateString = 'Sun 10 May 2015 13:54:36 -0700'
# parsedDate = dt.datetime.strptime(dateString,'')
d1 = dt.datetime.strptime('Sat 02 May 2015 19:54:36 +0530', '%a %d %b %Y %H:%M:%S %z').astimezone(tz=dt.timezone.utc)
d2 = dt.datetime.strptime('Fri 01 May 2015 13:54:36 -0000', '%a %d %b %Y %H:%M:%S %z').astimezone(tz=dt.timezone.utc)
# print(d1)
# print(d2)
tdelta = d1 - d2
# print(type(tdelta))
if d1 > d2:
    print(d1)
else:
    print(d2)

print(tdelta.days*86400+tdelta.seconds)

