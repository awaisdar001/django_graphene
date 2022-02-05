"""
Booking graphql api tests
"""
from datetime import time

from graphql_relay import to_global_id

from scheduler.meeting_scheduler.tests import BaseTests
from .schema import schema


class BookingAPITests(BaseTests):
    """
    Booking api tests.
    """

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
            query getUserBookings($username: String!) {
              bookings(username: $username){
                edges {
                  node {
                    id user {
                      id username email    
                    }
                  }
                }
              }
            }
        '''

    @classmethod
    def execute_and_assert_success(cls, query, **kwargs):
        """
        Run the query and assert there were no errors.
        """
        result = schema.execute(query, **kwargs)

        assert result.errors is None, result.errors
        return result.data

    @classmethod
    def execute_and_assert_error(cls, query, error, **kwargs):
        """
        Run the query and assert there the expected error is raised.
        """
        result = schema.execute(query, **kwargs)
        assert result.errors is not None, "No errors while executing query!"
        assert any(
            [error in err.message for err in result.errors]
        ) is True, f'No error {error} instead {result.errors}'
        return result.errors

    def test_user_has_one_booking(self):
        """Test that get user booking api returns data."""
        data = self.execute_and_assert_success(
            self.booking_by_user_query,
            variables={"username": "api-user"}
        )

        assert data is not None
        assert len(data['bookings']) == 1

    def test_user_booking_fields(self):
        """Test that get user booking api returns expected data."""
        bookings = self.execute_and_assert_success(
            self.booking_by_user_query,
            variables={"username": "api-user"}
        )['bookings']['edges']

        booking = bookings[0].get('node')
        assert booking['id'] == to_global_id("BookingType", self.user_booking.id)
        assert booking['user'] == {'id': f'{self.user.id}', 'username': 'api-user', 'email': self.user.email}

    def test_empty_filter_value(self):
        """"""
        query = '''
            query getUserBookings($username: String) {
              bookings(username: $username) {
                edges {
                  node {
                    id fullName email date startTime endTime totalTime updatedAt
                    user {
                      id username email
                    }
                  }
                }
              }
            }
        '''
        data = self.execute_and_assert_success(query)
        assert data is not None

    def test_user_booking_additional_fields(self):
        """
        Tests that you can provide additional api key fields and the api
        returns those additional fields.
        """
        query = '''
            query getUserBookings($username: String) {
              bookings(username: $username) {
                edges {
                  node {
                    id fullName email date startTime endTime totalTime updatedAt
                    user {
                      id username email
                    }
                  }
                }
              }
            }
        '''
        bookings = self.execute_and_assert_success(
            query,
            variables={"username": "api-user"}
        )['bookings']['edges']

        for edge in bookings:
            booking = edge.get('node')
            for field in "id fullName email date startTime endTime totalTime updatedAt".split():
                assert field in booking

    def test_missing_variable(self):
        """
        Test that missing variable error is raised when variable is not provided.
        """
        expected_error = 'Variable "$username" of required type "String!" was not provided.'
        self.execute_and_assert_error(self.booking_by_user_query, error=expected_error)
