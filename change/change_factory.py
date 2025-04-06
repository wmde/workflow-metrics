from change.change import Change
from github.github_change.github_change import GithubChange


class ChangeFactory:
    def __init__(self, author_affiliation_mapper):
        self.author_affiliation_mapper = author_affiliation_mapper

    def create_from_gerrit_change(self, gerrit_change):
        author_id = 'wikimedia-gerrit-' + str(gerrit_change.owner_id)

        author_org = ''
        author_team = ''
        affilitation_data = self.author_affiliation_mapper.get_affiliation_for_author(author_id, gerrit_change.submitted_at)

        if not affilitation_data:
            author_org = 'UNKNOWN:' + author_id
        elif 'organisation' in affilitation_data:
            author_org = affilitation_data['organisation']

        if affilitation_data and 'team' in affilitation_data:
            author_team = affilitation_data['team']

        change_info = {
            'id': 'wikimedia-gerrit-' + gerrit_change.change_id,
            'created_at': gerrit_change.created_at,
            'accepted_at': gerrit_change.submitted_at,
            'repository': gerrit_change.project,
            'vcs_system': 'wikimedia-gerrit',
            'author_id': author_id,
            'author_organisation': author_org,
            'author_team': author_team,
        }

        return Change(**change_info)

    def create_from_github_change(self, github_change: GithubChange):
        author_id = 'github-' + str(github_change.author_id)

        author_org = ''
        author_team = ''
        affilitation_data = self.author_affiliation_mapper.get_affiliation_for_author(author_id, github_change.merged_at)

        if not affilitation_data:
            author_org = 'UNKNOWN:' + author_id
        elif 'organisation' in affilitation_data:
            author_org = affilitation_data['organisation']

        if affilitation_data and 'team' in affilitation_data:
            author_team = affilitation_data['team']

        change_info = {
            'id': 'github-' + github_change.pull_request_id,
            'created_at': github_change.created_at,
            'accepted_at': github_change.merged_at,
            'repository': github_change.repository,
            'author_id': author_id,
            'author_organisation': author_org,
            'author_team': author_team,
            'vcs_system': 'github',
        }

        return Change(**change_info)