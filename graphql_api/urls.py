"""Graphql api URL Configuration."""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ActivateAccountView, GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'graphql/',
        csrf_exempt(GraphQLView.as_view(graphiql=True)),
        name='graphql'
    ),
    path(
        'activate/<username>/',
        ActivateAccountView.as_view(),
        name='activate'
    ),
]
