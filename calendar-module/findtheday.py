import calendar

# Take the input

input_date = list(map(int, input().split()))
vmonth = input_date[0]
vday = input_date[1]
vyear = input_date[2]
# print(vmonth)

c = calendar.weekday(vyear, vmonth, vday)

if calendar.MONDAY == c:
    print('MONDAY')

if calendar.TUESDAY == c:
    print('TUESDAY')

if calendar.WEDNESDAY == c:
    print('WEDNESDAY')

if calendar.THURSDAY == c:
    print('THURSDAY')

if calendar.FRIDAY == c:
    print('FRIDAY')

if calendar.SATURDAY == c:
    print('SATURDAY')

if calendar.SUNDAY == c:
    print('SUNDAY')

# week1 = c[0]
# week2 = c[1]

# print(c.firstweekday)
# print(calendar.SATURDAY)


# # for days in c.:
# #     try:
# #         if c.index(vday) == calendar.WEDNESDAY:
# #             print('Wednesday')
# #     except ValueError:
# #         pass
# #     except Exception as e:
# #         print(e)
# mycal = calendar.monthcalendar(vyear, vmonth)
#
# week1 = mycal[0]
# week2 = mycal[1]
# week3 = mycal[2]
#
# if week1[calendar.MONDAY] != 0:
#     auditday = week1[calendar.MONDAY]
# else:
#     auditday = week2[calendar.MONDAY]
#
# print(week3[calendar.TUESDAY])
# print(week3)