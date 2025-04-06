class GithubChange:
    def __init__(self, **kwargs):
        self.pull_request_id = None
        self.repository = None
        self.created_at = None
        self.author_id = None
        self.merged_at = None

        if 'pull_request_id' in kwargs:
            self.pull_request_id = kwargs['pull_request_id']
        if 'repository' in kwargs:
            self.repository = kwargs['repository']
        if 'created_at' in kwargs:
            self.created_at = kwargs['created_at']
        if 'merged_at' in kwargs:
            self.merged_at = kwargs['merged_at']
        if 'author_id' in kwargs:
            self.author_id = kwargs['author_id']