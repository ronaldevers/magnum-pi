try:
    from StringIO import StringIO
except ImportError:
    # for python 3.3
    from io import StringIO

import os
import pytest


from magnumpi.makeindex import (
    read_packages,
    write_index,
)


@pytest.fixture
def packages():
    return [
        'basketweaver2-2.0-py27-none-any.whl',
        'basketweaver2-2.0-py27.egg',
        'basketweaver2-2.0.tar.gz',
        'bad-extension',
        'good_extension_bad_name.egg',
    ]


@pytest.fixture
def mock_os(packages):
    class MockOs:
        @staticmethod
        def listdir(path):
            return packages

        @property
        def path(self):
            return self

        @staticmethod
        def makedirs(path):
            pass

        @staticmethod
        def join(*args):
            return os.path.join(*args)

        @staticmethod
        def exists(path):
            return False

    return MockOs()


class TestStringIO(StringIO):
    def close(self):
        pass

    def getvalue(self):
        value = StringIO.getvalue(self)
        StringIO.close(self)
        return value


@pytest.fixture
def mock_open():
    class MockOpen(object):
        def __init__(self):
            self.buffers = {}

        def __call__(self, filename, mode):
            self.buffers[filename] = TestStringIO()
            return self.buffers[filename]

    return MockOpen()

def test_read_packages(mock_os):
    packages = read_packages('root', mock_os)
    assert list(packages.keys()) == ['basketweaver2']
    assert len(packages['basketweaver2']) == 3


def test_write_index(mock_os, mock_open):
    packages = read_packages('root', mock_os)
    write_index('root', packages, mock_os, mock_open)

    index = mock_open.buffers[
        os.path.join('root', 'index', 'index.html')].getvalue()
    assert '"basketweaver2/index.html"' in index

    basketweaver2_index = mock_open.buffers[
        os.path.join('root', 'index', 'basketweaver2', 'index.html')].getvalue()
    assert '"../../basketweaver2-2.0-py27-none-any.whl"' in basketweaver2_index
    assert '"../../basketweaver2-2.0.tar.gz"' in basketweaver2_index
