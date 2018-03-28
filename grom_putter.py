import sys
import csv

import boto3
import requests

import aws_deets

def upload(ig_image_url, date, hash, user_name):
    try:
        s3 = boto3.resource('s3', aws_access_key_id=aws_deets.key,
            aws_secret_access_key=aws_deets.secret)
        bucket_name_to_upload_image_to = aws_deets.bucket_name
        s3_image_filename = '__'.join([date, hash, user_name]) + '.jpg'

        req_for_image = requests.get(ig_image_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()
        s3.Bucket(bucket_name_to_upload_image_to).put_object(
            Key=s3_image_filename, Body=req_data, ACL='public-read')
        uploaded_image_url = ('/').join(['https://s3.amazonaws.com',
            bucket_name_to_upload_image_to, s3_image_filename])
        return [True, uploaded_image_url]
    except:
        return [False, [ig_image_url, date, hash, user_name]]


def churn_through_csv(file_name):
    input_file = open(file_name, 'r')
    csv_reader = csv.reader(input_file)

    for line in csv_reader:
        s3_image_filename = '__'.join([line[1], line[0], line[3]]) + '.jpg'
        uploaded_image_url = ('/').join(['https://s3.eu-west-2.amazonaws.com',
            aws_deets.bucket_name, s3_image_filename])
        response = upload(line[2], line[1], line[0], line[3])
        if response[0]:
            print "Successfully uploaded {0}".format(uploaded_image_url)
        else:
            print "Failed to upload {0}".format(uploaded_image_url)

if __name__ == "__main__":
    if sys.argv[1][-3:] == 'csv':
        churn_through_csv(sys.argv[1])
