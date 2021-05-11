from xml.dom import minidom

# parse an xml file by name
mydoc = minidom.parse('pubmed21n0002.xml')
articles = mydoc.getElementsByTagName('PubmedArticle')
print(articles[1].firstChild.data)

# import xml.etree.ElementTree as ET
#
# tree = ET.parse('pubmed21n0002.xml')
# root = tree.getroot()
#
# # all items data
# print('PubMed Data:')
#
# for elem in root:
#     for subelem in elem:
#         print(subelem.text)


# xpath language
# xml query language
# minidom xpath uyumuna bak
