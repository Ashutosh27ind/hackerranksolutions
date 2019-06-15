import logging
import os
import fnmatch

if __name__ == '__main__':
    # print(len('  HACK  '))
    # print(len('  HACK  '.strip()))
    DateString = list(map(int, input().split()))
    print('Day {} Month {} Year {}'.format(DateString[0],DateString[1],DateString[2]))

