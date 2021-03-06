# Serializers define the API representation.
from rest_framework import serializers

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ["full_name", "first_name", "last_name", "initials", "url"]


class PathwaySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pathway
        fields = ['id', 'name', 'url']


class DiseaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Disease
        fields = ['disease_id', 'name', 'type', 'class_of', "semantic_type", "url"]


class MetabolitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Metabolity
        fields = ['metabolity_id', 'name', 'compartment', 'notes', "url"]


class MetabolitySerializerJustNameUrl(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Metabolity
        fields = ['name', "url"]


class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    metabolities = MetabolitySerializerJustNameUrl(many=True, read_only=True)

    class Meta:
        model = Reaction
        fields = ['reaction_id', 'name', 'metabolities', 'notes', 'lower_bound', 'upper_bound', 'gene_reaction_rule', "url"]


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    metabolities = MetabolitySerializer(many=True, read_only=True)
    diseases = DiseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'abstract_text', 'pub_date', 'doi', 'authors', 'metabolities', 'diseases', 'url']
