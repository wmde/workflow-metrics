from datetime import datetime

from author.author import Author

class AuthorFactory:
    def __init__(self):
        pass

    def create_from_data_dict(self, data) -> Author | None:
        author_id = ''
        if 'wikimedia_gerrit_account_id' in data: # or use wikimedia_gerrit_username
            author_id = 'wikimedia-gerrit-' + data['wikimedia_gerrit_account_id']
        elif 'github_account_name' in data:
            author_id = 'github-' + data['github_account_name']
        else:
            return None

        display_name = '' if not 'display_name' in data else data['display_name']
        wmde_start_date = None
        if data['wmde_start_date']:
            wmde_start_date = datetime.strptime(data['wmde_start_date'], '%Y-%m-%d')

        wikimedia_gerrit_username = None
        if 'wikimedia_gerrit_username' in data:
            wikimedia_gerrit_username = data['wikimedia_gerrit_username']

        github_username = None
        if 'github_account_name' in data:
            github_username = data['github_account_name']

        return Author(
            id=author_id,
            display_name=display_name,
            wmde_start_date=wmde_start_date,
            wikimedia_gerrit_username=wikimedia_gerrit_username,
            github_username=github_username,
        )