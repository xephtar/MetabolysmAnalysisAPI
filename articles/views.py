from django.shortcuts import render


# Create your views here.

# ViewSets define the view behavior.
from rest_framework import viewsets

from .models import Article, Author, Metabolity, Reaction
from .serializers import ArticleSerializer, AuthorSerializer, MetabolitySerializer, ReactionSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class MetabolityViewSet(viewsets.ModelViewSet):
    queryset = Metabolity.objects.all()
    serializer_class = MetabolitySerializer


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer