import os
import datetime
import xml.etree.ElementTree as et

# Open the xml and get the root element
tree = et.parse('movies.xml')
# Get the root element
root = tree.getroot()

print(root.tag)
print(root.attrib)

for child in root:
    print(child.tag, child.attrib)
# root.iter() : Itereates over all child elements & subchild

all_tags = [elem.tag for elem in root.iter()]
print(type(all_tags))
print(len(all_tags))

# print(et.tostring(root, encoding='utf8').decode('utf8'))
for movie in root.iter('movie'):
    print(movie.attrib)


