from datetime import datetime, date, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class UserModel(AbstractUser):
    """
    User model class implementing an abstract base class for a fully featured User model with
    admin-compliant permissions.
    """
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"  # e.g: "username", "email"
    EMAIL_FIELD = "email"  # e.g: "email", "primary_email"


class Availability(models.Model):
    """
    Availability model keeps tack of user's availability information.
    """
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_availability",
        null=True,
        blank=True,
    )
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    interval_mints = models.CharField(max_length=3, default='15', choices=settings.INTERVAL_CHOICES)

    class Meta:
        unique_together = ('user', 'from_time', 'to_time')

    @staticmethod
    def user_has_availability(user, target_date, start_time, end_time, total_time):
        """
        Checks if user has availability in the provided span range.
        Arguments:
            user (UserModel): instance of the user model.
            target_date: target date of a meeting/appointment.
            start_time: start time of a  meeting/appointment.
            end_time: end time of a  meeting/appointment.
        """
        target_start_datetime = datetime.combine(target_date, start_time)
        target_end_datetime = datetime.combine(target_date, end_time)
        return Availability.objects.filter(
            user=user,
            from_time__lte=target_start_datetime,
            to_time__gte=target_end_datetime,
        ).count()


class Booking(models.Model):
    """
    Booking model to keep track of appointment bookings.
    """
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_bookings",
        null=True,
        blank=True,
    )

    full_name = models.CharField("full name", max_length=100)
    email = models.EmailField()

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_time = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def validate_if_booking_has_already_exists(self):
        """
        Checks weather a booking for user already exists or not.
        Returns (Boolean): boolean value
        """
        return Booking.objects.filter(user=self.user, date=self.date, start_time=self.start_time).exists()

    def is_valid_new_booking(self):
        """
        Validates booking object before trying to save.

        Not already booked:
            The method tries to validate if the booking has already been done or its
            available for booking.
        User has availability:
            Checks if user has available in the provided booking slot.

        Returns:
            boolean(True): if all validations pass
        Raises:
            ValueError - in case of any validation fails
        """
        self.end_time = (
                datetime.combine(date.today(), self.start_time) + timedelta(minutes=self.total_time)
        ).time()
        already_booked = self.validate_if_booking_has_already_exists()
        if already_booked:
            raise ValueError(f'{self.user.username} has already been booked for {self.start_time}')

        has_availability = Availability.user_has_availability(
            user=self.user,
            target_date=self.date,
            start_time=self.start_time,
            end_time=self.end_time,
            total_time=self.total_time
        )
        if not has_availability:
            raise ValueError(f'{self.user.username} has no availability in this slot.')
        is_overlapping_booking = self.is_overlapping_booking()
        if is_overlapping_booking:
            raise ValueError(f'The slot is overlapping with other bookings.')
        return True

    def is_overlapping_booking(self):
        breakpoint()
        return Booking.objects.filter(
            Q(user=self.user) &
            Q(date=self.date),
            Q(start_time__range=[self.start_time, self.end_time]) |
            Q(end_time__range=[self.start_time, self.end_time])
        ).exists()
