import requests
import xmltodict, json
from articles.models import Article, Author

url = "https://www.ebi.ac.uk/europepmc/webservices/rest/searchPOST?query=cancer&resultType=core&pageSize=1000"

payload = {}
files = {}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

o = xmltodict.parse(response.text)
json.dumps(o)
i = 0

for m in o['responseWrapper']['resultList']['result']:
    print(i)
    i += 1
    try:
        if 'abstractText' in m.keys():
            if 'doi' in m.keys():
                ar = Article.objects.get_or_create(abstract_text=m['abstractText'], pub_date=m['firstPublicationDate'],
                                                   name=m['title'], doi=m['doi'])
            else:
                ar = Article.objects.get_or_create(abstract_text=m['abstractText'], pub_date=m['firstPublicationDate'],
                                                   name=m['title'])
            aus = []
            for a in m['authorList']['author']:
                au = Author.objects.get_or_create(full_name=a['fullName'], first_name=a['firstName'],
                                                  last_name=a['lastName'], initials=a['initials'])
                ar[0].authors.add(au[0])
    except:
        print("e")
    else:
        print("else")
