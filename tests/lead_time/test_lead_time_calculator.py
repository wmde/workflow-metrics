import unittest

from change.change import Change
from datetime import datetime
from lead_time.lead_time_calculator import LeadTimeCalculator

class TestLeadTimeCalculator(unittest.TestCase):

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

    def test_given_different_timestamps_get_lead_time_returns_difference(self):
        change = Change(**{'created_at': datetime.fromisoformat('2025-02-01T10:00:00'), 'accepted_at': datetime.fromisoformat('2025-02-01T10:30:00')})

        lead_time_calculator = LeadTimeCalculator()

        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(minutes=30))

    def test_given_different_timestamps_on_differt_dats_get_lead_time_returns_correct_difference(self):
        change = Change(**{
            'created_at': datetime.fromisoformat('2025-02-01T10:00:00'),
            'accepted_at': datetime.fromisoformat('2025-02-02T11:30:00')
        })

        lead_time_calculator = LeadTimeCalculator()

        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, self.express_in_seconds(days=1,hours=1,minutes=30))

    def test_given_accepted_before_created_get_lead_time_returns_zero(self):
        change = Change(
            created_at=datetime.fromisoformat('2025-02-02T11:00:00'),
            accepted_at=datetime.fromisoformat('2025-02-02T10:30:00')
        )

        lead_time_calculator = LeadTimeCalculator()
        lead_time = lead_time_calculator.get_lead_time(change)

        self.assertEqual(lead_time, 0)