import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType

from posts.models import Article


class ArticleType(DjangoObjectType):

    class Meta:
        model = Article


class Query(graphene.ObjectType):

    articles = graphene.List(ArticleType, title=graphene.String())

    def resolve_articles(self, info, **kwargs):
        # 這裡可以定義 query 方式
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

    class Arguments:
        article_data = ArticleInput()

    message = graphene.String()
    article = graphene.Field(ArticleType)

    def mutate(self, info, article_data):
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
