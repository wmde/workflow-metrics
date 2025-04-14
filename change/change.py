class Change:
    def __init__(self, **kwargs):
        self.id = None
        self.created_at = None
        self.accepted_at = None
        self.repository = None
        self.vcs_system = None
        self.author_id = None
        self.author_organisation = None
        self.author_team = None

        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            # TODO: generate an ID somehow? what the ID would be used for?
            pass

        if 'created_at' in kwargs:
            self.created_at = kwargs['created_at']
        if 'accepted_at' in kwargs:
            self.accepted_at = kwargs['accepted_at']

        if 'author_id' in kwargs:
            self.author_id = kwargs['author_id']
        if 'author_organisation' in kwargs:
            self.author_organisation = kwargs['author_organisation']
        if 'author_team' in kwargs:
            self.author_team = kwargs['author_team']

        if 'repository' in kwargs:
            self.repository = kwargs['repository']
        if 'vcs_system' in kwargs:
            self.vcs_system = kwargs['vcs_system']

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Change):
            return self.id == other.id
        return False
