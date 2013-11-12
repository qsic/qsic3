import unittest

from project_settings import settings

from myboto import S3File

class MyBotoTests(unittest.TestCase):

    def test__connection_made(self):
        f = S3File('test.txt',
                   'This is test info',
                   bucket=settings.AWS_STORAGE_BUCKET_NAME,
                   access_key=settings.AWS_ACCESS_KEY_ID,
                   secret_key=settings.AWS_SECRET_ACCESS_KEY)
        self.assertEqual(f.data, 'This is test info')
        f.put()

if __name__ == '__main__':
    unittest.main()