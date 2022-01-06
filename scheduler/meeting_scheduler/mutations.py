"""
Scheduler app mutations
"""

import graphene
from graphql import GraphQLError

from .decorators import user_required
from .enums import Description
from .models import Booking, UserModel as User, Availability
from .nodes import BookingNode, AvailabilityNode


class CreateBooking(graphene.Mutation):
    """
    OTD mutation class for creating bookings with users.
    """
    booking = graphene.Field(BookingNode)
    success = graphene.Boolean()

    class Arguments:
        """Defines the arguments the mutation can take."""
        username = graphene.String(
            description="Provide Username for which the booking is being made.",
            required=True
        )
        full_name = graphene.String(description="Provide your full name", required=True)
        email = graphene.String(description="Provide your email", required=True)
        target_date = graphene.Date(description="Provide the booking date", required=True)
        target_time = graphene.Time(description="Provide the booking time", required=True)
        total_time = graphene.Int(description="Provide the meeting interval", required=True)

    @classmethod
    def mutate(cls, root, info, username, target_date, target_time, **kwargs):
        """Mutate operation creating booking for a user in the system."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError(f"{username} does not exist.")

        booking = Booking(user=user, date=target_date, start_time=target_time, **kwargs)
        if booking.is_valid_new_booking():
            booking.save()
            return CreateBooking(booking=booking, success=True)

        GraphQLError("Booking information is not valid.")


class CreateAvailability(graphene.Mutation):
    """
    OTD mutation class for creating user availabilities.
    """
    availability = graphene.Field(AvailabilityNode)
    success = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        """Defines the arguments the mutation can take."""
        availability_from = graphene.DateTime(description=Description.availability_from, required=True)
        availability_to = graphene.DateTime(description=Description.availability_to, required=True)
        time_interval_mints = graphene.Int(description=Description.time_interval, required=True)

    @classmethod
    @user_required
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
    error = graphene.String()

    class Arguments:
        """Defines the arguments the mutation can take."""
        id = graphene.Int(required=True, description="ID of a availability to update.")
        availability_from = graphene.DateTime(
            description=Description.availability_from,
        )
        availability_to = graphene.DateTime(description=Description.availability_to)
        time_interval_mints = graphene.Int(description=Description.time_interval)

    @classmethod
    @user_required
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
    error = graphene.String(required=False)

    class Arguments:
        """Defines the arguments the mutation can take."""
        id = graphene.ID()

    @classmethod
    @user_required
    def mutate(cls, root, info, id):
        """Mutate operation deleting user availability in the system."""
        obj = Availability.objects.get(pk=id, user=info.context.user)
        obj.delete()
        return cls(success=True, error=None)
