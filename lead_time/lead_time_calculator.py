from change.change import Change

class LeadTimeCalculator:
    def __init__(self):
        pass

    # TODO: exlcude weekends?
    def get_lead_time(self, change: Change) -> int:
        created = change.created_at
        accepted = change.accepted_at

        if accepted < created:
            return 0

        delta = accepted - created
        return int(delta.total_seconds())
