class Author:
    def __init__(self, **kwargs):
        self.author_id = kwargs['id']
        self.display_name = kwargs['display_name']
        self.wikimedia_gerrit_username = None if 'wikimedia_gerrit_username' not in kwargs else kwargs['wikimedia_gerrit_username']
        self.github_username = None if 'github_username' not in kwargs else kwargs['github_username']
        self.wikimedia_gitlab_username = None
        self.wmde_start_date = None if 'wmde_start_date' not in kwargs else kwargs['wmde_start_date']
