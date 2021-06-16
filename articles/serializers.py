# Serializers define the API representation.
from rest_framework import serializers

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["full_name", "first_name", "last_name", "initials"]


class PathwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathway
        fields = ['id', 'name']


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ['disease_id', 'name', 'type', 'class_of', "semantic_type"]


class MetabolitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Metabolity
        fields = ['metabolity_id', 'name', 'compartment', 'notes']


class MetabolitySerializerJustNameUrl(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metabolity
        fields = ['name', "url"]


class ReactionSerializer(serializers.ModelSerializer):
    metabolities = MetabolitySerializerJustNameUrl(many=True, read_only=True)

    class Meta:
        model = Reaction
        fields = ['reaction_id', 'name', 'metabolities', 'notes', 'lower_bound', 'upper_bound', 'gene_reaction_rule']


class ArticleSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    metabolities = MetabolitySerializerJustNameUrl(many=True, read_only=True)
    diseases = DiseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'abstract_text', 'pub_date', 'doi', 'authors', 'metabolities', 'diseases', 'annotations']


class DiseasePathwaySearchSeriailizer(serializers.Serializer):
    disease = serializers.CharField(max_length=500)
    pathway = serializers.CharField(max_length=500)
