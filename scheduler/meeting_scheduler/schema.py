import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql_jwt.decorators import user_passes_test
from graphql_relay import from_global_id

from .filters import BookingFilter
from .models import Booking, Availability
from .mutations import (
    CreateBooking, CreateAvailability, DeleteAvailability, UpdateAvailability,
)
from .types import AvailabilityType, BookingType


class BookingQuery(graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the booking schema.
    """
    bookings = DjangoFilterConnectionField(BookingType, filterset_class=BookingFilter)

    @classmethod
    def resolve_bookings_by_user(cls, root, info, username, **kwargs):
        """Resolve bookings by user"""
        return Booking.objects.filter(user__username=username).prefetch_related('user')


class AvailabilityQuery(graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the availability schema.
    """
    availabilities = DjangoFilterConnectionField(AvailabilityType, )
    availability = graphene.Field(AvailabilityType, id=graphene.String(
        required=True, description="ID of a availability to view"
    ))

    @classmethod
    @user_passes_test(lambda user: user and not user.is_anonymous)
    def resolve_availabilities(cls, root, info, *args, **kwargs):
        """Resolve the user availabilities List"""
        return Availability.objects.filter(user=info.context.user)

    @classmethod
    @user_passes_test(lambda user: user and not user.is_anonymous)
    def resolve_availability(cls, root, info, id):
        """Resolve the user availability field"""
        __, _id = from_global_id(id)
        return Availability.objects.get(id=_id, user=info.context.user)


class BookingMutation(graphene.ObjectType):
    """
    Describes entry point for fields to *create* data in bookings API.
    """
    create_booking = CreateBooking.Field()


class AvailabilityMutation(graphene.ObjectType):
    """
    Describes entry point for fields to *create, update or delete* data in availability API.
    """
    create_availability = CreateAvailability.Field()
    update_availability = UpdateAvailability.Field()
    delete_availability = DeleteAvailability.Field()


class UserMutation(graphene.ObjectType):
    """
    Describes entry point for fields to *login, verify token* data in user API.
    """
    login = mutations.ObtainJSONWebToken.Field(description="Login and obtain token for the user")
    verify_token = mutations.VerifyToken.Field(description="Verify if the token is valid.")
