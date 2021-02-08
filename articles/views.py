from django.shortcuts import render

# Create your views here.

# ViewSets define the view behavior.
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Author, Metabolity, Reaction, Disease
from .serializers import ArticleSerializer, AuthorSerializer, MetabolitySerializer, ReactionSerializer, \
    DiseaseSerializer


def addTwoNumber(a, b):
    return int(a) + int(b)


class MyView(APIView):
    def post(self, request, *args, **kwargs):
        my_result = addTwoNumber(request.data.get('firstnum'), request.data.get('secondnum'))
        return Response(data={"my_return_data": my_result})


class ArticleViewSet(viewsets.ModelViewSet):
    search_fields = ['abstract_text']
    filter_backends = (filters.SearchFilter,)
    queryset = Article.objects.all().order_by('pk')
    serializer_class = ArticleSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class DiseaseViewSet(viewsets.ModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer


class MetabolityViewSet(viewsets.ModelViewSet):
    queryset = Metabolity.objects.all()
    serializer_class = MetabolitySerializer


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
