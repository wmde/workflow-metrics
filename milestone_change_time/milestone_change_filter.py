from author.author import Author
from change import change

class MilestoneChangeFilter:
    def __init__(self, changes: list[change.Change]):
        self.changes = changes

    def get_milestone_change_dates(self, author: Author, milestones: list[int]):
        changes_of_author = [change for change in self.changes if change.author_id == author.author_id]
        changes_of_author.sort(key=lambda change: change.accepted_at)

        milestone_change_dates = {}
        for milestone in milestones:
            if milestone >= len(changes_of_author) - 1:
                milestone_change_dates[milestone] = None
                continue

            milestone_change_dates[str(milestone)] = changes_of_author[milestone - 1].accepted_at

        return milestone_change_dates