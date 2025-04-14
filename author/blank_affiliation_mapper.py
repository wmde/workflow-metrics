from author.affiliation_mapper import AffiliationMapper

class BlankAffiliationMapper(AffiliationMapper):
    def __init__(self):
        pass

    def get_affiliation_for_author(self, author_id, change_time):
        return {'organisation': ''}