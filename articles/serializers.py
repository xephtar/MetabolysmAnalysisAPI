# Serializers define the API representation.
from rest_framework import serializers

from .models import Article, Author, Metabolity, Reaction


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ["full_name", "first_name", "last_name", "initials", "url"]


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
        fields = ['reaction_id', 'name', 'metabolities', 'notes', 'lower_bound', 'upper_bound', 'gene_reaction_rule']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    metabolities = MetabolitySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['name', 'abstract_text', 'pub_date', 'doi', 'authors', 'metabolities']