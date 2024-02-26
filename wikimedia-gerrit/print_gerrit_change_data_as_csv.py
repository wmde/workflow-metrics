import argparse
from gerrit_change.gerrit_change_list_json_loader import GerritChangeListJsonLoader
from presentation.gerrit_change_list_csv_printer import GerritChangeListCsvPrinter

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('json_filename')
args = arg_parser.parse_args()

json_filename = args.json_filename

json_loader = GerritChangeListJsonLoader()
csv_printer = GerritChangeListCsvPrinter()

with open(json_filename) as file:
    for line in file:
        changes = json_loader.load_change_data_from_json(line.rstrip())

        csv_printer.print(changes)