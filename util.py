# LAST UPDATED 6/20/2022 : 7:51 PM 
import os
from dotenv import load_dotenv
import boto3 as aws 



def main():
    '''
    Clears environment variables env, appName, logLevel 
            Parameters:
                    None

            Returns:
                    None
    '''
    if os.environ.get('env') == None:
        ...
    else:
        os.environ.pop('env')

    if os.environ.get('appName') == None:
        ...
    else:
        os.environ.pop('appName')

    if os.environ.get('logLevel') == None: 
        ...
    else:
        os.environ.pop('logLevel')

    #appPath = 'c:' + '\\' + 'Users' + '\\' + 'steve' + '\\' + 'OneDrive' + '\\' + 'Documents' + '\\' + 'Dev' + '\\' + 'Learning' + '\\' + 'projects' + '\\' + 'aws'  + '\\' + 'udemy-data-engineering' + '\\' + 'github-download'
    
    #dotenv_path = Path(appPath)

    #load_dotenv(dotenv_path=dotenv_path)


def get_env():
    ''' No parameters, returns environment variable env'''
    load_dotenv()
    return os.environ.get('env')

def get_appName():
    ''' No parameters, returns environment variable appName'''
    load_dotenv()
    return os.environ.get('appName')

def get_srcDir():
    ''' No parameters, returns environment variable srcDir'''
    load_dotenv()
    return os.environ.get('srcDir')

def get_srcPattern():
    ''' No parameters, returns environment variable srcPattern'''
    load_dotenv()
    return os.environ.get('srcPattern')

def get_srcFileFormat():
    ''' No parameters, returns environment variable srcFileFormat'''
    load_dotenv()
    return os.environ.get('srcFileFormat')

def get_s3_client():
    ''' No parameters, returns aws s3 client object'''
    try:
        s3_client = aws.client('s3')
        return s3_client
    except Exception as e:
        print(e)

def get_s3_resource():
    ''' No parameters, returns aws s3 resource object'''
    try:
        s3_resource = aws.resource('s3')
        return s3_resource
    except Exception as e:
        print(e)

def get_lambda_client():
    ''' No parameters, returns aws lambda client object'''
    try:
        lambda_client = aws.client('lambda')
        return lambda_client
    except Exception as e:
        print(e)

def get_iam_client():
    try:
        iam_client = aws.client('iam')
        return iam_client
    except Exception as e:
        print(e)   





