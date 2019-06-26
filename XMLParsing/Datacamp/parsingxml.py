import os
import datetime
import xml.etree.ElementTree as et
import csv

# Open the XML
tree = et.parse('cd.xml')
# Get the root element
root = tree.getroot()




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



