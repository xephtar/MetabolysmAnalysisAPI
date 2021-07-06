# Serializers define the API representation.
from rest_framework import serializers

from .models import Article, Author, Metabolity, Reaction, Disease, Pathway, EvidenceReport, EvidenceDetail


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
    pathways = PathwaySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'abstract_text', 'pub_date', 'doi', 'authors', 'metabolities', 'diseases', 'pathways', 'annotations']


class ArticleLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'abstract_text', 'pub_date', 'doi', 'annotations']


class PathwayDiseaseRelationSerializer(serializers.Serializer):
    pathway_name = serializers.CharField()
    disease_name = serializers.CharField()
    article_id = serializers.IntegerField()
    sia_score = serializers.FloatField()
    textblob_polarity = serializers.FloatField()
    textblob_subjectivity = serializers.FloatField()
    flair_score = serializers.FloatField()
    sentence = serializers.CharField()


class PathwayEvidenceSerializer(serializers.Serializer):
    pathway_name = serializers.CharField()
    total_count = serializers.IntegerField()


class DiseaseEvidenceSerializer(serializers.Serializer):
    disease_name = serializers.CharField()
    total_count = serializers.IntegerField()


class EvidenceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceReport
        fields = ['pathway_name', 'disease_name', 'evidence_count']


class EvidenceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceDetail
        fields = ['pathway_name', 'disease_name', 'total_count', 'analyzer_type']
