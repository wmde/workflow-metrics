class GerritChange:
    def __init__(self, **kwargs):
        self.change_id = None
        self.project = None
        self.branch = None
        self.subject = None
        self.status = None
        self.created_at = None
        self.owner_id = None
        self.submitted_at = None
        self.submitter_id = None
        self.phabricator_refs = None
        self.revision_count = None
        self.files_changed = None

        if 'change_id' in kwargs:
            self.change_id = kwargs['change_id']
        if 'project' in kwargs:
            self.project = kwargs['project']
        if 'branch' in kwargs:
            self.branch = kwargs['branch']
        if 'status' in kwargs:
            self.status = kwargs['status']
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
        if 'created_at' in kwargs:
            self.created_at = kwargs['created_at']
        if 'owner_id' in kwargs:
            self.owner_id = kwargs['owner_id']
        if 'submitted_at' in kwargs:
            self.submitted_at = kwargs['submitted_at']
        if 'submitter_id' in kwargs:
            self.submitter_id = kwargs['submitter_id']
        if 'phabricator_refs' in kwargs:
            self.phabricator_refs = kwargs['phabricator_refs']
        if 'revision_count' in kwargs:
            self.revision_count = kwargs['revision_count']
        if 'files_changed' in kwargs:
            self.files_changed = kwargs['files_changed']

