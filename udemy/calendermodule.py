import calendar

if __name__ == '__main__':
    # c = calendar.TextCalendar(calendar.MONDAY)
    # print(c.formatmonth(2019, 1))


    # print(c.formatmonth(2019, 6))
    # for c in c.itermonthdays(2019, 1):
    #     print(c)
    # for name in calendar.day_name:
    #     print(name)
    # for month in range(1, 2):
    #     mycal = calendar.monthcalendar(2019, 6)
    #     week1 = mycal[0]
    #     print(mycal)
    #     print(calendar.WEDNESDAY)
    #     if week1[calendar.MONDAY] != 0:
    #         auditday = week1[calendar.MONDAY]
    # Calendar object

    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    for day in c.itermonthdates(2018, 9):
        print(day)

    print(calendar.TextCalendar(firstweekday=calendar.SUNDAY).formatmonth(2018, 9))
    for day in calendar.Calendar(firstweekday=calendar.SUNDAY).iterweekdays():
        if day == calendar.SUNDAY:
            print('Sunday')
        else:
            print('Not Sunday')
    





