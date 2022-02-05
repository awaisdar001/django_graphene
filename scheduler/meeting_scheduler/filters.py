import django_filters
from django.db.models import Q

from .models import Booking


def filter_queryset_with_fields_and_matcher(fields, matcher):
    """Creates a filter for provided field and matcher on bookings model."""

    def _filter_qs(queryset, _, value):
        if value:
            query_filter = Q()
            for field in fields:
                query_filter |= Q(**{f'{field}__{matcher}': value})
            return queryset.filter(query_filter)
        return queryset

    return _filter_qs


class BookingFilter(django_filters.FilterSet):
    """Booking query filter. """
    search = django_filters.CharFilter(
        method=filter_queryset_with_fields_and_matcher(
            fields=['full_name', 'email'],
            matcher="icontains"
        )
    )
    username = django_filters.CharFilter(
        method=filter_queryset_with_fields_and_matcher(
            fields=['user__username'],
            matcher='iexact'
        )
    )

    class Meta:
        model = Booking
        fields = ["search", "user"]
