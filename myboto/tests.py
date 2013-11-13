import datetime
import unittest

from project_settings import settings

from myboto import S3File


class MyBotoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datetime = datetime.datetime.now()

    def setUp(self):
        self.test_contents = ''.join([
            'This file was uploaded ',
            str(self.__class__.datetime)
        ])
        self.test_file_name = '/test.txt'
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME

    def test__000_put_saves_file_to_s3(self):
        fput = S3File(self.bucket,
                      self.test_file_name,
                      self.test_contents,
                      access_key=settings.AWS_ACCESS_KEY_ID,
                      secret_key=settings.AWS_SECRET_ACCESS_KEY)
        put_status_code = fput.put()
        self.assertEqual(put_status_code, 200)

    def test__001_get_pulls_test_file_down(self):
        fget = S3File(self.bucket, self.test_file_name)
        get_status_code, get_contents = fget.get()
        self.assertEqual(get_status_code, 200)
        self.assertEqual(get_contents, self.test_contents.encode('utf-8'))

if __name__ == '__main__':
    unittest.main()