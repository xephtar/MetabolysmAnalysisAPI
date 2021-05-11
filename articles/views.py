import json

from django.shortcuts import render

# Create your views here.

# ViewSets define the view behavior.
from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway
from .serializers import ArticleSerializer, AuthorSerializer, MetabolitySerializer, ReactionSerializer, \
    DiseaseSerializer, PathwaySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    search_fields = ['abstract_text', 'diseases__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Article.objects.all().order_by('-pk')
    serializer_class = ArticleSerializer

    # @action(methods=['get'], detail=False, serializer_class=ArticleSerializer)
    # def findArticlesForGivenDiseaseName(self, request, **kwargs):
    #     empty_params = []
    #     for param in ['disease_name']:
    #         if param not in request.data.keys():
    #             empty_params.append({param: "This field should not be left empty."})
    #
    #     if len(empty_params) > 0:
    #         raise serializers.ValidationError(empty_params)
    #
    #     disease_name = request.data['disease_name']
    #     queryset = self.get_queryset().filter(diseases__name__contains=disease_name)
    #     paginator = PageNumberPagination()
    #     paginator.page_size = 5
    #     result_page = paginator.paginate_queryset(queryset, request)
    #     serializer = self.get_serializer(result_page, many=True)
    #     return paginator.get_paginated_response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PathwayViewSet(viewsets.ModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Pathway.objects.all()
    serializer_class = PathwaySerializer


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
