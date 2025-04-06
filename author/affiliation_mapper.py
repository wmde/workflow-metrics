import csv
from datetime import datetime

class AffiliationMapper:
    def __init__(self, affiliation_data_fielname):
        self.affiliation_by_author = {}
        self.affiliation_by_author_time_bound = {}
        self.gerrit_account_id_by_github_username = {}

        self.load_affiliation_data(affiliation_data_fielname)

    def load_affiliation_data(self, filename):
        with open(filename) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if not row['wikimedia_gerrit_account_id'] and not row['github_account_name']:
                    continue
                if not row['affiliation']:
                    continue

                affiliation_data = {'organisation': row['affiliation']}
                if row['affiliation_detailed']:
                    affiliation_data['team'] = row['affiliation_detailed']

                id = None
                if row['wikimedia_gerrit_account_id']:
                    id = 'wikimedia-gerrit-' + row['wikimedia_gerrit_account_id']
                elif row['github_account_name']:
                    id = 'github-' + row['github_account_name']

                if row['wikimedia_gerrit_account_id'] and row['github_account_name']:
                    github_author_id = 'github-' + row['github_account_name']
                    if not github_author_id in self.gerrit_account_id_by_github_username:
                        self.gerrit_account_id_by_github_username[github_author_id] = id

                if not id:
                    continue

                if row['affiliation_start'] or row['affiliation_end']:
                    start = None
                    if row['affiliation_start']:
                        start = datetime.strptime(row['affiliation_start'], '%Y-%m-%d')
                    end = None
                    if row['affiliation_end']:
                        end = datetime.strptime(row['affiliation_end'], '%Y-%m-%d')
                    if not id in self.affiliation_by_author_time_bound:
                        self.affiliation_by_author_time_bound[id] = []
                    self.affiliation_by_author_time_bound[id].append({ 'from': start, 'until': end, 'affiliation': affiliation_data })
                    continue

                self.affiliation_by_author[id] = affiliation_data

    def get_affiliation_for_author(self, author_id, change_time):
        if author_id in self.gerrit_account_id_by_github_username:
            author_id = self.gerrit_account_id_by_github_username[author_id]

        if author_id in self.affiliation_by_author_time_bound:
            for time_period in self.affiliation_by_author_time_bound[author_id]:
                matching_period_found = True
                if time_period['from'] and change_time < time_period['from']:
                    matching_period_found = False
                if time_period['until'] and change_time > time_period['until']:
                    matching_period_found = False
                if matching_period_found:
                    return time_period['affiliation']

        if author_id in self.affiliation_by_author:
            return self.affiliation_by_author[author_id]

        return None