import requests
import xmltodict, json
from articles.models import Article, Metabolity

all_articles = Article.objects.all()
all_metabolities = Metabolity.objects.all()

i = 0
for ar in all_articles:
    abstractText = ar.abstract_text.lower()
    for me in all_metabolities:
        nameOfMetabolity = me.name.lower()
        if nameOfMetabolity != "":
            print(nameOfMetabolity)
            if nameOfMetabolity in abstractText:
                ar.metabolities.add(me)
    i += 1
