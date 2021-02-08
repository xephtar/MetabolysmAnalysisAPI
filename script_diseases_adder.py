import csv
from articles.models import Disease

i = 0

with open("all_gene_disease_associations.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    columns = []
    for row in rd:
        if i != 0 and i > 1100030:
            d = Disease.objects.get_or_create(disease_id=row[4], name=row[5], type=row[6],
                                              class_of=row[7],
                                              semantic_type=row[8])
            print(d)
        i += 1
