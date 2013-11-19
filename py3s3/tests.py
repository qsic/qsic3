import datetime
import unittest

from django.conf import settings

from py3s3.files import S3File
from py3s3.storage import S3Storage
from qsic.performers.models import Performer


class S3FileTests(unittest.TestCase):
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
        self.assertEqual(get_contents,
                         self.test_contents.encode(settings.ENCODING))


class S3StorageTests(unittest.TestCase):

    def test__000_save_model_with_image(self):
        p = Performer.objects.create(
            first_name='Paul',
            last_name='Logston',
            it_url='http://newyork.improvteams.com/performers/2849/paullogston'
        )
        p.save()
        result = p.save_it_content_from_parsed_it_url()
        self.assertEqual(result['success'], True, 'IT info save failed.')
        result = p.fetch_headshot()
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()