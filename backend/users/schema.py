import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    current_user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get("id")
        if(id):
            return User.objects.get(pk=id)

    def resolve_current_user(self, info):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("Please log in")
        return current_user

    def resolve_all_users(self, info, **kwargs):

        return User.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments():
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User.objects.create(
            username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
