# Create your views here.

# ViewSets define the view behavior.
from django.db.models import F, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, filters, mixins, generics
from rest_framework.response import Response

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway
from .serializers import ArticleSerializer, AuthorSerializer, MetabolitySerializer, ReactionSerializer, \
    DiseaseSerializer, PathwaySerializer, DiseasePathwaySearchSeriailizer
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SingleArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.exclude(Q(annotations__isnull=False)).exclude(Q(abstract_text__exact='')).all()[:1]
    serializer_class = ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    search_fields = ['abstract_text', 'diseases__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Article.objects.prefetch_related('metabolities', 'authors', 'diseases', 'pathways').all()
    serializer_class = ArticleSerializer

    #@method_decorator(cache_page(CACHE_TTL))
    #def list(self, *args, **kwargs):
    #    return super().list(*args, **kwargs)


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


class DiseasePathwaySearchViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = DiseasePathwaySearchSeriailizer
    queryset = ''

    def get(self, request, *args, **kwargs):
        disease_name = request.query_params.get('disease', '-1')
        pathway_name = request.query_params.get('pathway', '-1')

        pathways = Pathway.objects.filter(name__icontains=pathway_name).distinct()
        diseases = Disease.objects.filter(name__icontains=disease_name).distinct()

        serialized_pathways = PathwaySerializer(pathways, many=True,
                                                context={'request': request}).data

        serialized_diseases = DiseaseSerializer(diseases, many=True,
                                                context={'request': request}).data

        articlesWithPathway = Article.objects.filter(
            pathways__in=pathways)
        articlesWithDisease = Article.objects.filter(
            diseases__in=diseases)

        related_diseases = Disease.objects.filter(article__in=articlesWithPathway)
        related_pathways = Pathway.objects.filter(article__in=articlesWithDisease)

        serialized_pathways_data = PathwaySerializer(related_pathways, many=True,
                                                     context={'request': request}).data
        serialized_disease_data = DiseaseSerializer(related_diseases, many=True,
                                                    context={'request': request}).data

        res = {
            'disease_info': {'tagged_article_count': len(articlesWithDisease),
                             'diseases': {'count': len(serialized_diseases), 'results': serialized_diseases},
                             'related_pathways': {'count': len(serialized_pathways_data),
                                                  'results': serialized_pathways_data}},
            'pathway_info': {'tagged_article_count': len(articlesWithPathway),
                             'pathways': {'count': len(serialized_pathways), 'results': serialized_pathways},
                             'related_diseases': {'count': len(serialized_disease_data),
                                                  'results': serialized_disease_data}}}

        return Response(data=res)
