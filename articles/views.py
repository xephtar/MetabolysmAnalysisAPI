# Create your views here.

# ViewSets define the view behavior.
from django.db import connection
from django.db.models import F, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, filters, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway, PathwayDiseaseRelation, EvidenceReport
from .serializers import ArticleSerializer, AuthorSerializer, MetabolitySerializer, ReactionSerializer, \
    DiseaseSerializer, PathwaySerializer, ArticleLightSerializer, PathwayDiseaseRelationSerializer, \
    EvidenceReportSerializer, PathwayEvidenceSerializer, DiseaseEvidenceSerializer, EvidenceDetailSerializer
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class GetRelation(ViewSet):
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, format=None):
        serialized_a = None
        serialized_b = None
        percent = '%'
        if self.request.query_params.get('pathway'):
            pathway = self.request.query_params.get('pathway')
            with connection.cursor() as cursor:
                cursor.execute("SELECT e.pathway_name, count(*) as total_count FROM evidencereport as e where e.pathway_name ilike %s group by e.pathway_name order by total_count desc limit 5", [percent+pathway+percent])
                serialized_a = PathwayEvidenceSerializer(dictfetchall(cursor), many=True).data

        if self.request.query_params.get('disease'):
            disease = self.request.query_params.get('disease')
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT e.disease_name, count(*) as total_count FROM evidencereport as e where e.disease_name ilike %s group by e.disease_name order by total_count desc limit 5",
                    [percent + disease + percent])
                serialized_b = DiseaseEvidenceSerializer(dictfetchall(cursor), many=True).data

        res = {'pathway_information': serialized_a, 'disease_information': serialized_b}
        return Response(data=res)


class GetPathwayRelationDetail(ViewSet):
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, format=None):
        list = []
        if self.request.query_params.get('pathway'):
            pathway = self.request.query_params.get('pathway')
            totalLimit = 5
            with connection.cursor() as cursor:
                cursor.execute("select disease_name, pathway_name, total_count, analyzer_type from evidenceneutrealdetail e where e.pathway_name = %s order by e.analyzer_type, e.total_count desc ", [pathway])
                neutreal_detail = EvidenceDetailSerializer(dictfetchall(cursor), many=True).data
                cursor.execute("select disease_name, pathway_name, total_count, analyzer_type from evidencepositivedetail e where e.pathway_name = %s order by e.analyzer_type, e.total_count desc ", [pathway])
                positive_detail = EvidenceDetailSerializer(dictfetchall(cursor), many=True).data
                cursor.execute("select disease_name, pathway_name, total_count, analyzer_type from evidencenegativedetail e where e.pathway_name = %s order by e.analyzer_type, e.total_count desc ", [pathway])
                negative_detail = EvidenceDetailSerializer(dictfetchall(cursor), many=True).data

                detailList = [neutreal_detail, positive_detail, negative_detail]

                d = {}
                for detail in detailList:
                    for dictionary in detail:
                        for k, v in dictionary.items():
                            if k == 'disease_name':
                                atype = dictionary['analyzer_type']
                                count = dictionary['total_count']
                                dic = {atype: count}
                                if v not in d:
                                    d[v] = dic
                                else:
                                    d[v].update(dic)

                pos = 'positive'
                neg = 'negative'
                neutreal = 'neutreal'
                sia = 'sia'
                flair = 'flair'
                textblob = 'textblob'
                totalEvidence = 'totalEvidence'

                for k, v in d.items():
                    detail = v
                    detailByModel = {flair: {pos: 0, neg: 0, neutreal: 0}, sia: {pos: 0, neg: 0, neutreal: 0}, textblob: {pos: 0, neg: 0, neutreal: 0}, totalEvidence: 0}
                    for t, z in detail.items():
                        if neutreal in t:
                            if sia in t:
                                detailByModel[sia][neutreal] = z
                            elif textblob in t:
                                detailByModel[textblob][neutreal] = z
                            elif flair in t:
                                detailByModel[flair][neutreal] = z
                        elif pos in t:
                            if sia in t:
                                detailByModel[sia][pos] = z
                            elif textblob in t:
                                detailByModel[textblob][pos] = z
                            elif flair in t:
                                detailByModel[flair][pos] = z
                        elif neg in t:
                            if sia in t:
                                detailByModel[sia][neg] = z
                            elif textblob in t:
                                detailByModel[textblob][neg] = z
                            elif flair in t:
                                detailByModel[flair][neg] = z
                    detailByModel[totalEvidence] = detailByModel[flair][neg] + detailByModel[flair][pos] + detailByModel[flair][neutreal]
                    list.append({'disease': k, 'data': detailByModel})
                print(list)

        if len(list) == 0:
            return Response(data={"error": "pathway query parameter is not given!"})

        return Response(data=list)


