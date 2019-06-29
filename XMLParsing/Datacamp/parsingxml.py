import os
import datetime
import xml.etree.ElementTree as et
import csv
import re

# Open the XML
tree = et.parse('movies.xml')
# Get the root element
root = tree.getroot()

# add node

for decade in root.findall("./genre/decade"):
    print(decade.attrib)
    for year in decade.findall("./movie/year"):
        print(year.text)

action = root.find("./genre[@category = 'Action'")
new_decade = et.SubElement(action, 'decade')











# Correct Data

# for form in root.findall("./genre/decade/movie/format"):
#     match = re.search(',', form.text)
#     if match:
#         form.set('multiple', 'Yes')
#     else:
#         form.set('multiple', 'No')
#
# # tree.write('movies.xml')
# # print xml
# print(et.tostring(root, encoding='utf8').decode('utf8'))

# b2ft = root.find("./genre/decade/movie[@title = 'ALIEN']")
# b2ft.attrib["title"] = 'Alien'
# print(b2ft.attrib["title"])
# print(b2ft.attrib["favorite"])
# tree.write('movies.xml')
#
# print(et.tostring(root, encoding='utf8').decode('utf8'))

# for cd in root.findall('CD'):
#     # print('%s- %s- %s- %s- %s- %s' %(cd.find('TITLE').text,cd.find('ARTIST').text,cd.find('COUNTRY').text,cd.find('PRICE').text,cd.find('COUNTRY').text,
#     #       cd.find('YEAR').text))
#     list_of_values.append([cd.find('TITLE').text,cd.find('ARTIST').text,cd.find('COUNTRY').text,cd.find('PRICE').text,cd.find('COMPANY').text,
#           cd.find('YEAR').text])
#
# with open('out.dat', 'w',newline='') as file:
#     file_writer = csv.writer(file, delimiter='|', dialect='excel')
#     file_writer.writerow(['TITLE','ARTIST','COUNTRY','PRICE','COMPANY','YEAR'])
#     for line in list_of_values:
#         file_writer.writerow(line)
# file.close()
# with open('out.txt', 'a',newline='') as file:
#     file_writer = csv.writer(file, delimiter='|')
#     for cd in root.findall('CD'):
#         title = cd.find('TITLE').text
#         print(title)
#         country = cd.find('COUNTRY').text
#         print(country)
#         file_writer.writerow([title, country])
#
# file.close()

# print(root.tag)
# print(root.attrib)
#
# for child in root:
#     print(child.tag, child.attrib)

# # to know all the tag
# print([elem.tag for elem in root.iter()].index('exists'))
# Show entire doc
# print(et.tostring(root, encoding='utf8').decode('utf8'))

# XPath
# for movie in root.findall("./genre/decade/movie/[year='1979']"):
#     print(movie.attrib)
#
# for desc in root.iter('description'):
#     print(desc.text)



