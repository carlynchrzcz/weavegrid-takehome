from app import app
import unittest
import os
import shutil
from pwd import getpwuid

app.testing = True

ROOT = 'test_root'
FILE = 'test_file'
FILE_CONTENTS = 'I am a file in root'
DIRECTORY = 'test_directory'
SUBFILE = 'test_subfile'
SUBFILE_CONTENTS = 'I am a file in a directory'

class TestGetRequest(unittest.TestCase):
    def setUp(self):
        # set up filesystem
        self.filesystem = os.path.join(os.getcwd(), ROOT)
        os.mkdir(self.filesystem)

        os.environ['ROOT_PATH'] = self.filesystem

        # set up file
        self.file = os.path.join(self.filesystem, FILE)
        f = open(self.file, "x")
        f.write(FILE_CONTENTS)
        f.close()

        # set up directory
        self.directory = os.path.join(self.filesystem, DIRECTORY)
        os.mkdir(self.directory)

        # set up subfile
        self.subfile = os.path.join(self.directory, SUBFILE)
        f = open(self.subfile, "x")
        f.write(SUBFILE_CONTENTS)
        f.close()

    def get_metadata(self, path):
        stats = os.stat(os.path.join(path))
        metadata = {
            "name": os.path.basename(path),
            "owner": getpwuid(stats.st_uid).pw_name,
            "size": stats.st_size,
            "permissions": oct(stats.st_mode)[-3:]
        }

        return metadata

    def testGetRootRequest(self):
        with app.test_client() as client:
            response = client.get('/')
            stats = os.stat(self.file)

            expected_response = [
                self.get_metadata(self.file),
                self.get_metadata(self.directory)
            ]

            self.assertEqual(response.get_json(), expected_response)

    def testGetFileRequest(self):
        with app.test_client() as client:
            response = client.get('/' + FILE)

            self.assertEqual(response.get_json(), FILE_CONTENTS)

    def testGetDirectoryRequest(self):
        with app.test_client() as client:
            response = client.get('/' + DIRECTORY)

            self.assertEqual(response.get_json(), [self.get_metadata(self.subfile)])

    def testGetSubFileRequest(self):
        with app.test_client() as client:
            response = client.get('/' + DIRECTORY + '/' + SUBFILE)

            self.assertEqual(response.get_json(), SUBFILE_CONTENTS)

    def testInvalidRequest(self):
        with app.test_client() as client:
            response = client.get('/fake_file')

            self.assertEqual(response.status, '404 NOT FOUND')

    def tearDown(self):
        shutil.rmtree(self.filesystem)

if __name__ == '__main__':
    unittest.main()