class GetDiseaseRelationDetail(ViewSet):
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, format=None):
        list = []
        if self.request.query_params.get('disease'):
            disease = self.request.query_params.get('disease')
            totalLimit = 5
            with connection.cursor() as cursor:
                cursor.execute(
                    "select disease_name, pathway_name, total_count, analyzer_type from evidenceneutrealdetail e where e.disease_name = %s order by e.analyzer_type, e.total_count desc ",
                    [disease])
                neutreal_detail = EvidenceDetailSerializer(dictfetchall(cursor), many=True).data
                cursor.execute(
                    "select disease_name, pathway_name, total_count, analyzer_type from evidencepositivedetail e where e.disease_name = %s order by e.analyzer_type, e.total_count desc ",
                    [disease])
                positive_detail = EvidenceDetailSerializer(dictfetchall(cursor), many=True).data
                cursor.execute(
                    "select disease_name, pathway_name, total_count, analyzer_type from evidencenegativedetail e where e.disease_name = %s order by e.analyzer_type, e.total_count desc ",
                    [disease])
                negative_detail = EvidenceDetailSerializer(dictfetchall(cursor), many=True).data

                detailList = [neutreal_detail, positive_detail, negative_detail]

                d = {}
                for detail in detailList:
                    for dictionary in detail:
                        for k, v in dictionary.items():
                            if k == 'pathway_name':
                                atype = dictionary['analyzer_type']
                                count = dictionary['total_count']
                                dic = {atype: count}
                                if v not in d:
                                    d[v] = dic
                                else:
                                    d[v].update(dic)

                pos = 'positive'
                neg = 'negative'
                neutreal = 'neutreal'
                sia = 'sia'
                flair = 'flair'
                textblob = 'textblob'
                totalEvidence = 'totalEvidence'

                for k, v in d.items():
                    detail = v
                    detailByModel = {flair: {pos: 0, neg: 0, neutreal: 0}, sia: {pos: 0, neg: 0, neutreal: 0},
                                     textblob: {pos: 0, neg: 0, neutreal: 0}, totalEvidence: 0}
                    for t, z in detail.items():
                        if neutreal in t:
                            if sia in t:
                                detailByModel[sia][neutreal] = z
                            elif textblob in t:
                                detailByModel[textblob][neutreal] = z
                            elif flair in t:
                                detailByModel[flair][neutreal] = z
                        elif pos in t:
                            if sia in t:
                                detailByModel[sia][pos] = z
                            elif textblob in t:
                                detailByModel[textblob][pos] = z
                            elif flair in t:
                                detailByModel[flair][pos] = z
                        elif neg in t:
                            if sia in t:
                                detailByModel[sia][neg] = z
                            elif textblob in t:
                                detailByModel[textblob][neg] = z
                            elif flair in t:
                                detailByModel[flair][neg] = z
                    detailByModel[totalEvidence] = detailByModel[flair][neg] + detailByModel[flair][pos] + \
                                                   detailByModel[flair][neutreal]
                    list.append({'pathway': k, 'data': detailByModel})

        if len(list) == 0:
            return Response(data={"error": "disease query parameter is not given!"})

        return Response(data=list)


class SingleArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.exclude(Q(annotations__isnull=False)).exclude(Q(abstract_text__exact='')).all()[:1]
    serializer_class = ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    search_fields = ['abstract_text', 'diseases__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Article.objects.prefetch_related('metabolities', 'authors', 'diseases', 'pathways').all()
    serializer_class = ArticleSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

class PathwayViewSet(viewsets.ModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Pathway.objects.all()
    serializer_class = PathwaySerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

class DiseaseViewSet(viewsets.ModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

class MetabolityViewSet(viewsets.ModelViewSet):
    queryset = Metabolity.objects.all()
    serializer_class = MetabolitySerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)