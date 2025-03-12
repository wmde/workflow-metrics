from datetime import timedelta
import numpy as np

from change.change import Change
from lead_time.lead_time_calculator import LeadTimeCalculator

class BusinessDaysAwareLeadTimeCalculator(LeadTimeCalculator):
    def get_lead_time(self, change: Change) -> int:
        created = change.created_at
        accepted = change.accepted_at

        if accepted < created:
            return 0

        delta = accepted - created

        business_days_in_between = max(0, np.busday_count(created.date(), accepted.date()) - 1)
        all_days_in_between = max(0, delta.days - 1)

        if business_days_in_between == all_days_in_between:
            return int(delta.total_seconds())

        if created.date() == accepted.date():
            return int(delta.total_seconds())

        lead_time_on_created_day = 24*3600 - int(timedelta(hours=created.hour, minutes=created.minute, seconds=created.second).total_seconds())
        lead_time_on_accepted_day = int(timedelta(hours=accepted.hour, minutes=accepted.minute, seconds=accepted.second).total_seconds())

        return lead_time_on_created_day + business_days_in_between*24*3600 + lead_time_on_accepted_day