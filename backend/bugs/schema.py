import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Bug
from tags.models import Tag


class UserType(DjangoObjectType):
    class Meta:
        model = User


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class BugType(DjangoObjectType):
    class Meta:
        model = Bug


class Query(object):
    all_bugs = graphene.List(BugType, search=graphene.String())

    def resolve_all_bugs(self, info, search=None):
        status = {"resolved": True, "unresolved": False}
        if search:
            if search not in status:
                filtered_bugs = Bug.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(created_by__username__icontains=search) |
                    Q(assigned_to__username__icontains=search) |
                    Q(tag__name__icontains=search)
                )
            else:
                filtered_bugs = Bug.objects.filter(
                    resolved=status[search]
                )
            return filtered_bugs

        return Bug.objects.all()


class CreateBug(graphene.Mutation):
    bug = graphene.Field(BugType)

    class Arguments():
        title = graphene.String()
        description = graphene.String()
        assigned_to = graphene.String()

    def mutate(self, info, **kwargs):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("You must be loged-in to create a bug")
        created_by = current_user
        assigned_to_username = kwargs.get("assigned_to", current_user)
        assigned_to = User.objects.get(username=assigned_to_username)
        title = kwargs.get("title")
        description = kwargs.get("description")
        bug = Bug.objects.create(
            title=title, description=description, created_by=created_by)
        bug.assigned_to.add(assigned_to)
        bug.save()

        return CreateBug(bug=bug)


class UpdateBug(graphene.Mutation):
    bug = graphene.Field(BugType)

    class Arguments():
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        assigned_to = graphene.List(graphene.String)

    def mutate(self, info, **kwargs):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("You must be loged-in to update a bug")
        id = kwargs.get("id")
        bug = Bug.objects.get(pk=id)
        if bug.created_by != current_user:
            raise Exception("Only original author allowed to update the bug")

        assigned_to_usernames = kwargs.get("assigned_to")
        assigned_to = []
        for name in assigned_to_usernames:
            new = User.objects.filter(username=name)
            assigned_to.append(*new)

        title = kwargs.get("title")
        description = kwargs.get("description")
        bug.title = title
        bug.description = description
        bug.assigned_to.add(*assigned_to)
        bug.save()

        return UpdateBug(bug=bug)


class DeleteBug(graphene.Mutation):
    id = graphene.ID()

    class Arguments():
        id = graphene.ID()

    def mutate(self, info, id):
        current_user = info.context.user

        bug = Bug.objects.get(pk=id)
        if bug.created_by != current_user:
            raise Exception("Only original author allowed to update the bug")

        bug.delete()
        return DeleteBug(id=id)


class Mutation(graphene.ObjectType):
    create_bug = CreateBug.Field()
    update_bug = UpdateBug.Field()
    delete_bug = DeleteBug.Field()
