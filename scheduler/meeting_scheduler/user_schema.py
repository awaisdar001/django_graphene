import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.mutations import ObtainJSONWebToken
from graphql_auth.schema import UserQuery

from scheduler.meeting_scheduler.models import UserModel


class UserType(DjangoObjectType):
    """User Object Type Definition"""

    class Meta:
        model = UserModel
        fields = ("id", "username", "email")


class Query(UserQuery, graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the user Schema.
    """
    pass


class Mutation(graphene.ObjectType):
    login = mutations.ObtainJSONWebToken.Field(description="Login and obtain token for the user")
    verify_token = mutations.VerifyToken.Field(description="Verify if the token is valid.")


schema = graphene.Schema(query=Query, mutation=Mutation)
