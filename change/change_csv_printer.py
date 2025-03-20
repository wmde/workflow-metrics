import csv
import os

class ChangeCsvPrinter:
    def __init__(self, output_handle):
        fieldnames = ['id', 'created_at', 'accepted_at', 'repository', 'vcs_system', 'author_organisation', 'author_team', 'lead_time_in_seconds', 'business_days_lead_time_in_seconds', 'working_lead_time_in_seconds']

        self.csv_writer = csv.DictWriter(output_handle, fieldnames=fieldnames, lineterminator=os.linesep)

    def print_header(self):
        self.csv_writer.writeheader()

    def print(self, change, lead_time_in_seconds, business_days_lead_time_in_seconds, working_lead_time_in_seconds: int):
        self.csv_writer.writerow(self.present_as_csv(change, lead_time_in_seconds, business_days_lead_time_in_seconds, working_lead_time_in_seconds))

    def present_as_csv(self, change, lead_time_in_seconds, business_days_lead_time_in_seconds, working_lead_time_in_seconds: int):
        return {
            'id': str(change.id or ''),
            'created_at': str(change.created_at or ''),
            'accepted_at': str(change.accepted_at or ''),
            'repository': str(change.repository or ''),
            'vcs_system': str(change.vcs_system or ''),
            'author_organisation': str(change.author_organisation or ''),
            'author_team': str(change.author_team or ''),
            'lead_time_in_seconds': str(lead_time_in_seconds or ''),
            'business_days_lead_time_in_seconds': str(business_days_lead_time_in_seconds or ''),
            'working_lead_time_in_seconds': str(working_lead_time_in_seconds or ''),
        }


