import argparse
import sys
import boto3


# display all objects in a bucket
def ls(bucket_name, my_bucket):
    try:
        # print bucket objects
        for file in my_bucket.objects.all():
            print(file.key)
    # connection failed
    except:
        print("Could not perform ls on this bucket")


# add an object to a bucket
def add(bucket_name, object_path, object_name, my_bucket):
    try:
        my_bucket.upload_file(Filename=object_path, Key=object_name)
        print("successfully added")
    # connection failed
    except:
        print("Could not add object to this bucket")


# delete an object from a bucket
def delete(bucket_name, object_path, s3_client):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_path)
        print("successfully deleted")
    # connection failed
    except:
        print("Could not perform delete object from this bucket")


def main():
    # args contains user inputs
    parser = argparse.ArgumentParser(description='Make operation from user')
    parser.add_argument('-o', '--operation', type=str, required=True, help='type of operation')
    parser.add_argument('-b', '--bucket', type=str, help='bucket to make operation')
    parser.add_argument('-k', '--key', type=str, help='object path')
    parser.add_argument('-nk', '--newkey', type=str, help='object path in s3 bucket')
    parser.add_argument('-ak', '--accessKey', type=str, help='Access Key')
    parser.add_argument('-sk', '--secretKey', type=str, help='Secret Key')
    args = parser.parse_args()

    if (args.accessKey and not args.secretKey) or (not args.accessKey and args.secretKey):
        print("missing credentials")
        sys.exit(0)
    # if cerds are not provided use the local configure
    s3_client = boto3.client('s3', aws_access_key_id=args.accessKey, aws_secret_access_key=args.secretKey)
    s3_resource = boto3.resource('s3', aws_access_key_id=args.accessKey, aws_secret_access_key=args.secretKey)
    # create connection to the bucket in s3
    my_bucket = s3_resource.Bucket(args.bucket)


    # the user wants to display the context of the bucket
    if args.operation == "ls":
        # missing arguments for ls operation
        if args.bucket is None:
            print("[-] missing arguments, -b")
            sys.exit(0)
        else:
            ls(args.bucket, my_bucket)

    # the user add an object to a bucket
    elif args.operation == "add":
        # missing arguments for add operation
        if args.bucket is None or args.key is None or args.newkey is None:
            print("[-] missing arguments")
        else:
            add(args.bucket, args.key, args.newkey, my_bucket)

    # the user wants to delete object from specific bucket
    elif args.operation == "del":
        # missing arguments for delete operation
        if args.bucket is None or args.key is None:
            print("[-] missing arguments")
        else:
            delete(args.bucket, args.key, s3_client)

    # check if the operation is valid
    else:
        print(f"There is no operation {args.operation}")
        sys.exit(0)



if __name__ == '__main__':
    main()
