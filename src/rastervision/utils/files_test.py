import tempfile
import os
import unittest

import boto3
from moto import mock_s3

from rastervision.utils.files import file_to_str, NotFoundException


class TestFileUtils(unittest.TestCase):
    def setUp(self):
        self.mock_s3 = mock_s3()
        self.mock_s3.start()

        # Save temp file.
        self.file_name = 'hello.txt'
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, self.file_name)
        self.file_contents = 'hello'
        with open(self.file_path, 'w') as myfile:
            myfile.write(self.file_contents)

        # Upload file to mock S3 bucket.
        self.s3 = boto3.client('s3')
        self.bucket = 'mock_bucket'
        self.s3.create_bucket(Bucket=self.bucket)
        self.s3_path = 's3://{}/{}'.format(self.bucket, self.file_name)
        self.s3.upload_file(
            self.file_path, self.bucket, self.file_name)

    def tearDown(self):
        self.temp_dir.cleanup()
        self.mock_s3.stop()

    def test_file_to_str_s3(self):
        str = file_to_str(self.s3_path)
        self.assertEqual(str, self.file_contents)

    def test_file_to_str_local(self):
        str = file_to_str(self.file_path)
        self.assertEqual(str, self.file_contents)

    def test_file_to_str_wrong_s3(self):
        wrong_path = 's3://{}/{}'.format(self.bucket, 'x.txt')
        with self.assertRaises(NotFoundException):
            file_to_str(wrong_path)

    def test_file_to_str_wrong_local(self):
        wrong_path = '/wrongpath/x.txt'
        with self.assertRaises(NotFoundException):
            file_to_str(wrong_path)


if __name__ == '__main__':
    unittest.main()
