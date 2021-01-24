"""gproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
from .views import ArticleViewSet, AuthorViewSet, MetabolityViewSet, ReactionViewSet, DiseaseViewSet

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet, basename="article")
router.register(r'authors', AuthorViewSet, basename="author")
router.register(r'metabolities', MetabolityViewSet, basename="metabolity")
router.register(r'reactions', ReactionViewSet, basename="reaction")
router.register(r'diseases', DiseaseViewSet, basename="disease")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
