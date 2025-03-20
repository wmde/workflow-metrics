import argparse
import sys
from change.change_factory import ChangeFactory
from change.change_csv_printer import ChangeCsvPrinter
from author.affiliation_mapper import AffiliationMapper
from lead_time.business_days_aware_lead_time_calculator import BusinessDaysAwareLeadTimeCalculator
from lead_time.working_hours_aware_lead_time_calculator import WorkingHoursAwareLeadTimeCalculator
from wikimedia_gerrit.gerrit_change.gerrit_change_list_json_loader import GerritChangeListJsonLoader
from wikimedia_gerrit.gerrit_api.gerrit_timestamp_converter import GerritTimestampConverter
from lead_time.lead_time_calculator import LeadTimeCalculator

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('json_filename')
arg_parser.add_argument('--no-header', action='store_true')
args = arg_parser.parse_args()

json_filename = args.json_filename
no_header = args.no_header

json_loader = GerritChangeListJsonLoader(GerritTimestampConverter())

author_affiliation_mapper = AffiliationMapper('gerrit_account_data_annotated.csv')
change_factory = ChangeFactory(author_affiliation_mapper)

lead_time_calculator = LeadTimeCalculator()
business_days_aware_lead_time_calculate = BusinessDaysAwareLeadTimeCalculator()
working_hours_aware_lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()

change_csv_printer = ChangeCsvPrinter(sys.stdout)
if not no_header:
    change_csv_printer.print_header()

with open(json_filename) as file:
    for line in file:
        gerrit_changes = json_loader.load_change_data_from_json(line.rstrip())

        for gerrit_change in gerrit_changes:
            change = change_factory.create_from_gerrit_change(gerrit_change)
            lead_time_in_seconds = lead_time_calculator.get_lead_time(change)
            business_days_lead_time_in_seconds = business_days_aware_lead_time_calculate.get_lead_time(change)
            working_hours_lead_time_in_seconds = working_hours_aware_lead_time_calculator.get_lead_time(change)
            change_csv_printer.print(change, lead_time_in_seconds, business_days_lead_time_in_seconds,working_hours_lead_time_in_seconds)
