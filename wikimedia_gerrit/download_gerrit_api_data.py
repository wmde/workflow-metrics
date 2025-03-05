import json
import argparse
import sys
from gerrit_api.gerrit_api_client import GerritApiClient

arg_parser = argparse.ArgumentParser(epilog='Either --repository or --repository-list must be specified')
arg_parser.add_argument('-r', '--repository', required=False)
arg_parser.add_argument('-l', '--repository-list', required=False)
arg_parser.add_argument('-s', '--since', required=True)
arg_parser.add_argument('-o', '--output', required=True)

args = arg_parser.parse_args()

gerrit_repositories = []
if args.repository:
    gerrit_repositories.append(args.repository)
elif args.repository_list:
    list_filename = args.repository_list
    with open(list_filename) as file:
        for line in file:
            gerrit_repositories.append(line.rstrip())
else:
    arg_parser.print_help()
    sys.exit(2)

gerrit_since_date = args.since
output_filename = args.output

gerrit_api_client = GerritApiClient()

changes = gerrit_api_client.get_changes_data(gerrit_repositories, gerrit_since_date, True, False)

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(changes, f, ensure_ascii=False)
