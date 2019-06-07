import re

patterns = ['terms1', 'terms2']
text = 'This is a string with terms1 but not with other'

for pattern in patterns:
    # print('Searching for %s in \n %s' % (pattern, text))
    if re.search(pattern,text):
        print('Pattern %s found in \n%s' %(pattern,text))
    else:
        print('Not Found')

split_term = '@'
phrase = 'Is your email address hello@gmail.com?'
