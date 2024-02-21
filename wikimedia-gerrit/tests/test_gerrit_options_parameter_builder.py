import unittest

from gerrit_api.gerrit_options_parameter_builder import GerritOptionsParameterBuilder

class TestGerritOptionsParameterBuilder(unittest.TestCase):
    def test_given_no_options_returns_empty_object(self):
        builder = GerritOptionsParameterBuilder()
        self.assertEqual(builder.build_options(), [])

    def test_given_include_filenames_options_return_expected_values(self):
        builder = GerritOptionsParameterBuilder()
        builder.include_filenames()

        options = builder.build_options()
        self.assertTrue('CURRENT_REVISION' in options)
        self.assertTrue('CURRENT_FILES' in options)

    def test_given_include_comments_options_return_expected_values(self):
        builder = GerritOptionsParameterBuilder()
        builder.include_comments()

        options = builder.build_options()
        self.assertTrue('MESSAGES' in options)

    def test_given_include_tracking_system_refs_options_return_expected_values(self):
        builder = GerritOptionsParameterBuilder()
        builder.include_tracking_system_refs()

        options = builder.build_options()
        self.assertTrue('TRACKING_IDS' in options)

    def test_given_option_set_multiple_times_no_dupes_in_result(self):
        builder = GerritOptionsParameterBuilder()
        builder.include_comments()
        builder.include_comments()

        options = builder.build_options()
        self.assertEqual(options, ['MESSAGES'])

if __name__ == '__main__':
    unittest.main()
