from change.change import Change

class ChangeFactory:
    def __init__(self):
        pass

    def create_from_gerrit_change(self, gerrit_change):

        change_info = {
            'id': 'wikimedia-gerrit-' + gerrit_change.change_id,
            'created_at': gerrit_change.created_at,
            'accepted_at': gerrit_change.submitted_at,
            'repository': gerrit_change.project,
            'vcs_system': 'wikimedia-gerrit'
        }

        return Change(**change_info)