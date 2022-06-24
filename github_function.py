import json
import util
import aws 

def upload_handler(event, context):
    boto = aws.Aws(
        util.get_s3_client(),
        util.get_s3_resource(),
        util.get_iam_client(),
        util.get_lambda_client()
    )
    
    status_code, response = boto.add_file_to_bucket(payload=event)
    if status_code == 200:
        msg = f'{status_code} - FILE {event["file_name"]} UPLOADED TO {event["bucket_name"]} SUCCESSFULLY!'
        print(msg)
    else:
        status_code == 404
        msg = f'{status_code} - AN ERROR OCCURED UPLOADED {event["file_name"]} TO {event["bucket_name"]}\n{response}'
        print(msg)
    return {
        'statusCode' : status_code,
        'body' : json.dumps(msg)
    }