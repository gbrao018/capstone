import json

try:
    import unzip_requirements
except ImportError:
    pass
import torch
import torchvision
import torchvision.transforms as transform
from PIL import Image

import boto3
import os
import io
import json
import base64
import uuid
import zipfile
import cv2
import requests
from requests_toolbelt.multipart import decoder
print('Import Ends here')

S3_BUCKET = os.environ['S3_BUCKET'] if 'S3_BUCKET' in os.environ else 'ganji-capstone'

s3 = boto3.client('s3')



def generate_token():
    return uuid.uuid1()

def api_generate_token(event, context):
    try:
        guid = generate_token()
        return {
                "statusCode": 200,
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True
                    },
                "body": json.dumps({'token': guid})
                }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
                },
            "body": json.dumps({"error": repr(e)})
            }

def api_upload_train_data(event, context):
    try:
        content_type_header = event['headers']['content-type')
        token = event["body"]['token'].read()
        print('token is ',token)
        bytestream = io.BytesIO(obj['Body']['file'].read())
        #zfile = zipfile.ZipFile(bytestream)
        #s3.Bucket(S3_BUCKET).put(Key=token, Body=bytestream, ACL='public-read')
        s3.meta.client.upload_file(bytestream, S3_BUCKET, token)
        print('Image data uploaded to S3',token)

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
                },
            "body": json.dumps({'token': token})
            }
    except Exception as e:
        print(repr(e))
        return {
                "statusCode": 500,
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True
                    },
                "body": json.dumps({"error": repr(e)})
                }


def api_train(event, context):
    try:
        content_type_header = event['headers']['content-type']
        token = event["body"].read()
        print('token is ',token)
        uri = http://3.7.242.30:5000/classify/train
        data = {}
        data = {}
        data = {
                "token":token
                }
        r = requests.post(uri, json.dumps(data))
        return {
            "statusCode": r.status_code,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
                },
            "body": json.dumps({'result': r.status_code})
            }
    except Exception as e:
        print(repr(e))
        return {
                "statusCode": 500,
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True
                    },
                "body": json.dumps({"error": repr(e)})
                }

def api_test(event, context):
    try:
        content_type_header = event['headers']['content-type']
        token = event["body"].read()
        print('token is ',token)
        uri = http://3.7.242.30:5000/classify/test
        data = {}
        data = {}
        data = {
                "token":token
                }
        r = requests.post(uri, json.dumps(data))
        return {
            "statusCode": r.status_code,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
                },
            "body": json.dumps({'result': r.result})
            }
    except Exception as e:
        print(repr(e))
        return {
                "statusCode": 500,
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True
                    },
                "body": json.dumps({"error": repr(e)})
                }

def api_upload_test_image(event, context):
    try:
        content_type_header = event['headers']['content-type']
        token = generate_token()
        #bucket.new_key(token)
        body = base64.b64decode(event["body"])
        print('BODY LOADED')
        picture = decoder.MultipartDecoder(body,content_type_header).parts[0]
        
        #zfile = zipfile.ZipFile(content)
        #file_list = [( name,
        #    '/tmp/' + os.path.basename(name),
        #    token + os.path.basename(name))
        #    for name in zfile.namelist()]
        key = token+'-'+test
        s3.meta.client.upload_file(content, S3_BUCKET, key)
        print('Image uploaded to S3',key)


        #content = event["body"]#uploaded zipped file
        return {
                "statusCode": 200,
                "headers": {
                    'Content-Type': 'application/zip',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True
                    },
                "body": json.dumps({'token': key})
                }
    except:
        Exception as e:
            print(repr(e))
            return {
                    "statusCode": 500,
                    "headers": {
                        'Content-Type': 'application/zip',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': True
                        },
                    "body": json.dumps({"error": repr(e)})
                    }


def hello(event, context):
    body = {

        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
