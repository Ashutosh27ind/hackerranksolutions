import re

num_of_input = int(input())
for t in range(num_of_input):
    try:
        reg_exp = input()
        re.compile(reg_exp)
        is_valid = True
        print(is_valid)
    except Exception as e:
        print(e)
        is_valid = False
        print(is_valid)



