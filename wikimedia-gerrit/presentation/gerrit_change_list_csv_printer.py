import csv
import sys
from gerrit_change.gerrit_change import GerritChange

class GerritChangeListCsvPrinter:
    def print(self, changes):
        fieldnames = ['change_id', 'project', 'branch', 'status', 'subject', 'created_at', 'owner_id', 'submitted_at', 'phabricator_refs', 'revision_count', 'files_changed']
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

        writer.writeheader()
        for change in changes:
            writer.writerow(self.present_change_as_csv_fields(change))

    def present_change_as_csv_fields(self, change):
        return {
            'change_id': str(change.change_id or ''),
            'project': str(change.project or ''),
            'branch': str(change.branch or ''),
            'status': str(change.status or ''),
            'subject': str(change.subject or ''),
            'created_at': str(change.created_at or ''),
            'owner_id': str(change.owner_id or ''),
            'submitted_at': str(change.submitted_at or ''),
            'phabricator_refs': '' if change.phabricator_refs is None else ', '.join(change.phabricator_refs),
            'revision_count': str(change.revision_count or ''),
            'files_changed': '' if change.files_changed is None else '\n'.join(change.files_changed)
        }

