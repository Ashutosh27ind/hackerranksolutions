import os
import datetime
import xml.etree.ElementTree as et

# Open the XML
# tree = et.parse('movies.xml')
# # Get the root element
# root = tree.getroot()

tree = et.parse('short.xml')
root = tree.getroot()
for head in root.findall('//with_attributes'):
    name = head.attrib.get('name')
    print(name)


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



