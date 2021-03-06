from django.db import models


# Create your models here.

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Author(TimeStampMixin):
    full_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    initials = models.CharField(max_length=10)


class Metabolity(TimeStampMixin):
    metabolity_id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500)
    compartment = models.CharField(max_length=500, null=True)
    notes = models.JSONField(null=True)


class Pathway(TimeStampMixin):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=500, unique=True)


class Disease(TimeStampMixin):
    id = models.AutoField(db_column='id', primary_key=True)
    disease_id = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=500, null=True)
    class_of = models.CharField(max_length=500, null=True)
    semantic_type = models.CharField(max_length=500, null=True)


class Reaction(TimeStampMixin):
    reaction_id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500)
    metabolities = models.ManyToManyField(Metabolity)
    notes = models.JSONField(null=True)
    lower_bound = models.FloatField()
    upper_bound = models.FloatField()
    gene_reaction_rule = models.CharField(max_length=500)


class Article(TimeStampMixin):
    abstract_text = models.CharField(max_length=5000, null=True)
    pub_date = models.DateField()
    name = models.CharField(max_length=500)
    doi = models.CharField(max_length=500, null=True)
    authors = models.ManyToManyField(Author)
    metabolities = models.ManyToManyField(Metabolity)
    diseases = models.ManyToManyField(Disease)
    pathways = models.ManyToManyField(Pathway)
