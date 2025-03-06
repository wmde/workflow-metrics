class Change:
    def __init__(self, **kwargs):
        self.id = None
        self.created_at = None
        self.accepted_at = None
        self.repository = None
        self.vcs_system = None
        # TODO: author (org, team, etc) required to be able to filter the relevant data to be measured

        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            # TODO: generate an ID somehow? what the ID would be used for?
            pass

        if 'created_at' in kwargs:
            self.created_at = kwargs['created_at']
        if 'accepted_at' in kwargs:
            self.accepted_at = kwargs['accepted_at']
        if 'repository' in kwargs:
            self.repository = kwargs['repository']
        if 'vcs_system' in kwargs:
            self.vcs_system = kwargs['vcs_system']
