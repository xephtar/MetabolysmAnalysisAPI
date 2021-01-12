import json
from articles.models import Reaction, Metabolity

# Opening JSON file
f = open('universal_model.json', )

# returns JSON object as
# a dictionary
data = json.load(f)
reactions = data['reactions']
i = 0
for index, m in enumerate(reactions):
    r = Reaction.objects.get_or_create(reaction_id=m['id'], name=m['name'], notes=m['notes'],
                                       upper_bound=m['upper_bound'],
                                       lower_bound=m['lower_bound'], gene_reaction_rule=m['gene_reaction_rule'])
    for met in m['metabolites']:
        r[0].metabolities.add(Metabolity.objects.get(metabolity_id=met))