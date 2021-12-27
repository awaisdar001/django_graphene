"""
Scheduler API URL Configuration.
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from scheduler.meeting_scheduler.availability_schema import schema as availability_schema
from scheduler.meeting_scheduler.booking_schema import schema as booking_schema
from scheduler.meeting_scheduler.user_schema import schema as user_schema

urlpatterns = [
    path("bookings", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=booking_schema))),
    path("availability", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=availability_schema))),
    path("users", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=user_schema))),

]
