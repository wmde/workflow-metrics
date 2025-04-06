from datetime import datetime

from github.github_change.github_change import GithubChange

class GithubChangeBuilder:
    def __init__(self):
        self.pull_request_id = None
        self.repository = None
        self.created_at = None
        self.author_id = None
        self.merged_at = None

    def with_pull_request_id(self, pull_request_id: str):
        self.pull_request_id = pull_request_id

    def with_repository(self, repository: str):
        self.repository = repository

    def with_author_id(self, author_id: str):
        self.author_id = author_id

    def with_created_at(self, created_at: datetime):
        self.created_at = created_at

    def with_merged_at(self, merged_at: datetime):
        self.merged_at = merged_at

    def build(self) -> GithubChange:
        change_data = {}

        if self.pull_request_id is not None:
            change_data['pull_request_id'] = self.pull_request_id
        if self.repository is not None:
            change_data['repository'] = self.repository
        if self.author_id is not None:
            change_data['author_id'] = self.author_id
        if self.created_at is not None:
            change_data['created_at'] = self.created_at
        if self.merged_at is not None:
            change_data['merged_at'] = self.merged_at

        return GithubChange(**change_data)