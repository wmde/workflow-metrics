import requests
import json

from wikimedia_gerrit.gerrit_api.gerrit_query_parameter_builder import GerritQueryParameterBuilder
from wikimedia_gerrit.gerrit_api.gerrit_options_parameter_builder import GerritOptionsParameterBuilder

class GerritApiClient:
    CHANGES_URL_BASE = 'https://gerrit.wikimedia.org/r/changes/'
    ACCOUNT_URL_BASE = 'https://gerrit.wikimedia.org/r/accounts/'
    CHANGES_LIMIT = 500
    USER_AGENT = 'WMDE Gerrit API Client'
    TRANSLATEWIKI_BOT_EMAIL = 'l10n-bot@translatewiki.net'

    def get_changes_data(self, repositories, since_date, only_master_branch=True, exclude_translatewiki_bot=True):
        query_param_builder = GerritQueryParameterBuilder()
        options_param_builder = GerritOptionsParameterBuilder()

        query_param_builder.only_merged()
        for repository in repositories:
            query_param_builder.for_project(repository)
        query_param_builder.after_timestamp(since_date)

        if only_master_branch:
            query_param_builder.for_branch('master')

        if exclude_translatewiki_bot:
            query_param_builder.excluding_owner(self.TRANSLATEWIKI_BOT_EMAIL)

        options_param_builder.include_comments()
        options_param_builder.include_filenames()
        options_param_builder.include_tracking_system_refs()

        should_fetch_next_batch = True
        offset = 0
        result = []

        while should_fetch_next_batch:
            request_params = {
                'q': query_param_builder.build_query_string(),
                'o': options_param_builder.build_options(),
                'n': self.CHANGES_LIMIT
            }
            if offset > 0:
                request_params['S'] = offset

            headers = {
                'User-Agent': self.USER_AGENT
            }

            response = requests.get(self.CHANGES_URL_BASE, params=request_params, headers=headers)

            response_json = self.strip_gerrit_magic_prefix(response.text)

            changes = json.loads(response_json)

            should_fetch_next_batch = False
            if changes and '_more_changes' in changes[-1] and changes[-1]['_more_changes']:
                should_fetch_next_batch = True

            if should_fetch_next_batch:
                offset = offset + self.CHANGES_LIMIT

            result.extend(changes)

        return result

    def get_data_of_accounts(self, account_ids):
        result = []

        headers = {
            'User-Agent': self.USER_AGENT
        }

        for account_id in account_ids:
            url = self.ACCOUNT_URL_BASE + account_id

            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue

            response_json = self.strip_gerrit_magic_prefix(response.text)

            account_data = json.loads(response_json)

            result.append(account_data)

        return result

    def strip_gerrit_magic_prefix(self, gerrit_response):
        return gerrit_response.removeprefix(')]}\'\n')