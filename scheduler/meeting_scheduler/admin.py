from django.apps import apps
from django.contrib import admin

from scheduler.meeting_scheduler.models import Booking, Availability, UserModel as User


class BookingsAdmin(admin.ModelAdmin):
    """Bookings admin model"""
    readonly_fields = ('end_time',)
    list_display = ('full_name', 'email', 'date', 'start_time', 'end_time', 'total_time',)


admin.site.register(User)
admin.site.register(Availability)
admin.site.register(Booking, BookingsAdmin)

auth_app = apps.get_app_config('graphql_auth')
for model_name, model in auth_app.models.items():
    admin.site.register(model)