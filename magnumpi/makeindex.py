import os
import sys


extensions = ('.tar.gz', '.tgz', '.egg', '.zip', '.bz2', '.whl')


def read_packages(root, _os):
    packages = {}
    for f in _os.listdir(root):
        if not f.endswith(extensions):
            # ignore because file does not appear to be a package
            continue

        parts = f.split('-')
        n = 1
        if f.endswith('.egg'):
            n = 2
        elif f.endswith('.whl'):
            n = 4

        project = '-'.join(parts[:-n])
        if not project:
            sys.stderr.write('error parsing %s\n' % f)
            continue
        packages.setdefault(project, []).append(f)

    return packages


def write_index(root, packages, _os, _open):
    index_root = _os.path.join(root, 'index')
    if not _os.path.exists(index_root):
        _os.makedirs(index_root)
    top = _open(_os.path.join(index_root, 'index.html'), 'w')
    top.writelines(['<html>\n',
                    '<body>\n',
                    '<h1>Package Index</h1>\n',
                    '<ul>\n'])

    for project, files in sorted(packages.items()):
        print('Project: %s' % project)
        project_dir = _os.path.join(index_root, project)
        if not _os.path.exists(project_dir):
            _os.makedirs(project_dir)
        top.write('<li><a href="%s/index.html">%s</a>\n' % (project, project))

        sub = _open(_os.path.join(project_dir, 'index.html'), 'w')
        sub.writelines(['<html>\n',
                        '<body>\n',
                        '<h1>%s Distributions</h1>\n' % project,
                        '<ul>\n'])

        for f in files:
            print('  -> %s' % f)
            sub.write('<li><a href="../../%s">%s</a>\n' % (f, f))

        sub.writelines(['</ul>\n',
                        '</body>\n',
                        '</html>\n'])

    top.writelines(['</ul>\n',
                    '</body>\n',
                    '</html>\n'])
    top.close()


def main():
    if len(sys.argv) != 2:
        sys.exit('must pass direcory with packages as argument')
    root = sys.argv[1]

    packages = read_packages(root, os)
    write_index(root, packages, os, open)
