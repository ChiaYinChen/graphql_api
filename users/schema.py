import graphene
from django.contrib.auth import authenticate
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import superuser_required
from graphql_jwt.utils import jwt_encode, jwt_payload

from graphql_api.utils import APIException
from users.models import User
from users.send import send_confirmation_email


class UserType(DjangoObjectType):

    class Meta:
        model = User
        exclude = ('password',)


class Query(graphene.ObjectType):

    users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String())

    @superuser_required
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            return user
        return APIException('User not found', status=404)


class UserInput(graphene.InputObjectType):

    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String()


class CreateUser(graphene.Mutation):

    class Arguments:
        user_data = UserInput()

    message = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, **kwargs):
        data = kwargs.get('user_data', {})
        username = data.get('username')
        email = data.get('email')
        if not email:
            return APIException('Email required', status=404)
        user = User.objects.filter(username=username).first()
        if user:
            return CreateUser(message='User already exist', user=user)
        user = User(**data)
        user.set_password(data.get('password'))
        user.save()
        send_confirmation_email(email=user.email, username=user.username)
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


class LoginUser(graphene.Mutation):

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()

    def mutate(self, info, **kwargs):
        user = authenticate(
            username=kwargs.get('email'),
            password=kwargs.get('password')
        )
        error_message = 'Invalid login credentials.'
        success_message = "You logged in successfully."
        if user:
            payload = jwt_payload(user)
            token = jwt_encode(payload)
            return LoginUser(token=token, message=success_message)
        return LoginUser(message=error_message)


class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login_user = LoginUser.Field()
