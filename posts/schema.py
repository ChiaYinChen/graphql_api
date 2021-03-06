"""Graphql schema for article API."""
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from graphql_api.utils import APIException
from posts.models import Article
from users.models import User


class ArticleType(DjangoObjectType):

    class Meta:
        model = Article


class Query(graphene.ObjectType):
    """Get article list."""

    articles = graphene.List(ArticleType, title=graphene.String())

    @login_required
    def resolve_articles(self, info, **kwargs):
        title = kwargs.get('title')
        if title is not None:
            return Article.objects.filter(title__contains=title)
        return Article.objects.all()


class ArticleInput(graphene.InputObjectType):

    title = graphene.String()
    author = graphene.String(required=True)
    content = graphene.String()
    url = graphene.String()


class CreateArticle(graphene.Mutation):
    """Create a article by username."""

    class Arguments:
        article_data = ArticleInput()

    message = graphene.String()
    article = graphene.Field(ArticleType)

    @login_required
    def mutate(self, info, article_data):
        if info.context.user.username != article_data.author:
            return APIException('Please use the right token', status=404)
        user = User.objects.filter(username=article_data.author).first()
        if not user:
            return CreateArticle(message='User not found')
        article = Article(
            title=article_data.title,
            author=user,
            content=article_data.content,
            url=article_data.url
        )
        article.save()
        return CreateArticle(
            message='Post success',
            article=article
        )


class Mutation(graphene.ObjectType):

    create_article = CreateArticle.Field()
