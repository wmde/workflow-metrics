class GerritOptionsParameterBuilder:
    def __init__(self):
        self.options = []

    def include_filenames(self):
        self.options.extend(['CURRENT_REVISION', 'CURRENT_FILES'])

    def include_comments(self):
        self.options.extend(['MESSAGES'])

    def include_tracking_system_refs(self):
        self.options.extend(['TRACKING_IDS'])

    def build_options(self):
        return list(set(self.options))