import datetime
import time
import unittest

from django.conf import settings

from .files import S3ContentFile
from .storage import S3IOError
from .storage import S3Storage
from .storage import S3MediaStorage
from .storage import S3StaticStorage


class Py3s3S3StorageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datetime = datetime.datetime.now()
        cls.modify_time_dt = None

    def setUp(self):
        self.test_content = ''.join([
            'This file was uploaded ',
            str(self.__class__.datetime)
        ])
        self.test_file_name = '/test.txt'
        self.file = S3ContentFile(self.test_content)
        self.storage = S3Storage()

    def test__000_PUT_saves_test_file_to_s3(self):
        name = self.storage._save(self.test_file_name, self.file)
        self.assertEqual(name, self.test_file_name)
        self.__class__.modify_time_dt = datetime.datetime.utcnow()

    def test__001_HEAD_returns_test_file_existance(self):
        self.assertTrue(self.storage.exists(self.test_file_name))

    def test__002_HEAD_returns_correct_file_size(self):
        size = self.storage.size(self.test_file_name)
        self.assertEqual(size, self.file.size)

    def test__003_HEAD_returns_correct_modified_time(self):
        time_ = self.storage.modified_time(self.test_file_name)
        self.assertAlmostEqual(
            time_, self.__class__.modify_time_dt,
            delta=datetime.timedelta(seconds=2)
        )

    def test__004_GET_pulls_test_file_down(self):
        file = self.storage._open(self.test_file_name)
        self.assertEqual(self.file.content, file.content)

    def test__005_DELETE_deletes_test_file_from_s3(self):
        self.storage.delete(self.test_file_name)
        self.assertFalse(self.storage.exists(self.test_file_name))


class Py3s3S3StaticStorageTests(Py3s3S3StorageTests):
    def setUp(self):
        super().setUp()
        self.storage = S3StaticStorage()


class Py3s3S3MediaStorageTests(Py3s3S3StorageTests):
    def setUp(self):
        super().setUp()
        self.storage = S3MediaStorage()

if __name__ == '__main__':
    unittest.main()
