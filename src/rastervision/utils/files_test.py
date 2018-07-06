import tempfile
import os
import unittest

import boto3
from moto import mock_s3

from rastervision.utils.files import file_to_str


class TestFiles(unittest.TestCase):
    @mock_s3
    def setUp(self):
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
        self.s3.meta.client.upload_file(
            self.file_path, self.bucket, self.file_name)

    def test_file_to_str(self):
        s3_str = file_to_str(self.s3_path)
        self.assertEqual(s3_str, self.file_contents)


if __name__ == '__main__':
    unit
