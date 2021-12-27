from datetime import time

from scheduler.meeting_scheduler.booking_schema import schema
from scheduler.meeting_scheduler.tests import BaseTests


class BookingAPITests(BaseTests):
    def setUp(self) -> None:
        self.user = self.create_user(username="api-user")
        self.availability = self.create_availability(self.user)
        # Create booking today 11:00am - 11:15am
        self.user_booking = self.create_booking(
            self.user,
            start_time=time(hour=11, minute=0, second=0),
            total_time=15
        )
        self.booking_by_user_query = '''
            query getUserBookings {
              bookingsByUser(username: "api-user"){
                id user {
                  id username email
                }
              }
            }
        '''

    def test_user_has_one_booking(self):
        result = schema.execute(self.booking_by_user_query)
        data = result.data
        assert data is not None
        assert len(data['bookingsByUser']) == 1

    def test_user_booking_fields(self):
        result = schema.execute(self.booking_by_user_query)
        booking = result.data['bookingsByUser'][0]

        assert booking['id'] == f'{self.user_booking.id}'
        assert booking['user'] == {'id': f'{self.user.id}', 'username': 'api-user', 'email': self.user.email}

    def test_user_booking_additional_fields(self):
        self.booking_by_user_query = '''
            query getUserBookings {
              bookingsByUser(username: "api-user"){
                id fullName email date startTime endTime totalTime updatedAt
                user {
                  id username email
                }
              }
            }
        '''
        result = schema.execute(self.booking_by_user_query)
        booking = result.data['bookingsByUser'][0]
        for field in "id fullName email date startTime endTime totalTime updatedAt".split():
            assert field in booking
