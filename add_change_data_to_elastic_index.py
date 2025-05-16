from author.affiliation_mapper import AffiliationMapper
from change.change_factory import ChangeFactory
from elasticsearch import Elasticsearch
from lead_time.business_days_aware_lead_time_calculator import BusinessDaysAwareLeadTimeCalculator
from lead_time.lead_time_calculator import LeadTimeCalculator
from lead_time.working_hours_aware_lead_time_calculator import WorkingHoursAwareLeadTimeCalculator
import os
from wikimedia_gerrit.gerrit_api.gerrit_timestamp_converter import GerritTimestampConverter
from wikimedia_gerrit.gerrit_change.gerrit_change_list_json_loader import GerritChangeListJsonLoader

import re

json_filename = 'gerrit-changes.json'
affiliation_data_filename = 'account_data_annotated.csv'

elastic_host_url = os.environ.get('ELASTIC_HOST_URL')
elastic_api_key = os.environ.get('ELASTIC_API_KEY')
elastic_certs = os.environ.get('ELASTIC_CERTS')
elastic_index = os.environ.get('ELASTIC_INDEX')

json_loader = GerritChangeListJsonLoader(GerritTimestampConverter())

author_affiliation_mapper = AffiliationMapper(affiliation_data_filename)
change_factory = ChangeFactory(author_affiliation_mapper)

lead_time_calculator = LeadTimeCalculator()
business_days_aware_lead_time_calculate = BusinessDaysAwareLeadTimeCalculator()
working_hours_aware_lead_time_calculator = WorkingHoursAwareLeadTimeCalculator()

changes = []
with open(json_filename) as file:
    for line in file:
        changes_loaded = json_loader.load_change_data_from_json(line.rstrip())

        for change_to_process in changes_loaded:
            changes.append( change_factory.create_from_gerrit_change(change_to_process) )

elastic_client = Elasticsearch(elastic_host_url, api_key=elastic_api_key, ca_certs=elastic_certs)

for change in changes:
    lead_time_in_seconds = lead_time_calculator.get_lead_time(change)
    business_days_lead_time_in_seconds = business_days_aware_lead_time_calculate.get_lead_time(change)
    working_hours_lead_time_in_seconds = working_hours_aware_lead_time_calculator.get_lead_time(change)
    response = elastic_client.index(index=elastic_index, id='change-' + re.sub( '[^0-9a-zA-Z]', '-', change.id), document={
        'id': change.id,
        'created_at': change.created_at,
        'accepted_at': change.accepted_at,
        'repository': change.repository,
        'vcs_system': change.vcs_system,
        'author_id': change.author_id,
        'author_org': change.author_organisation,
        'author_team': change.author_team,
        'lead_time_in_seconds': lead_time_in_seconds,
        'business_days_lead_time_in_seconds': business_days_lead_time_in_seconds,
        'working_lead_time_in_seconds': working_hours_lead_time_in_seconds,
    })
