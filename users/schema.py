from django.contrib.auth.models import User
import graphene
from graphene_django.types import DjangoObjectType
from graphql_api.utils import APIException


class UserType(DjangoObjectType):

    class Meta:
        model = User


class Query(graphene.ObjectType):

    users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String())

    def resolve_users(self, info, **kwargs):
        breakpoint()
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            return user
        return APIException('User not found.', status=404)


class UserInput(graphene.InputObjectType):

    username = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(graphene.Mutation):

    class Arguments:
        user_data = UserInput()

    message = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, **kwargs):
        data = kwargs.get('user_data', {})
        username = data.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            return CreateUser(message='User already exist', user=user)
            # return APIException('User already exist.', status=404)
        user = User(**data)
        user.set_password(data.get('password'))
        user.save()
        return CreateUser(message='Successfully created user', user=user)


class UpdateUser(graphene.Mutation):

    class Arguments:
        user_data = UserInput()

    message = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, **kwargs):
        data = kwargs.get('user_data', {})
        username = data.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            user.set_password(data.get('password'))
            user.save()
            return UpdateUser(message='Successfully updated user', user=user)
        else:
            return UpdateUser(message='User not found')


class DeleteUser(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)

    message = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            user.delete()
            return DeleteUser(message='User deleted', user=user)
        else:
            return DeleteUser(message='User not found')
            # return APIException('User not found.', status=404)


class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
