import json

from github.github_change.github_change_builder import GithubChangeBuilder
from github.github_timestamp_converter import GithubTimestampConverter

class GithubChangeListJsonLoader:
    def __init__(self, timestamp_converter: GithubTimestampConverter):
        self.timestamp_converter = timestamp_converter

    def load_change_data_from_json(self, json_string):
        changes = []
        changes_json = json.loads(json_string)
        for change_data in changes_json:
            change = self.parse_single_change_data(change_data)
            changes.append(change)
        return changes

    def parse_single_change_data(self, change_data):
        change_builder = GithubChangeBuilder()

        if 'id' in change_data:
            change_builder.with_pull_request_id(change_data['id'])

        if 'repository' in change_data and 'nameWithOwner' in change_data['repository']:
            change_builder.with_repository(change_data['repository']['nameWithOwner'])

        if 'author' in change_data and 'login' in change_data['author']:
            change_builder.with_author_id(change_data['author']['login'])

        if 'createdAt' in change_data:
            change_builder.with_created_at(self.timestamp_converter.to_datetime(change_data['createdAt']))

        if 'mergedAt' in change_data:
            change_builder.with_merged_at(self.timestamp_converter.to_datetime(change_data['mergedAt']))

        return change_builder.build()