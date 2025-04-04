import argparse
import json
import os
import sys
from github_api_client import GithubApiClient

arg_parser = argparse.ArgumentParser(epilog='Either --repository or --repository-list must be specified')
arg_parser.add_argument('-r', '--repository', required=False)
arg_parser.add_argument('-l', '--repository-list', required=False)
arg_parser.add_argument('-s', '--since', required=True)
arg_parser.add_argument('-o', '--output', required=True)

args = arg_parser.parse_args()

repositories = []
if args.repository:
    repositories.append(args.repository)
elif args.repository_list:
    list_filename = args.repository_list
    with open(list_filename) as file:
        for line in file:
            repositories.append(line.rstrip())
else:
    arg_parser.print_help()
    sys.exit(2)

github_api_token = os.environ.get('GITHUB_API_TOKEN')
if github_api_token is None:
    sys.stderr.write('GITHUB_API_TOKEN environment variable is not set')
    sys.exit(1)

since_date = args.since
output_filename = args.output

github_api_client = GithubApiClient(github_api_token)

changes = []
for repository in repositories:
    changes.extend(github_api_client.get_changes_data(repository=repository,since_date=since_date))

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(changes, f, ensure_ascii=False)
