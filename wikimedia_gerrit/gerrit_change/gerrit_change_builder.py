from wikimedia_gerrit.gerrit_change.gerrit_change import GerritChange

class GerritChangeBuilder:
    def __init__(self):
        self.change_id = None
        self.project = None
        self.branch = None
        self.subject = None
        self.status = None
        self.created_at = None
        self.owner_id = None
        self.submitted_at = None
        self.submitter_id = None
        self.phabricator_refs = []
        self.files_changed = []
        self.revision_count = None

    def with_change_id(self, change_id):
        self.change_id = change_id
        return self

    def with_project(self, project):
        self.project = project
        return self

    def with_branch(self, branch):
        self.branch = branch
        return self

    def with_subject(self, subject):
        self.subject = subject
        return self

    def with_status(self, status):
        self.status = status
        return self
    def with_created_at(self, created_at):
        self.created_at = created_at
        return self

    def with_owner_id(self, owner_id):
        self.owner_id = owner_id
        return self

    def with_submitted_at(self, submitted_at):
        self.submitted_at = submitted_at
        return self

    def with_submitter_id(self, submitter_id):
        self.submitter_id = submitter_id
        return self

    def with_phabricator_ref(self, phabricator_ref):
        self.phabricator_refs.append(phabricator_ref)
        return self

    def with_revision_count(self, revision_count):
        self.revision_count = revision_count
        return self

    def with_files_changed(self, files_changed):
        self.files_changed.extend(files_changed)
        return self

    def build(self):
        change_info = {}

        if self.change_id is not None:
            change_info['change_id'] = self.change_id

        if self.project is not None:
            change_info['project'] = self.project

        if self.branch is not None:
            change_info['branch'] = self.branch

        if self.subject is not None:
            change_info['subject'] = self.subject

        if self.status is not None:
            change_info['status'] = self.status

        if self.created_at is not None:
            change_info['created_at'] = self.created_at

        if self.owner_id is not None:
            change_info['owner_id'] = self.owner_id

        if self.submitted_at is not None:
            change_info['submitted_at'] = self.submitted_at

        if self.submitter_id is not None:
            change_info['submitter_id'] = self.submitter_id

        if self.phabricator_refs:
            change_info['phabricator_refs'] = self.phabricator_refs

        if self.revision_count is not None:
            change_info['revision_count'] = self.revision_count

        if self.files_changed is not None:
            change_info['files_changed'] = self.files_changed

        return GerritChange(**change_info)