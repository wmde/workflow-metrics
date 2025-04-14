from author.author import Author

class AccountToAuthorMap:
    def __init__(self, author_data: dict[str, Author]):
        self.author_by_wikimedia_gerrit_account = {}
        self.author_by_github_account = {}

        for author in author_data.values():
            if author.wikimedia_gerrit_username:
                self.author_by_wikimedia_gerrit_account[author.wikimedia_gerrit_username] = author
            if author.github_username:
                self.author_by_github_account[author.github_username] = author

    def get_author_for_wikimedia_gerrit_account(self, account_username: str) -> Author | None:
        if not account_username in self.author_by_wikimedia_gerrit_account:
            return None

        return self.author_by_wikimedia_gerrit_account[account_username]

    def get_author_for_github_account(self, account_username: str) -> Author | None:
        if not account_username in self.author_by_github_account:
            return None

        return self.author_by_github_account[account_username]

    def get_author_for_account_username(self, account_username: str) -> Author | None:
        if account_username.startswith('wikimedia-gerrit-'):
            return self.get_author_for_wikimedia_gerrit_account(account_username.removeprefix('wikimedia-gerrit-'))
        if account_username.startswith('github-'):
            return self.get_author_for_github_account(account_username.removeprefix('github-'))
        return None
