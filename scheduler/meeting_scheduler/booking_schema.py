import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from scheduler.meeting_scheduler.models import Booking, UserModel as User
from scheduler.meeting_scheduler.user_schema import UserType


class BookingNode(DjangoObjectType):
    """Booking Object Type Definition"""
    id = graphene.ID()
    user = graphene.Field(UserType)

    class Meta:
        model = Booking


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


class Query(graphene.ObjectType):
    """
    Describes entry point for fields to *read* data in the booking Schema.
    """
    bookings_by_user = graphene.List(
        BookingNode,
        username=graphene.Argument(
            graphene.String, description="Pass username of the user.", required=True
        ),
    )

    @classmethod
    def resolve_bookings_by_user(cls, root, info, username):
        """Resolve bookings by user"""
        return Booking.objects.filter(user__username=username).prefetch_related('user')


class Mutation(graphene.ObjectType):
    """
    Describes entry point for fields to *create, update or delete* data in bookings API.
    """
    create_booking = CreateBooking.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
