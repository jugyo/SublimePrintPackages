import sublime, sublime_plugin
import os
import json
import StringIO

class PrintPackagesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        output = StringIO.StringIO()
        for package in self.list_packages():
            metadata = self.get_metadata(package)
            if len(metadata) > 1:
                output.write("* [%s](%s)\n" % (package, metadata['url']))

        insert_position = self.view.sel()[0].begin()
        self.view.insert(edit, insert_position, output.getvalue())

    # from https://github.com/wbond/sublime_package_control/blob/master/Package%20Control.py#L2627
    def list_packages(self):
        package_names = os.listdir(sublime.packages_path())
        package_names = [path for path in package_names if
            os.path.isdir(os.path.join(sublime.packages_path(), path))]
        # Ignore things to be deleted
        ignored_packages = []
        for package in package_names:
            cleanup_file = os.path.join(sublime.packages_path(), package,
                'package-control.cleanup')
            if os.path.exists(cleanup_file):
                ignored_packages.append(package)
        packages = list(set(package_names) - set(ignored_packages) -
            set(self.list_default_packages()))
        packages = sorted(packages, key=lambda s: s.lower())
        return packages

    # from https://github.com/wbond/sublime_package_control/blob/master/Package%20Control.py#L2655
    def list_default_packages(self):
        files = os.listdir(os.path.join(os.path.dirname(
            sublime.packages_path()), 'Pristine Packages'))
        files = list(set(files) - set(os.listdir(
            sublime.installed_packages_path())))
        packages = [file.replace('.sublime-package', '') for file in files]
        packages = sorted(packages, key=lambda s: s.lower())
        return packages

    def get_metadata(self, package):
        metadata_filename = os.path.join(self.get_package_dir(package),
            'package-metadata.json')
        if os.path.exists(metadata_filename):
            with open(metadata_filename) as f:
                try:
                    return json.load(f)
                except (ValueError):
                    return {}
        return {}

    def get_package_dir(self, package):
        return os.path.join(sublime.packages_path(), package)
