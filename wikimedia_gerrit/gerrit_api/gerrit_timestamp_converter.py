from datetime import datetime

class GerritTimestampConverter:
    def to_datetime(self, timestamp):
        timestamp = self.strip_nanoseconds(timestamp)
        return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    def strip_nanoseconds(self, timestamp):
        nanosecond_suffix = '.000000000'
        if timestamp.endswith(nanosecond_suffix):
            return timestamp[:-len(nanosecond_suffix)]
        return timestamp