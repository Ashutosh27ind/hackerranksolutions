import calendar

# Take the input

input_date = list(map(int, input().split()))
vmonth = input_date[0]
vday = input_date[1]
vyear = input_date[2]
# print(vmonth)

c = calendar.Calendar(firstweekday=calendar.SUNDAY).


# week1 = c[0]
# week2 = c[1]

for days in c:
    try:
        if c.index(vday) == calendar.WEDNESDAY:
            print('Wednesday')
    except ValueError:
        pass
    except Exception as e:
        print(e)

