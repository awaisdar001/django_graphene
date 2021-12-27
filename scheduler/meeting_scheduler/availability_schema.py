import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from scheduler.meeting_scheduler.models import Availability
from scheduler.meeting_scheduler.user_schema import UserType


class Description:
    """Verbose descriptions for availability fields. """
    availability_from = "Provide iso datetime for the start of the availability e.g. 2022-08-17T09:00:00"
    availability_to = "Provide iso datetime for your availability limit e.g. 2022-08-17T06:00:00"
    time_interval = "Provide a how much time user can book at max. e.g. 15"


class AvailabilityNode(DjangoObjectType):
    """Availability Object Type Definition"""
    id = graphene.ID()
    interval_mints = graphene.String()
    user = graphene.Field(UserType)

    class Meta:
        model = Availability

    @classmethod
    def resolve_interval_mints(cls, availability, info):
        """Resolves interval mints choice field."""
        return availability.get_interval_mints_display()


class CreateAvailability(graphene.Mutation):
    """
    OTD mutation class for creating user availabilities.
    """
    availability = graphene.Field(AvailabilityNode)
    success = graphene.Boolean()

    class Arguments:
        """Defines the arguments the mutation can take."""
        availability_from = graphene.DateTime(description=Description.availability_from, required=True)
        availability_to = graphene.DateTime(description=Description.availability_to, required=True)
        time_interval_mints = graphene.Int(description=Description.time_interval, required=True)

    @classmethod
    def mutate(cls, root, info, availability_from, availability_to, time_interval_mints):
        """Mutate operation creating user availability in the system."""
        user = info.context.user
        availability = Availability.objects.create(
            user=user,
            from_time=availability_from,
            to_time=availability_to,
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
        id = graphene.Int(required=True, description="ID of a availability to update.")
        availability_from = graphene.DateTime(
            description=Description.availability_from,
        )
        availability_to = graphene.DateTime(description=Description.availability_to)
        time_interval_mints = graphene.Int(description=Description.time_interval)

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        """Mutate operation updating user availability in the system."""
        try:
            availability = Availability.objects.get(id=id, user=info.context.user)
        except Availability.DoesNotExist:
            raise GraphQLError(f"This ID:{id} doesn't seem to be belong you!")
        key_mapping = {"availability_from": "from_time", "availability_to": "to_time",
                       "time_interval_mints": "interval_mints"}
        for key, mapping in key_mapping.items():
            if not kwargs.get(key):
                continue
            setattr(availability, mapping, kwargs.get(key))
        availability.save()
        return UpdateAvailability(availability=availability, success=True)


class DeleteAvailability(graphene.Mutation):
    """
    OTD mutation class for deleting user availabilities.
    """
    success = graphene.Boolean(description="Boolean indicating the status of the deletion.")

    class Arguments:
        """Defines the arguments the mutation can take."""
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        """Mutate operation deleting user availability in the system."""
        obj = Availability.objects.get(pk=id, user=info.context.user)
        obj.delete()
        return DeleteAvailability(success=True)


class Query(graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the user availability Schema.
    """
    availabilities = graphene.List(AvailabilityNode)
    availability = graphene.Field(AvailabilityNode, id=graphene.Int(
        required=True, description="ID of a availability to view"
    ))

    @classmethod
    def resolve_availabilities(cls, root, info):
        """Resolve the user availabilities List"""
        return Availability.objects.filter(user=info.context.user)

    @classmethod
    def resolve_availability(cls, root, info, id):
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
