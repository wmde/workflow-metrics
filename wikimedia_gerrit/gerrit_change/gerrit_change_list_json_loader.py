import json
from wikimedia_gerrit.gerrit_change.gerrit_change_builder import GerritChangeBuilder

class GerritChangeListJsonLoader:
    def __init__(self, timestamp_converter):
        self.timestamp_converter = timestamp_converter

    def load_change_data_from_json(self, json_string):
        changes = []
        changes_json = json.loads(json_string)
        for change_data in changes_json:
            change = self.parse_single_change_data(change_data)
            changes.append(change)
        return changes

    def parse_single_change_data(self, data):
        change_builder = GerritChangeBuilder()

        if 'change_id' in data:
            change_builder.with_change_id(data['change_id'])

        if 'project' in data:
            change_builder.with_project(data['project'])

        if 'branch' in data:
            change_builder.with_branch(data['branch'])

        if 'subject' in data:
            change_builder.with_subject(data['subject'])

        if 'status' in data:
            change_builder.with_status(data['status'])

        if 'created' in data:
            change_builder.with_created_at(self.timestamp_converter.to_datetime(data['created']))

        if 'owner' in data:
            change_builder.with_owner_id(data['owner']['_account_id'])

        if 'submitted' in data:
            change_builder.with_submitted_at(self.timestamp_converter.to_datetime(data['submitted']))

        if 'submitter' in data:
            change_builder.with_submitter_id(data['submitter']['_account_id'])

        if 'current_revision' in data and 'revisions' in data:
            current_revision_id = data['current_revision']

            change_builder.with_revision_count(data['revisions'][current_revision_id]['_number'])

            files_changed = self.parse_files_changed(data['revisions'][current_revision_id]['files'])
            change_builder.with_files_changed(files_changed)

        if 'tracking_ids' in data:
            phabricator_refs = self.parse_phabricator_references(data['tracking_ids'])
            for phab_id in phabricator_refs:
                change_builder.with_phabricator_ref(phab_id)

        return change_builder.build()

    def parse_phabricator_references(self, tracking_data):
        phabricator_refs = []
        for reference in tracking_data:
            if reference['system'] == 'Phab':
                phabricator_refs.append(reference['id'])

        return phabricator_refs

    def parse_files_changed(self, files_data):
        return list(files_data.keys())