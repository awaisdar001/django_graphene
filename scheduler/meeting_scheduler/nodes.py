"""
Custom scheduler app nodes
"""

import graphene
from graphene_django import DjangoObjectType

from scheduler.meeting_scheduler.models import Booking, Availability, UserModel


class UserType(DjangoObjectType):
    """User Object Type Definition"""

    class Meta:
        model = UserModel
        fields = ("id", "username", "email")


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


class BookingNode(DjangoObjectType):
    """Booking Object Type Definition"""
    id = graphene.ID()
    user = graphene.Field(UserType)

    class Meta:
        model = Booking
