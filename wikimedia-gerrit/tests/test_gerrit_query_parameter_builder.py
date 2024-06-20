import unittest

from gerrit_api.gerrit_query_parameter_builder import GerritQueryParameterBuilder

class TestGerritQueryParameterBuilder(unittest.TestCase):
    def test_given_no_input_returns_empty_string(self):
        builder = GerritQueryParameterBuilder()
        self.assertEqual(builder.build_query_string(), '')

    def test_given_only_merged_set_query_string_includes_status_merged(self):
        builder = GerritQueryParameterBuilder()
        builder.only_merged()

        self.assertEqual(builder.build_query_string(), 'status:merged')

    def test_given_project_query_string_includes_project(self):
        builder = GerritQueryParameterBuilder()
        builder.for_project('mediawiki/extensions/Wikibase')

        self.assertEqual(builder.build_query_string(), '(project:mediawiki/extensions/Wikibase)')

    def test_given_multiple_projects_query_string_includes_all_projects_ored(self):
        builder = GerritQueryParameterBuilder()
        builder.for_project('mediawiki/extensions/Wikibase')
        builder.for_project('mediawiki/core')

        self.assertEqual(builder.build_query_string(), '(project:mediawiki/core OR project:mediawiki/extensions/Wikibase)')

    def test_given_branch_query_string_includes_branch(self):
        builder = GerritQueryParameterBuilder()
        builder.for_branch('main')

        self.assertEqual(builder.build_query_string(), 'branch:main')

    def test_given_owner_email_to_exclude_query_string_includes_email(self):
        builder = GerritQueryParameterBuilder()
        builder.excluding_owner('helga.knoblauch@example.net')

        self.assertEqual(builder.build_query_string(), '-owner:helga.knoblauch@example.net')

    def test_given_after_timestamp_query_string_includes_after_date(self):
        builder = GerritQueryParameterBuilder()
        builder.after_timestamp('2023-01-01')

        self.assertEqual(builder.build_query_string(), 'after:2023-01-01')

    def test_given_only_merged_and_project_set_query_string_includes_all_fields(self):
        builder = GerritQueryParameterBuilder()
        builder.only_merged()
        builder.for_project('mediawiki/extensions/Wikibase')

        self.assertEqual(builder.build_query_string(), 'status:merged (project:mediawiki/extensions/Wikibase)')

if __name__ == '__main__':
    unittest.main()
