import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery
from graphql_auth.mutations import ObtainJSONWebToken

from scheduler.meeting_scheduler.models import UserModel


class UserType(DjangoObjectType):
    """User Object Type Definition"""

    class Meta:
        model = UserModel
        fields = ("id", "username")


class Query(UserQuery, graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the user Schema.
    """
    pass

class Mutation(graphene.ObjectType):
    login = ObtainJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
