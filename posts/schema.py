import graphene
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
    content = graphene.String()
    url = graphene.String()


class CreateArticle(graphene.Mutation):

    # 請求提交的參數
    class Arguments:
        article_data = ArticleInput()

    # 返回的資料
    success = graphene.Boolean()
    article = graphene.Field(ArticleType)

    # 建立 article 的邏輯
    def mutate(self, info, article_data):
        article = Article(
            title=article_data.title,
            content=article_data.content,
            url=article_data.url
        )
        article.save()
        return CreateArticle(article=article, success=True)


class Mutation(graphene.ObjectType):

    create_article = CreateArticle.Field()
