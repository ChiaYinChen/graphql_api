"""Django views for graphql_api project."""
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView as BaseGraphQLView

from users.models import User


class GraphQLView(BaseGraphQLView):
    """Extend GraphQLView."""

    @staticmethod
    def format_error(error):
        """Customize json response for an error in graphql."""
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)
        try:
            formatted_error['status'] = error.original_error.status
        except AttributeError:
            pass
        return formatted_error


class ActivateAccountView(TemplateView):
    """Account Activation With Email Verification."""

    def get(self, request, *args, **kwargs):
        """Activate the user account."""
        username = kwargs.get('username')
        if username:
            user = User.objects.get(username=username)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect('graphql')
            else:
                return HttpResponse('Email address has already been verified.')
