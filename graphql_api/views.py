from graphene_django.views import GraphQLView as BaseGraphQLView


class GraphQLView(BaseGraphQLView):

    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)
        try:
            formatted_error['status'] = error.original_error.status
        except AttributeError:
            pass
        return formatted_error
