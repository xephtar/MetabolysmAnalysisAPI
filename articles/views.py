# Create your views here.

# ViewSets define the view behavior.
from rest_framework import viewsets, filters, mixins, generics
from rest_framework.response import Response

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway
from .serializers import ArticleSerializer, AuthorSerializer, MetabolitySerializer, ReactionSerializer, \
    DiseaseSerializer, PathwaySerializer, DiseasePathwaySearchSeriailizer


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
