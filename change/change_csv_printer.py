import csv
import os

class ChangeCsvPrinter:
    def __init__(self, output_handle):
        fieldnames = ['id', 'created_at', 'accepted_at', 'repository', 'vcs_system', 'lead_time_in_seconds']

        self.csv_writer = csv.DictWriter(output_handle, fieldnames=fieldnames, lineterminator=os.linesep)

    def print_header(self):
        self.csv_writer.writeheader()

    def print(self, change, lead_time_in_seconds):
        self.csv_writer.writerow(self.present_as_csv(change, lead_time_in_seconds))

    def present_as_csv(self, change, lead_time_in_seconds):
        return {
            'id': str(change.id or ''),
            'created_at': str(change.created_at or ''),
            'accepted_at': str(change.accepted_at or ''),
            'repository': str(change.repository or ''),
            'vcs_system': str(change.vcs_system or ''),
            'lead_time_in_seconds': str(lead_time_in_seconds or '')
        }


