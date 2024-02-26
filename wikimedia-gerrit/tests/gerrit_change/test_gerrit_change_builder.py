import unittest

from gerrit_change.gerrit_change_builder import GerritChangeBuilder

class TestGerritChangeBuilder(unittest.TestCase):

    def test_given_change_id_change_has_change_id_set(self):
        builder = GerritChangeBuilder()
        change_id = 'I7ad37870536adde9fa41ef593a489d9995d38e4c'
        builder.with_change_id(change_id)

        change = builder.build()

        self.assertEqual(change.change_id, change_id)

    def test_given_multiple_fields_change_has_expected_values(self):
        project = 'mediawiki/extensions/Wikibase'
        branch = 'master'
        status = 'MERGED'

        builder = GerritChangeBuilder()
        builder.with_project(project)
        builder.with_branch(branch)
        builder.with_status(status)

        change = builder.build()

        self.assertEqual(change.project, project)
        self.assertEqual(change.branch, branch)
        self.assertEqual(change.status, status)

if __name__ == '__main__':
    unittest.main()
