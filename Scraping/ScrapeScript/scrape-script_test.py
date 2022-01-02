import boto3

from scrape_utils import bfs_channels

l = ['nynets-_sal8iqlt8y']
(bfs_channels("testing","arena-urls",l,50,2,True))

s3 = boto3.client('s3')


with open('read_and_write_test', 'wb') as data:
    s3.download_fileobj('arena-urls', 'testing/', data)
# s3://arena-urls/testing/