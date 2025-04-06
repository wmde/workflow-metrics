from datetime import datetime

class GithubTimestampConverter:
    def to_datetime(self, timestamp: str) -> datetime:
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')