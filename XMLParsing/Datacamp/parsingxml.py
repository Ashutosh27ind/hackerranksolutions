import os
import datetime
import xml.etree.ElementTree as et

# Open the xml and get the root element
tree = et.parse('movies.xml')
# Get the root element
root = tree.getroot()

# print(root.tag)
# print(root.attrib)
#
# for child in root:
#     print(child.tag, child.attrib)
# root.iter() : Itereates over all child elements & subchild

# all_tags = [elem.tag for elem in root.iter()]
# print(type(all_tags))
# print(len(all_tags))
# commit
# print(et.tostring(root, encoding='utf8').decode('utf8'))
# for movie in root.iter('movie'):
#     print(movie.attrib)

# print(et.tostring(root,encoding='utf8').decode('utf8'))
#
# for desc in root.iter('description'):
#     print(desc.text)

# Search by tag text
#
# for movie in root.findall("./genre/decade/movie/[rating = 'PG']"):
#     print(movie.attrib['title'])
#     print(movie.attrib['favorite'])
#     # print(type(movie.attrib))

# search by attribute

# for movie in root.findall("./genre/decade/movie/[@favorite = 'True']"):
#     print(movie.attrib['title'])
#     print(movie.attrib['favorite'])
#     # print(type(movie.attrib))
