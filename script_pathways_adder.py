import json
from articles.models import Pathway

# Opening JSON file
f = open('Recon3D.json', )

# returns JSON object as
# a dictionary
data = json.load(f)
reactions = data['reactions']
i = 0
for index, m in enumerate(reactions):
    name = m['subsystem']
    if 'exchange' not in name:
        Pathway.objects.get_or_create(name=name)
    i += 1

# Using readlines()
file1 = open('biocycpathways.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
for line in Lines:
    if count != 0:
        name = line.split('\n')
        Pathway.objects.get_or_create(name=name[0])
    count += 1


# Opening JSON file
f = open('br08901.json', )

# returns JSON object as
# a dictionary
data = json.load(f)
reactions = data['reactions']
i = 0
for index, m in enumerate(reactions):
    name = m['subsystem']
    if 'exchange' not in name:
        Pathway.objects.get_or_create(name=name)
    i += 1
