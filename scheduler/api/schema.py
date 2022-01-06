import graphene
from graphql_auth.schema import UserQuery

from scheduler.meeting_scheduler.schema import (
    AvailabilityQuery, BookingQuery, AvailabilityMutation, BookingMutation, UserMutation
)


class Query(BookingQuery, AvailabilityQuery, UserQuery):
    pass


class Mutation(AvailabilityMutation, BookingMutation, UserMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
