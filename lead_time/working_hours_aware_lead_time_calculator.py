from datetime import time, timedelta
import numpy as np
from change.change import Change
from lead_time.lead_time_calculator import LeadTimeCalculator

class WorkingHoursAwareLeadTimeCalculator(LeadTimeCalculator):
    def __init__(self):
        # TODO: inject
        self.working_hours_start = time(hour=10, minute=0, second=0)
        self.working_hours_end = time(hour=19, minute=0, second=0)

    def in_seconds(self, time: time) -> int:
        return int(timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds())

    def get_lead_time(self, change: Change) -> int:
        created = change.created_at
        accepted = change.accepted_at

        if accepted < created:
            return 0

        start_time_normalized = max(created.time(), self.working_hours_start)
        end_time_normalized = min(accepted.time(), self.working_hours_end)

        if created.date() == accepted.date():
            if created.time() > self.working_hours_end and accepted.time() > self.working_hours_end:
                delta = accepted - created
                return int(delta.total_seconds())

            if created.time() < self.working_hours_start and accepted.time() < self.working_hours_start:
                delta = accepted - created
                return int(delta.total_seconds())

            return self.in_seconds(end_time_normalized) - self.in_seconds(start_time_normalized)

        business_days_in_between = max(0, np.busday_count(created.date(), accepted.date()) - 1)
        working_day_in_seconds = self.in_seconds(self.working_hours_end) - self.in_seconds(self.working_hours_start)

        lead_time_on_created_day = 0
        if np.is_busday(created.date()):
            lead_time_on_created_day = max(0, self.in_seconds(self.working_hours_end) - self.in_seconds(start_time_normalized) )

        lead_time_on_accepted_day = 0
        if np.is_busday(accepted.date()):
            lead_time_on_accepted_day = max(0, self.in_seconds(end_time_normalized) - self.in_seconds(self.working_hours_start) )

        return lead_time_on_created_day + business_days_in_between*working_day_in_seconds + lead_time_on_accepted_day
