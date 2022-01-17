"""Meeting scheduler model tests"""
import random
from datetime import date, time, datetime

from django.test import TestCase

from .models import Booking, UserModel, Availability


class BaseTests(TestCase):
    def create_user(self, username="robo1"):
        return UserModel.objects.create(username=username, password="robo")

    def create_availability(self, user, from_time=None, to_time=None):
        """
        Create user availability today from 11am to 11:45am
        """
        from_time = from_time or datetime.combine(date.today(), time(hour=11, minute=0, second=0))
        to_time = to_time or datetime.combine(date.today(), time(hour=11, minute=45, second=0))
        return Availability.objects.create(
            user=user,
            from_time=from_time,
            to_time=to_time,
            interval_mints=15,
        )

    def create_booking(self, user, start_time=None, total_time=45):
        """
        Create user booking today at 11:00am -- 11:45am
        """
        if not start_time:
            start_time = time(hour=11, minute=0, second=0)
        booking = Booking(
            user=user,
            full_name='DemoX',
            email='a@a.com',
            date=date.today(),
            start_time=start_time,
            total_time=total_time,
        )
        if booking.is_valid_new_booking():
            booking.save()
            return booking


class AppTests(BaseTests):
    def setUp(self) -> None:
        self.robo1 = self.create_user()

    def test_valid_booking(self):
        """Test that you can book new slots. """
        # create availability today from 11am to 11:45am
        self.create_availability(self.robo1)
        # create booking today at 11:00am -- 11:15am
        self.create_booking(user=self.robo1, total_time=15)
        # create new booking at 11:16am -- 11:30am
        self.create_booking(user=self.robo1, start_time=time(hour=11, minute=16), total_time=15)

    def test_valid_booking_in_past(self):
        """Test that you can book new slots in past."""
        # create availability today from 11am to 11:45am
        self.create_availability(self.robo1)
        # create new booking at 11:15am -- 11:30am
        self.create_booking(user=self.robo1, start_time=time(hour=11, minute=15), total_time=15)
        # create new booking at 11:00am -- 11:14am
        self.create_booking(user=self.robo1, start_time=time(hour=11, minute=00), total_time=14)

    def test_no_availability(self):
        """
        Tests that system generates value error when there is
        no availability available for user.
        """
        with self.assertRaises(ValueError) as value_error:
            self.create_booking(user=self.robo1)

        self.assertEqual(
            str(value_error.exception),
            f'{self.robo1.username} has no availability in this slot.'
        )

    def test_already_booked_same_user(self):
        """Tests that user can not book already booked slot."""
        self.create_availability(self.robo1)
        self.create_booking(user=self.robo1)
        with self.assertRaises(ValueError) as value_error:
            self.create_booking(user=self.robo1)

        self.assertEqual(
            str(value_error.exception),
            f'Cannot book slot with {self.robo1.username} The slot is overlapping with other bookings.'
        )

    def test_overlapping_booking(self):
        """Tests that validation fails when we try to book an overlapping slot."""
        self.create_availability(self.robo1)
        self.create_booking(user=self.robo1)
        today_date = date.today()
        # test 20 random cases.
        for case in range(1, 20):
            random_min = random.randint(1, 44)
            random_second = random.randint(1, 59)

            new_booking = Booking(
                user=self.robo1,
                full_name='DemoX',
                email='a@a.com',
                date=today_date,
                start_time=time(hour=11, minute=random_min, second=random_second),
                total_time=10,
            )

            with self.assertRaises(ValueError) as value_error:
                new_booking.is_valid_new_booking()

            self.assertEqual(
                str(value_error.exception),
                f'Cannot book slot with {self.robo1.username} The slot is overlapping with other bookings.'
            )
