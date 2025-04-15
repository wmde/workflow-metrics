class GerritQueryParameterBuilder:
    def __init__(self):
        self.status = None
        self.projects = []
        self.branches = []
        self.excluded_owners = []
        self.after = None

    def only_merged(self):
        self.status = 'merged'
        return self

    def for_project(self, project):
        self.projects.append(project)
        return self

    def for_branch(self, branch):
        self.branches.append(branch)
        return self

    def excluding_owner(self, owner_email):
        self.excluded_owners.append(owner_email)
        return self

    def after_timestamp(self, timestamp):
        self.after = timestamp
        return self

    def build_query_string(self):
        query_string = ''

        if self.status is not None:
            query_string = query_string + ' '
            query_string = query_string + 'status:merged'

        if self.projects:
            query_string = query_string + ' '

            unique_projects = sorted(list(set(self.projects)))
            query_string = query_string + '(' + ' OR '.join(
                map(lambda p: 'project:' + p, unique_projects)
            ) + ')'

        if self.branches:
            query_string = query_string + ' '

            unique_branches = list(set(self.branches))
            query_string = query_string + ' '.join(
                map(lambda b: 'branch:' + b, unique_branches)
            )

        if self.excluded_owners:
            query_string = query_string + ' '

            unique_emails = list(set(self.excluded_owners))
            query_string = query_string + ' '.join(
                map(lambda e: '-owner:' + e, unique_emails)
            )

        if self.after is not None:
            query_string = query_string + ' '
            query_string = query_string + 'after:' + self.after

        return query_string.strip()