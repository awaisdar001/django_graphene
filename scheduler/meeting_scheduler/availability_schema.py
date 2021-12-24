import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from scheduler.meeting_scheduler.models import Availability
from scheduler.meeting_scheduler.user_schema import UserType


class AvailabilityNode(DjangoObjectType):
    """Availability Object Type Definition"""
    id = graphene.ID()
    interval_mints = graphene.String()
    user = graphene.Field(UserType)

    class Meta:
        model = Availability

    def resolve_interval_mints(self, info):
        """Resolves interval mints choice field."""
        return self.get_interval_mints_display()


class CreateAvailability(graphene.Mutation):
    """
    OTD mutation class for creating user availabilities.
    """
    availability = graphene.Field(AvailabilityNode)
    success = graphene.Boolean()

    class Arguments:
        """Defines the arguments the mutation can take."""
        from_time = graphene.DateTime()
        to_time = graphene.DateTime()
        time_interval_mints = graphene.Int()

    def mutate(cls, info, from_time, to_time, time_interval_mints):
        """Mutate operation creating user availability in the system."""
        user = info.context.user
        availability = Availability.objects.create(
            user=user,
            from_time=from_time,
            to_time=to_time,
            interval_mints=time_interval_mints
        )
        return CreateAvailability(availability=availability, success=True)


class UpdateAvailability(graphene.Mutation):
    """
    OTD mutation class for updating user availabilities.
    """
    availability = graphene.Field(AvailabilityNode)
    success = graphene.Boolean()

    class Arguments:
        """Defines the arguments the mutation can take."""
        id = graphene.Int(required=True)
        from_time = graphene.DateTime()
        to_time = graphene.DateTime()
        time_interval_mints = graphene.Int()

    def mutate(self, info, id, **kwargs):
        """mutate operation updating user availability in the system."""
        try:
            availability = Availability.objects.get(id=id, user=info.context.user)
        except Availability.DoesNotExist:
            raise GraphQLError(f"This ID:{id} doesn't seem to be belong you")

        for key, value in kwargs.items():
            setattr(availability, key, value)
        availability.save()
        success = True
        return UpdateAvailability(availability=availability, success=success)


class DeleteAvailability(graphene.Mutation):
    """
    OTD mutation class for deleting user availabilities.
    """
    success = graphene.Boolean()

    class Arguments:
        """Defines the arguments the mutation can take."""
        id = graphene.ID()

    def mutate(self, info, **kwargs):
        """Mutate operation deleting user availability in the system."""
        obj = Availability.objects.get(pk=kwargs["id"])
        obj.delete()
        return DeleteAvailability(success=True)


class Query(graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the user availability Schema.
    """
    availabilities = graphene.List(AvailabilityNode)
    availability = graphene.Field(AvailabilityNode, id=graphene.Int(required=True))

    def resolve_availabilities(self, info):
        """Resolve the user availabilities List"""
        return Availability.objects.filter(user=info.context.user)

    def resolve_availability(self, info, id):
        """Resolve the user availability field"""
        return Availability.objects.get(id=id, user=info.context.user)


class Mutation(graphene.ObjectType):
    """
    Describes entry point for fields to *create, update or delete* data in availability API.
    """
    create_availability = CreateAvailability.Field()
    update_availability = UpdateAvailability.Field()
    delete_availability = DeleteAvailability.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
