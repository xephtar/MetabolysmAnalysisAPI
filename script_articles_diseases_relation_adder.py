from articles.models import Article, Disease

all_articles = Article.objects.all()
all_diseases = Disease.objects.all()

i = 0
for ar in all_articles:
    if i > 2565:
        abstractText = ar.abstract_text.lower()
        for me in all_diseases:
            nameOfDisease = me.name.lower()
            if nameOfDisease != "":
                print(nameOfDisease)
                if nameOfDisease in abstractText:
                    ar.diseases.add(me)
    i += 1