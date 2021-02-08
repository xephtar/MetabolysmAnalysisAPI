import json
from articles.models import Metabolity

# Opening JSON file
f = open('universal_model.json', )

# returns JSON object as
# a dictionary
data = json.load(f)
metabolities = data['metabolites']

for index, m in enumerate(metabolities):
    Metabolity.objects.get_or_create(metabolity_id=m['id'], name=m['name'], compartment=m['compartment'], notes=m['notes'])
