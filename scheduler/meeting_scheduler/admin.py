"""
Scheduler app admin configurations.
"""
from django.apps import apps
from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Booking, Availability, UserModel as User

admin.site.site_header = "Meeting Scheduler Admin panel"

class SessionAdmin(admin.ModelAdmin):
    """Django session model admin """

    def _session_data(self, obj):
        """Return decoded session data."""
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)


class BookingsAdmin(admin.ModelAdmin):
    """Bookings admin model."""
    readonly_fields = ('end_time',)
    list_display = ('full_name', 'email', 'date', 'start_time', 'end_time', 'total_time',)


admin.site.register(User)
admin.site.register(Availability)
admin.site.register(Booking, BookingsAdmin)

auth_app = apps.get_app_config('graphql_auth')
for model_name, model in auth_app.models.items():
    admin.site.register(model)
