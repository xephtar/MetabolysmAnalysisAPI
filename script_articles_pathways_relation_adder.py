from articles.models import Article, Pathway

all_articles = Article.objects.all()
all_pathways = Pathway.objects.all()

i = 0
for ar in all_articles:
    abstractText = ar.abstract_text.lower()
    for me in all_pathways:
        nameOfPathway = me.name.lower()
        if nameOfPathway != "":
            print(nameOfPathway)
            if nameOfPathway in abstractText:
                ar.pathways.add(me)
    i += 1