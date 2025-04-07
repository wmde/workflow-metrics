import argparse
import sys
from change.change_factory import ChangeFactory
from change.change_csv_printer import ChangeCsvPrinter
from author.affiliation_mapper import AffiliationMapper
from github.github_change.github_change_list_json_loader import GithubChangeListJsonLoader
from github.github_timestamp_converter import GithubTimestampConverter
from lead_time.business_days_aware_lead_time_calculator import BusinessDaysAwareLeadTimeCalculator
from lead_time.working_hours_aware_lead_time_calculator import WorkingHoursAwareLeadTimeCalculator
from wikimedia_gerrit.gerrit_change.gerrit_change_list_json_loader import GerritChangeListJsonLoader
from wikimedia_gerrit.gerrit_api.gerrit_timestamp_converter import GerritTimestampConverter
from lead_time.lead_time_calculator import LeadTimeCalculator

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('json_filename')
arg_parser.add_argument('-a', '--affiliation-data-filename', required=True)
arg_parser.add_argument('--input-type', choices=['gerrit', 'github'], default='gerrit')
arg_parser.add_argument('--no-header', action='store_true')
args = arg_parser.parse_args()

json_filename = args.json_filename
affiliation_data_filename = args.affiliation_data_filename
input_type = args.input_type
no_header = args.no_header

json_loader = None
if input_type == 'gerrit':
    json_loader = GerritChangeListJsonLoader(GerritTimestampConverter())
elif input_type == 'github':
    json_loader = GithubChangeListJsonLoader(GithubTimestampConverter())

author_affiliation_mapper = AffiliationMapper(affiliation_data_filename)
change_factory = ChangeFactory(author_affiliation_mapper)

lead_time_calculator = LeadTimeCalculator()
business_days_aware_lead_time_calculate = BusinessDaysAwareLeadTimeCalculator()
working_hours_aware_lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()

change_csv_printer = ChangeCsvPrinter(sys.stdout)
if not no_header:
    change_csv_printer.print_header()

changes = []
with open(json_filename) as file:
    for line in file:
        system_specific_changes = json_loader.load_change_data_from_json(line.rstrip())

        for change_to_process in system_specific_changes:
            if input_type == 'gerrit':
                changes.append( change_factory.create_from_gerrit_change(change_to_process) )
            elif input_type == 'github':
                changes.append( change_factory.create_from_github_change(change_to_process) )

for change in changes:
    lead_time_in_seconds = lead_time_calculator.get_lead_time(change)
    business_days_lead_time_in_seconds = business_days_aware_lead_time_calculate.get_lead_time(change)
    working_hours_lead_time_in_seconds = working_hours_aware_lead_time_calculator.get_lead_time(change)
    change_csv_printer.print(change, lead_time_in_seconds, business_days_lead_time_in_seconds,working_hours_lead_time_in_seconds)
