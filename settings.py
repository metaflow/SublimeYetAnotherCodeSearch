import sublime

import os.path

def fix_path(path, project_dir):
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(project_dir, path)
    return path

class Settings(object):
    """Code search settings for the project.

    Attributes:
        csearch_path: The path to the csearch command.
        cindex_path: The path to the cindex command.
        index_filename: An optional path to a csearchindex file.
        paths_to_index: An optional list of paths to index.
        paths_to_exclude: TODO(metaflow)
    """

    def __init__(self, csearch_path, cindex_path, index_filename=None,
                 paths_to_index=None, paths_to_exclude=None):
        self.csearch_path = csearch_path
        self.cindex_path = cindex_path
        self.index_filename = index_filename
        self.paths_to_index = paths_to_index
        self.paths_to_exclude = paths_to_exclude

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.csearch_path == other.csearch_path and
                self.cindex_path == other.cindex_path and
                self.index_filename == other.index_filename and
                self.paths_to_index == other.paths_to_index and
                self.paths_to_exclude == other.paths_to_exclude)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # Not really needed, so a very dumb implementation to just be correct.
        return 42

    def __repr__(self):
        s = ('{0}(csearch_path={1}; cindex_path={2}; index_filename={3};'
             ' paths_to_index={4}, paths_to_exclude={5})')
        return s.format(self.__class__, self.csearch_path, self.cindex_path,
                        self.index_filename, self.paths_to_index, self.paths_to_exclude)


def get_project_settings(project_data, project_file_name, index_project_folders=False):
    """Gets the Code Search settings for the current project.

    Args:
        project_data: The project data associated for a window as a dict.
        index_project_folders: A boolean which specifies if we should use the
            project's folders as our starting points for indexing files.
    Returns:
        A Settings object describing the code search settings.
    Raises:
        Exception: If an index file was set, but it doesn't exist or if the
            index file is missing.
    """
    print("get_project_settings", project_data, project_file_name)
    settings = sublime.load_settings('YetAnotherCodeSearch.sublime-settings')
    path_cindex = settings.get('path_cindex')
    path_csearch = settings.get('path_csearch')
    index_filename = None
    paths_to_index = []
    paths_to_exclude = []
    project_dir = os.path.dirname(project_file_name)
    if ('code_search' in project_data):
        if 'csearchindex' in project_data['code_search']:
            index_filename = project_data['code_search']['csearchindex']
            index_filename = os.path.expanduser(index_filename)
            if not os.path.isabs(index_filename):
                index_filename = os.path.join(project_dir, index_filename)
            print("index_filename", index_filename)
        if 'exclude' in project_data['code_search']:
            for excluded in project_data['code_search']['exclude']:
                excluded = fix_path(excluded, project_dir)
                print("excluded", excluded)
                paths_to_exclude.append(excluded)
        # if not os.path.isfile(index_filename) and not index_project_folders:
        #     raise Exception(
        #         'The index file, {}, does not exist'.format(index_filename))

    if index_project_folders:
        print("project_dir", project_dir)
        for folder in project_data['folders']:
            path = os.path.expanduser(folder['path'])
            if not os.path.isabs(path):
                path = os.path.join(project_dir, path)
            paths_to_index.append(path)

    return Settings(path_csearch, path_cindex,
                    index_filename=index_filename,
                    paths_to_index=paths_to_index,
                    paths_to_exclude=paths_to_exclude)
