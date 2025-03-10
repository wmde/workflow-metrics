from change.change import Change

class ChangeFactory:
    def __init__(self, author_affiliation_mapper):
        self.author_affiliation_mapper = author_affiliation_mapper

    def create_from_gerrit_change(self, gerrit_change):
        author_id = 'wikimedia-gerrit-' + str(gerrit_change.owner_id)

        author_org = ''
        author_team = ''
        affilitation_data = self.author_affiliation_mapper.get_affiliation_for_author(author_id, gerrit_change.submitted_at)
        if 'organisation' in affilitation_data:
            author_org = affilitation_data['organisation']
        if 'team' in affilitation_data:
            author_team = affilitation_data['team']

        change_info = {
            'id': 'wikimedia-gerrit-' + gerrit_change.change_id,
            'created_at': gerrit_change.created_at,
            'accepted_at': gerrit_change.submitted_at,
            'repository': gerrit_change.project,
            'vcs_system': 'wikimedia-gerrit',
            'author_id': author_id,
            'author_organisation': author_org,
            'author_team': author_team,
        }

        return Change(**change_info)