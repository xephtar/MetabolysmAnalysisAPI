# Serializers define the API representation.
from rest_framework import serializers

from .models import Article, Author, Metabolity


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ["full_name", "first_name", "last_name", "initials", "url"]


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['name', 'abstract_text', 'pub_date', 'doi', 'authors']


class MetabolitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Metabolity
        fields = ['metabolity_id', 'name', 'compartment', 'notes']
