import datetime
import unittest

from django.conf import settings

from .files import S3ContentFile
from .storage import S3Storage


class Py3s3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datetime = datetime.datetime.now()

    def setUp(self):
        self.test_content = ''.join([
            'This file was uploaded ',
            str(self.__class__.datetime)
        ])
        self.test_file_name = '/test.txt'
        self.file = S3ContentFile(self.test_content)
        self.storage = S3Storage()

    def test__000_put_saves_file_to_s3(self):
        name = self.storage._save(self.test_file_name, self.file)
        self.assertEqual(name, self.test_file_name)

    def test__001_get_pulls_test_file_down(self):
        file = self.storage._open(self.test_file_name)
        self.assertEqual(self.file.content, file.content)

if __name__ == '__main__':
    unittest.main()
