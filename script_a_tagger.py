from articles.models import Article
from textblob import TextBlob
import json

all_articles = Article.objects.all()
tagged = []
i = 0
for ar in all_articles:
    abstractText = ar.abstract_text.lower()
    t = TextBlob(abstractText)
    jsont = json.dumps(t.tags)
    tagged.append(jsont)
    print(i)
    i += 1

for index, ar in enumerate(all_articles):
    if index > 1:
        continue
    try:
        a = Article.objects.get(pk=ar.pk)
        print(a.tagged)
    except:
        print('none')
    print(index)
