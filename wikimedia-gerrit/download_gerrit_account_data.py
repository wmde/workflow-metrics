import argparse
import json
import sys
from gerrit_api.gerrit_api_client import GerritApiClient

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('account_ids_file')
args = arg_parser.parse_args()

account_ids = []
ids_filename = args.account_ids_file
with open(ids_filename) as file:
    for line in file:
        account_ids.append(line.rstrip())

gerrit_api_client = GerritApiClient()

account_data = gerrit_api_client.get_data_of_accounts(account_ids)

json.dump(account_data, sys.stdout, ensure_ascii=False)