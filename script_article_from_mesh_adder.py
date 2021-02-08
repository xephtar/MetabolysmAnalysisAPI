from xml.dom import minidom

# parse an xml file by name
mydoc = minidom.parse('pubmed21n0001.xml')
articles = mydoc.getElementsByTagName('PubmedArticle')
print(articles[1].firstChild.data)
