import boto
import boto.s3.connection

#s3conn = boto.s3.Connection(
s3conn = boto.connect_s3(
    aws_access_key_id='test',
    aws_secret_access_key='20abcff02df7dede8661d84116ea4efa',
    port=8080,
    host='127.0.0.1',
    is_secure=False,
    calling_format=boto.s3.connection.OrdinaryCallingFormat())

print s3conn

for bucket in s3conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        )
