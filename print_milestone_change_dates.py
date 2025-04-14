import argparse
import csv
import os
import sys
from datetime import datetime

from author.account_data_list_loader import AccountDataListLoader
from author.account_to_author_map import AccountToAuthorMap
from author.blank_affiliation_mapper import BlankAffiliationMapper
from change.change_factory import ChangeFactory
from github.github_change.github_change_list_json_loader import GithubChangeListJsonLoader
from github.github_timestamp_converter import GithubTimestampConverter
from milestone_change_time.milestone_change_filter import MilestoneChangeFilter
from wikimedia_gerrit.gerrit_api.gerrit_timestamp_converter import GerritTimestampConverter
from wikimedia_gerrit.gerrit_change.gerrit_change_list_json_loader import GerritChangeListJsonLoader

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--gerrit-changes', required=True)
arg_parser.add_argument('--github-changes', required=True)
arg_parser.add_argument('--author-data', required=True)
arg_parser.add_argument('--engineer-list', required=True)

args = arg_parser.parse_args()

gerrit_change_json_filename = args.gerrit_changes
github_change_json_filename = args.github_changes
author_data_filename = args.author_data
engineer_list_filename = args.engineer_list

gerrit_changes_json_loader = GerritChangeListJsonLoader(GerritTimestampConverter())
github_changes_json_loader = GithubChangeListJsonLoader(GithubTimestampConverter())
author_data_list_loader = AccountDataListLoader()

change_factory = ChangeFactory(BlankAffiliationMapper())

changes = []
with open(gerrit_change_json_filename) as file:
    for line in file:
        gerrit_changes = gerrit_changes_json_loader.load_change_data_from_json(line.rstrip())
        for gerrit_change in gerrit_changes:
            changes.append(change_factory.create_from_gerrit_change(gerrit_change))

with open(github_change_json_filename) as file:
    for line in file:
        github_changes = github_changes_json_loader.load_change_data_from_json(line.rstrip())
        for github_change in github_changes:
            changes.append(change_factory.create_from_github_change(github_change))

milestone_change_filter = MilestoneChangeFilter(changes)

fieldnames = ['engineer', 'start_date', 'date_change_1', 'date_change_5', 'date_change_10', 'date_change_50', 'date_change_100']
csv_writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator=os.linesep)
csv_writer.writeheader()

author_data = author_data_list_loader.load_author_data_from_csv_file(author_data_filename)
account_to_author_map = AccountToAuthorMap(author_data)

with open(engineer_list_filename) as file:
    for line in file:
        engineer_username = line.rstrip()

        author = account_to_author_map.get_author_for_account_username(engineer_username)

        milestone_change_dates = milestone_change_filter.get_milestone_change_dates(author, [1, 5, 10, 50, 100])
        output_row = {
            'engineer': author.display_name,
            'start_date': '' if not author.wmde_start_date else author.wmde_start_date.strftime('%Y-%m-%d'),
            'date_change_1': '' if '1' not in milestone_change_dates else milestone_change_dates['1'].strftime('%Y-%m-%d'),
            'date_change_5': '' if '5' not in milestone_change_dates else milestone_change_dates['5'].strftime('%Y-%m-%d'),
            'date_change_10': '' if '10' not in milestone_change_dates else milestone_change_dates['10'].strftime('%Y-%m-%d'),
            'date_change_50': '' if '50' not in milestone_change_dates else milestone_change_dates['50'].strftime('%Y-%m-%d'),
            'date_change_100': '' if '100' not in milestone_change_dates else milestone_change_dates['100'].strftime('%Y-%m-%d'),
        }
        csv_writer.writerow(output_row)
