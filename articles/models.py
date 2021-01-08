from django.db import models


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    initials = models.CharField(max_length=10)


class Article(models.Model):
    abstract_text = models.CharField(max_length=5000, null=True)
    pub_date = models.DateField()
    name = models.CharField(max_length=500)
    doi = models.CharField(max_length=500, null=True)
    authors = models.ManyToManyField(Author)


class Metabolity(models.Model):
    metabolity_id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500)
    compartment = models.CharField(max_length=500, null=True)
    notes = models.JSONField(null=True)
