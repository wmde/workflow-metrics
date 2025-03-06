import argparse
import sys
from change.change_factory import ChangeFactory
from change.change_csv_printer import ChangeCsvPrinter
from wikimedia_gerrit.gerrit_change.gerrit_change_list_json_loader import GerritChangeListJsonLoader
from wikimedia_gerrit.gerrit_api.gerrit_timestamp_converter import GerritTimestampConverter
from lead_time.lead_time_calculator import LeadTimeCalculator

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('json_filename')
args = arg_parser.parse_args()

json_filename = args.json_filename

json_loader = GerritChangeListJsonLoader(GerritTimestampConverter())
change_factory = ChangeFactory()
lead_time_calculator = LeadTimeCalculator()

change_csv_printer = ChangeCsvPrinter(sys.stdout)
change_csv_printer.print_header()

with open(json_filename) as file:
    for line in file:
        gerrit_changes = json_loader.load_change_data_from_json(line.rstrip())

        for gerrit_change in gerrit_changes:
            change = change_factory.create_from_gerrit_change(gerrit_change)
            lead_time_in_seconds = lead_time_calculator.get_lead_time(change)
            change_csv_printer.print(change, lead_time_in_seconds)
