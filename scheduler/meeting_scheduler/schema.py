import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery
from graphql_jwt.decorators import user_passes_test

from scheduler.meeting_scheduler.models import Booking, Availability
from scheduler.meeting_scheduler.mutations import (
    CreateBooking, CreateAvailability, DeleteAvailability, UpdateAvailability,
)
from scheduler.meeting_scheduler.nodes import AvailabilityNode, BookingNode


class Query(UserQuery, graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the booking Schema.
    """
    availabilities = graphene.List(AvailabilityNode)
    availability = graphene.Field(AvailabilityNode, id=graphene.Int(
        required=True, description="ID of a availability to view"
    ))

    bookings_by_user = graphene.List(
        BookingNode,
        username=graphene.String(required=True),
        # Alternative
        # username=graphene.Argument(graphene.String, description="Pass username of the user.", required=True),
    )

    @classmethod
    @user_passes_test(lambda user: user and not user.is_anonymous)
    def resolve_availabilities(cls, root, info):
        """Resolve the user availabilities List"""
        return Availability.objects.filter(user=info.context.user)

    @classmethod
    @user_passes_test(lambda user: user and not user.is_anonymous)
    def resolve_availability(cls, root, info, id):
        """Resolve the user availability field"""
        return Availability.objects.get(id=id, user=info.context.user)

    @classmethod
    def resolve_bookings_by_user(cls, root, info, username):
        """Resolve bookings by user"""
        return Booking.objects.filter(user__username=username).prefetch_related('user')


class Mutation(graphene.ObjectType):
    """
    Describes entry point for fields to *create, update or delete* data in bookings API.
    """
    # Availability mutations
    create_availability = CreateAvailability.Field()
    update_availability = UpdateAvailability.Field()
    delete_availability = DeleteAvailability.Field()

    # Booking mutations
    create_booking = CreateBooking.Field()

    # User mutations
    login = mutations.ObtainJSONWebToken.Field(description="Login and obtain token for the user")
    verify_token = mutations.VerifyToken.Field(description="Verify if the token is valid.")


schema = graphene.Schema(query=Query, mutation=Mutation)
