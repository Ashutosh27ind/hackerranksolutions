import datetime
import pytz


# instantiate a date object
d = datetime.date(2018, 1, 20)

# today
tday = datetime.date.today()
print(tday.isoweekday())

tdelta = datetime.timedelta(days=-7)
# date1 = date2 - timedelta
# date1 + date2 = timedelta

# Calcualte how many days have passed since my birthday

bday = datetime.date(1988, 3, 12)
print((datetime.date.today() - bday).total_seconds())

dt = datetime.datetime(2016,3,11,13,20,45)
print(dt)
# print year, month and day
print(dt.year)
print(dt.month)
print(dt.day)
print(dt.time())
# You can use timedeta as before
print(dt + tdelta)
# Handling timezone
print('Hadling timezones now')
dt_1 = datetime.datetime.today()
dt_2 = datetime.datetime.now()  # You can passin timeozone info here
dt_3 = datetime.datetime.utcnow() # UTC time or Greenwich time

print(dt_1)
print(dt_2)
print(dt_3)

print('TimeZone')

# dt_iran = datetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
# # Current time in Iran is
# print(dt_iran)
# dt_ist = dt_iran.astimezone(pytz.timezone('Asia/Kolkata'))
# print(dt_ist)

# Print out all timezones in pytz
#
# for tz in pytz.all_timezones:
#     print(tz)


dt_ist = datetime.datetime.now()
dt_est = dt_ist.astimezone(pytz.timezone('US/Eastern'))
# strftime - string format time.
print(dt_est.strftime('%d-%b-%Y'))















