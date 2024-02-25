import json
import argparse
from gerrit_api.gerrit_api_client import GerritApiClient

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-r', '--repository', required=True)
arg_parser.add_argument('-s', '--since', required=True)
arg_parser.add_argument('-o', '--output', required=True)

args = arg_parser.parse_args()

gerrit_repository = args.repository
gerrit_since_date = args.since
output_filename = args.output

gerrit_api_client = GerritApiClient()

changes = gerrit_api_client.get_changes_data(gerrit_repository, gerrit_since_date)

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(changes, f, ensure_ascii=False)
