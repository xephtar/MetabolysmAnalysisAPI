from django.db import models


# Create your models here.

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Author(TimeStampMixin):
    id = models.AutoField(db_column='id', primary_key=True, db_index=True)
    full_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    initials = models.CharField(max_length=10)


class Metabolity(TimeStampMixin):
    metabolity_id = models.CharField(max_length=500, primary_key=True, db_index=True)
    name = models.CharField(max_length=500)
    compartment = models.CharField(max_length=500, null=True)
    notes = models.JSONField(null=True)


class Pathway(TimeStampMixin):
    id = models.AutoField(db_column='id', primary_key=True, db_index=True)
    name = models.CharField(max_length=500, unique=True)


class Disease(TimeStampMixin):
    id = models.AutoField(db_column='id', primary_key=True, db_index=True)
    disease_id = models.CharField(max_length=500, unique=True, db_index=True)
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=500, null=True)
    class_of = models.CharField(max_length=500, null=True)
    semantic_type = models.CharField(max_length=500, null=True)


class Reaction(TimeStampMixin):
    reaction_id = models.CharField(max_length=500, primary_key=True, db_index=True)
    name = models.CharField(max_length=500)
    metabolities = models.ManyToManyField(Metabolity, db_index=True)
    notes = models.JSONField(null=True)
    lower_bound = models.FloatField()
    upper_bound = models.FloatField()
    gene_reaction_rule = models.CharField(max_length=500)


class Article(TimeStampMixin):
    id = models.AutoField(db_column='id', primary_key=True, db_index=True)
    abstract_text = models.CharField(max_length=20000, null=True)
    pub_date = models.DateField()
    name = models.CharField(max_length=500)
    doi = models.CharField(max_length=500, null=True)
    authors = models.ManyToManyField(Author, db_index=True)
    metabolities = models.ManyToManyField(Metabolity, db_index=True)
    diseases = models.ManyToManyField(Disease, db_index=True)
    pathways = models.ManyToManyField(Pathway, db_index=True)
    annotations = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-id']


class PathwayDiseaseRelation(models.Model):
    id = models.AutoField(db_column='id', primary_key=True, db_index=True)
    pathway_name = models.CharField(max_length=500, db_index=True)
    disease_name = models.CharField(max_length=500, db_index=True)
    article_id = models.IntegerField(blank=True, null=True)
    sia_score = models.FloatField(null=True)
    textblob_polarity = models.FloatField(null=True)
    textblob_subjectivity = models.FloatField(null=True)
    flair_score = models.FloatField(null=True)
    sentence = models.CharField(max_length=5000, null=True, db_index=True)

    class Meta:
        ordering = ['pathway_name']
        db_table = 'pathway_disease_relation'
        indexes = [
            models.Index(fields=['pathway_name', 'disease_name', 'article_id', 'sentence']),
        ]
        index_together = [
            ["pathway_name", "disease_name", "article_id", "sentence"],
        ]
        unique_together = [['pathway_name', 'disease_name', 'article_id', 'sentence']]


class EvidenceReport(models.Model):
    pathway_name = models.CharField(max_length=500)
    disease_name = models.CharField(max_length=500)
    evidence_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'evidencereport'


class EvidenceDetail(models.Model):
    pathway_name = models.CharField(max_length=500)
    disease_name = models.CharField(max_length=500)
    total_count = models.IntegerField()
    analyzer_type = models.CharField(max_length=500)

    class Meta:
        managed = False