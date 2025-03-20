import unittest
from datetime import datetime

from change.change import Change
from lead_time.working_hours_aware_lead_time_calculator import WorkingHoursAwareLeadTimeCalculator


class TestWorkingHoursAwareLeadTimeCalculator(unittest.TestCase):
    HOURS_ON_WORKING_DAY = 9

    def express_in_seconds(self, **kwargs):
        total_secounds = 0

        if 'days' in kwargs:
            total_secounds += kwargs['days'] * 24 * 60 * 60

        if 'hours' in kwargs:
            total_secounds += kwargs['hours'] * 60 * 60

        if 'minutes' in kwargs:
            total_secounds += kwargs['minutes'] * 60

        if 'seconds' in kwargs:
            total_secounds += kwargs['seconds']

        return total_secounds


    def test_given_created_and_accepted_on_same_day_within_working_hours_get_lead_time_returns_simple_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T11:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-03T14:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3))

    def test_given_created_and_accepted_time_within_working_hours_get_lead_time_returns_difference_scaled_to_working_day_length(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T11:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-06T14:00:00'),  # Thursday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3 + 3*self.HOURS_ON_WORKING_DAY))

    def test_given_created_and_accepted_time_within_working_hours__with_multiple_weeks_in_between_get_lead_time_returns_difference_skipping_weekends(
            self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T11:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-13T14:00:00'),  # Thursday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3 + 8*self.HOURS_ON_WORKING_DAY))


    def test_given_created_before_working_hours_accepted_on_same_day_get_lead_time_returns_adjusted_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T08:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-03T14:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=4))

    def test_given_accepted_on_the_same_day_after_working_hours_accepted_on_same_day_get_lead_time_returns_adjusted_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T12:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-03T21:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=7))

    def test_given_created_and_accepted_on_the_same_day_outside_working_hours_accepted_on_same_day_get_lead_time_returns_adjusted_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T08:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-03T21:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=self.HOURS_ON_WORKING_DAY))

    def test_given_created_and_accepted_on_the_same_day_after_working_hours_accepted_on_same_day_get_lead_time_returns_simple_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T21:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-03T23:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=2))

    def test_given_created_and_accepted_on_different_days_created_outside_working_hours_get_lead_time_returns_adjusted_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T21:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-06T14:00:00'), # Thursday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=4 + 2*self.HOURS_ON_WORKING_DAY))

    def test_given_created_and_accepted_on_different_days_created_and_accepted_after_working_hours_get_lead_time_returns_adjusted_difference(
            self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T21:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-06T21:00:00'),  # Thursday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3*self.HOURS_ON_WORKING_DAY))

    def test_given_created_and_accepted_on_different_days_accepted_outside_working_hours_get_lead_time_returns_adjusted_difference(
            self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T13:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-06T21:00:00'),  # Thursday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=6 + 3 * self.HOURS_ON_WORKING_DAY))

    def test_given_created_and_accepted_on_different_days_accepted_before_working_hours_get_lead_time_returns_adjusted_difference(
            self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-03T13:00:00'),  # Monday
            accepted_at=datetime.fromisoformat('2025-03-06T07:00:00'),  # Thursday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=6 + 2 * self.HOURS_ON_WORKING_DAY))

    def test_given_created_and_accepted_on_business_days_with_weekend_in_between_get_lead_time_returns_difference_skipping_weekend(
            self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-06T11:00:00'),  # Thursday
            accepted_at=datetime.fromisoformat('2025-03-11T14:00:00'),  # Tuesday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3 + 3*self.HOURS_ON_WORKING_DAY))

    def test_given_created_on_friday_and_accepted_on_monday_get_lead_time_returns_difference_skipping_weekend(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-07T11:00:00'),  # Friday
            accepted_at=datetime.fromisoformat('2025-03-10T14:00:00'),  # Monday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3 + 1*self.HOURS_ON_WORKING_DAY))

    def test_given_created_on_friday_and_accepted_on_monday_multiple_weeks_in_between_get_lead_time_returns_difference_skipping_weekends(
            self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-07T11:00:00'),  # Friday
            accepted_at=datetime.fromisoformat('2025-03-17T14:00:00'),  # Monday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3 + 6*self.HOURS_ON_WORKING_DAY))

    def test_given_created_on_friday_and_accepted_on_saturday_get_lead_time_returns_working_hours_amount(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-07T13:00:00'),  # Friday
            accepted_at=datetime.fromisoformat('2025-03-08T14:00:00'),  # Saturday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=6))

    def test_given_created_on_saturday_and_accepted_on_monday_get_lead_time_returns_working_hours_amount(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-08T11:00:00'),  # Saturday
            accepted_at=datetime.fromisoformat('2025-03-10T14:00:00'),  # Monday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=4))

    def test_given_created_and_accepted_over_weekend_get_lead_time_returns_zero(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-08T11:00:00'),  # Saturday
            accepted_at=datetime.fromisoformat('2025-03-09T14:00:00'),  # Sunday
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, 0)

    def test_given_created_and_accepted_on_same_not_business_day_get_lead_time_returns_simple_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-08T11:00:00'),  # Saturday
            accepted_at=datetime.fromisoformat('2025-03-08T14:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=3))

    def test_given_created_and_accepted_on_same_not_business_day_outside_working_hours_get_lead_time_returns_adjusted_difference(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-08T13:00:00'),  # Saturday
            accepted_at=datetime.fromisoformat('2025-03-08T21:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(hours=6))

    def test_given_created_after_accepted__get_lead_time_returns_zero(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-03-06T11:00:00'),
            accepted_at=datetime.fromisoformat('2025-03-03T14:00:00'),
        )

        lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, 0)