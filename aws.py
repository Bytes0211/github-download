# LAST UPDATED 6/20/2022 : 7:51 PM 
import uuid
import boto3 as aws
import requests 
import io 

class Aws:
    """
    A class to represent a aws s3 bucket and behaviors.

    ...

    Attributes
    ----------
        None

    Methods
    -------
    def __init__(self, s3_client, s3_resource, iam_client, lambda_client) -> None:
        initializes boto3 s3 client, s3 resource, iam client, lambda client objects

    def create_bucket_name(self, *args : str) -> str:
        Creates a bucket name ensuring that the name is unique using uuid

    def create_bucket(self, bucket_prefix, resource):
        creates a bucket in aws using the name generated with the create_bucket name method.

    def list_buckets(self):
        creates a list of of buckets associated with the executing profile

    def list_bucket_objects(self, bucket_list_name):
       retrieves list of objects associated with the bucket_list_name 


    def add_file_to_bucket(self, bucket_name, file_name):
        Add file to bucket

    def copy_to_bucket(self, from_bucket, to_bucket, file_name):
        Copy an s3 object from bucket to bucket

    def delete_files_from_bucket(self, bucket_name, file_list):
        '''
            delete files from existing s3

    def enable_bucket_versioning(self, bucket_name:str):
        generate a version for a bucket.

    def __init__(self, client, resource) -> None:
        initializes aws lambda client and aws lambda resource objects

    def list_iam_roles(self)->dict:
        Creates a list of all aws iam roles in aws account

    def validate_iam_role(self, role):
        validates iam role exist in account  

    def __init__(self, client, resource) -> None:
        initializes aws lambda client and aws lambda resource objects

    def list_iam_roles(self):
        list iam roles in account 

    def validate_iam_role(self, role):
        validates iam role exist in account

    def deploy_function(self, role, file, func_name, description, env):
        deploys zip file to aws as a lambda

    def invoke_lambda(self, name, test_event):
        invokes aws lambda remotely 

    def describe_lambda(self, name):
        describes aws lambda 

    def update_function(self, name:str, file_loc:str)->str:
        updates
    """

    

    def __init__(self, s3_client, s3_resource, iam_client, lambda_client) -> None:
        """
        Constructs all the necessary attributes for the bucket object.

            Parameters
            ----------
                client : boto3 aws s3 client object 
                    client object used as a conduit to interact with aws s3 objects 
                resource : boto3 aws s3 resource  object
                    resource object conduit to interact with aws s3 objects
        """
        self.s3_client = s3_client
        self.s3_resource = s3_resource
        self.iam_client = iam_client
        self.lambda_client = lambda_client

    def create_bucket_name(self, *args : str) -> str:
        '''
        Creates a bucket name ensuring that the name is unique using uuid

            Parameters:
            ----------
                #args as string name, using default name if none is passed in      
            Returns:
                bucket name as string 
        '''
        # The generated bucket name must be between 3 and 63 chars long
        try: 
            default_name = 'scotton'
            if args == None or len(args) == 0:
                return ''.join([default_name, str(uuid.uuid4())])
            else: 
                return ''.join([args[0], str(uuid.uuid4())[:8]]) # I will only use the first 8 chars of the uuid
        except Exception as e:
            err = f'An Exception occured creating bucket name:\n {e} '
            print(err)

    def create_bucket(self, bucket_prefix, s3_resource):
        '''
        creates a bucket in aws using the name generated with the create_bucket name method.

            Parameters:
            ----------
                bucket_prefix (str): the prefix of the bucket name
                resource (aws resource): s3 resource meta client 

            Action: 
            -------
                creates s3 bucket in aws

            Returns:
            --------
                Name of bucket (str) , s3 response  
        ''' 
        try:
            session = aws.session.Session()
            current_region = session.region_name
            #bucket_name = create_bucket_name(bucket_prefix)
            # bucket_name = 'aws-sam-cli-managed-default-samclisourcebucket-1tcgb3olhz2nc'
            bucket_name = self.create_bucket_name(bucket_prefix)
            bucket_response = s3_resource.create_bucket(
                Bucket=bucket_name,
            # only works and required outside of us CreateBucketConfiguration={'LocationConstraint': current_region}
            )
            print(bucket_name, current_region)
            return bucket_name, bucket_response
        except Exception as e:
            err = f'AN ERROR OCCURED CREATEDING BUCKET {bucket_prefix}:::\n{e}'
            print(err)

    def list_buckets(self):
        '''
        creates a list of of buckets associated with the executing profile
            Parameters: 
            ----------
                None

            Action: 
            -------
                List all buckets associated with account

            Returns:
            --------
                bucket list   
        ''' 
        try: 
            bucket_list = []
            for bucket_dict in self.s3_resource.meta.client.list_buckets().get('Buckets'):
                bucket_list.append( bucket_dict['Name'])
            return bucket_list
        except Exception as e:
            err = f'AN EXCEPTION OCCURED LISTING BUCKETS::::\n{e} '
            print(err)


    def list_bucket_objects(self, bucket_list_name):
        """
        retrieves list of objects associated with the bucket_list_name 

            Parameters
            ----------
            bucket_list_name : str
                The name of the bucket to reference in aws which we are retrieving objects 

            Returns
            -------
            list : List of objects in the parameter bucket_list_name 
        """
        try: 
            response = self.s3_client.list_objects_v2(Bucket = bucket_list_name)
            object_list = []
            for x in response['Contents']:
                obj_dict = {'Name' : x['Key'], 'Size' : x['Size'], 'StorageClass' : x['StorageClass']}
                object_list.append(obj_dict)
            return object_list
        except Exception as e:
            err = f'AN EXCEPTION OCCURED CREATING FILE LIST FOR BUCKET: {bucket_list_name}\n{e}'
            print(err)



    def add_file_to_bucket(self, payload : dict):
        ''' 
            Add file to bucket\n
            if url is provided , down load file from url\n
            If url is not provided, file string should be a file path\n
            Parameters:
            ----------
                file_name (str):name of file 
                bucket_name (str): name of bucket to add file to
                object_name (str): txt file with optional folder in linux format    
                url(str): url to remote file 
            Action:
            -------
                Add file to existing s3

            Returns:
            --------
                status, str: print confirmation 
        ''' 
        try:
            # DETERMINE FILE TYPE 
            if payload["url"] == None:
                #s3_resource.meta.client.upload_file(
                    #Filename=file_name, Bucket=bucket_name,Key=key)
                with open(payload["file_name"], 'rb') as file:
                   self.s3_client.upload_fileobj(file, payload["bucket_name"], payload["object_name"])
                msg = f'FILE {payload["file_name"]} UPLOADED TO {payload["bucket_name"]} SUCCESSFULLY!'
            else: 
                # file = '2021-01-29-0.json.gz'
                object_name = payload["object_name"]
                file = requests.get(f'{payload["url"]}/{payload["file_name"]}')
                #open('2021-01-29-0.json.gz', 'wb').write(file.content)
                #with open (file_name, 'rb') as f:
                self.s3_client.upload_fileobj(io.BytesIO(file.content), payload["bucket_name"], object_name)
                msg = f'FILE {object_name} UPLOADED TO {payload["bucket_name"]} SUCCESSFULLY!'
            return 200,msg
        except Exception as e:
            err = f'AN EXCEPTION OCCURED UPLOADING FILE {payload["file_name"]} TO BUCKET {payload["bucket_name"]}\n{e} '
            print(err)
            return 400,msg 

    def copy_to_bucket(self, from_bucket, to_bucket, file_name):
        '''
        Copy an s3 object from bucket to bucket
            Parameters:
            ----------
                    from_bucket (str) name of bucket to copy from 
                    to_bucket (str): name of bucket to add file to
                    file_name (text file): txt file
            Action:
            -------
            copy file between buckets
                
            Returns:
            --------
                    Name of bucket (str) , s3 response  
        ''' 
        try: 
            copy_source = {
                'Bucket': from_bucket,
                'Key': file_name
            }
            self.s3_resource.Object(to_bucket, file_name).copy(copy_source)
            msg = f'FILE {file_name} COPIED FROM {from_bucket} TO {to_bucket} '
            print(msg)
        except Exception as e:
            err = f'AN ERROR OCCURED COPYING {file_name} FROM BUCKET {from_bucket} TO BUCKET {to_bucket}:::\n{err}'
            print(err)


    def delete_files_from_bucket(self, bucket_name, file_list):
        '''
            delete files from existing s3

            Parameters:
            ----------
                file_list(text file): list
                bucket (bucket_name): name of bucket to add file to
            Returns:
            --------
                Name of bucket (str) , s3 response  
        ''' 
        try:
            delete_list = []
            if type(file_list) == list:
                for obj in file_list:
                    response = self.s3_client.delete_object(Bucket=bucket_name, Key=obj)
                msg = f'{len(file_list)} DELETED!\n\n{response})'
            else:
                msg = f'{file_list} IS NOT A LIST'
            return 200,  msg
        except Exception as e:
            err = f'AN OCCURED REMOVING FILES FROM BUCKET {bucket_name}\n{e}'
            print(err)
            return 400, err


    def enable_bucket_versioning(self, bucket_name:str):
        '''
        generate a version for a bucket.

            Parameters:
            ----------
                bucket_name (str): string representing bucket name
            Action:
            ------
                creates s3 bucket in aws

            Returns:
            -------
                Name of bucket (str) , s3 response  
        '''
        try: 
            bkt_versioning = self.s3_resource.BucketVersioning(bucket_name)
            bkt_versioning.enable()
            msg = f'VERSION CREATED FOR BUCKET {bucket_name} WITH STATUS {bkt_versioning.status}'
            print(msg)
        except Exception as e:
            err = f'AN EXCEPTION OCCURED CREATING VERSION FOR BUCKET {bucket_name}\n{e}'
            print(err)

    def list_iam_roles(self)->dict:
        """
        Creates a list of all aws iam roles in aws account\n
        uses iam class attribute boto3 aws iam client
            Parameters
                None 
            ----------

            Returns
                list : all aws iam roles in aws account
            ----------
        """
        try: 
            roles = []
            arns = []
            response = self.iam_client.list_roles()
            for i in range(len(response['Roles'])):
                roles.append(response['Roles'][i]['RoleName'])
                arns.append(response['Roles'][i]['Arn'])
            roles_dict = {r[0] : (r[0], r[1]) for r in list(zip(roles, arns))}
            return roles_dict
        except Exception as e:
            err = f'An error has occured retreiving IAM roles:\n{e} '
            print(err)
            return err 


    def validate_iam_role(self, role):
        """
        validates iam role exist in account    
            Parameters
                role (str) : the aws iam role 

            ----------

            Returns
                str : (str) iam role detail  
            ----------
        """
        try:
            role_list =  self.list_iam_roles()
            if role in role_list:
                result = (role_list[role][0],role_list[role][1])
                #result = f'Role: {role_list[role][0]}\nArn: {role_list[role][1]}'
            return 1, result
        except Exception as e:
            msg = f'ROLE {role} NOT FOUND!'
            return 0, msg 

    def deploy_function(self, role, file, func_name, description, env):
        """
        deploys zip file to aws as a lambda  
            Parameters
                role (str) : the aws lambda arn name
                file (str) : the zip of the lambda file that will be deployed
                func_name (str) : the name of the function 
                description (str) : description of the lambda functionality 
                env (str) : environment variables available to the lambda 
            ----------

            Returns
                str : confirmation of deployment  
            ----------
        """    
        try:
            print(f'ROLE:::::{role}')
            if self.validate_iam_role(role)[0]== 1:
                role = self.validate_iam_role(role)
                zip_file = file + '.zip'
                with open(zip_file, 'rb') as f:
                    zipped_code = f.read()
                    handler = file + '.' + func_name
                response = self.lambda_client.create_function(
                    FunctionName = func_name,
                    Description = description,
                    Runtime='python3.9',
                    Role= role[1][1],
                    Handler = handler,
                    Code=dict(ZipFile=zipped_code),
                    Timeout=300, # Maximum allowable timeout  
                    Environment = env,       
                )
                #msg = json.dumps(response, indent=2, default=str)    
                msg = f'LAMBDA CREATED:\nFunction Name: {response["FunctionName"]}\nFunction Arn: {response["FunctionArn"]}'
                print(msg)     
            else: 
                print(f'{role} not found!')
            
        except Exception as e:
            print(f'An lambda deployment error has occured\n{e} ')


    def invoke_lambda(self, name, test_event):
        """
        invokes aws lambda remotely   
            Parameters
                name (str) : the aws lambda arn name
                test_event (dict) : variables passed to the function 

            ----------

            Returns
                str : confirmation of invocation   
            ----------
        """
        import json 
        try:
            #test_event = dict()
            response = self.lambda_client.invoke(
            FunctionName=name,
            Payload=json.dumps(test_event),  
            )
            msg = response['Payload'].read().decode("utf-8")
            return msg 
        except Exception as e:
            msg = f'EXCEPTION OCCURRED INVOKING LAMBDA {name}\n{e}'
            return msg 


    def describe_lambda(self, name):
        """
        describes aws lambda   
            Parameters
                name (str) : the aws lambda arn name
                file_loc (str) : archive file 

            ----------

            Returns
                str : function name, arn, state, LastUpdateStatus    
            ----------
        """
        try:
            response = self.lambda_client.get_function(
                FunctionName=name
            )
            info = 'FunctionName: ' + str(response['Configuration']['FunctionName']) + '\n'
            info = info + 'FunctionArn: ' + str(response['Configuration']['FunctionArn']) + '\n'
            info = info + 'State: ' + str(response['Configuration']['State']) + '\n'
            info = info + 'LastUpdateStatus: ' + str(response['Configuration']['LastUpdateStatus'])
            return info
        except Exception as e:
            err = f'An error occurred while describing boto20220518\n{e} '
            return err


    def update_function(self, name:str, file_loc:str)->str:
        """
        updates aws lambda code remotely   
            Parameters
                name (str) : the aws lambda arn name
                file_loc (str) : archive file 

            ----------

            Returns
                str : confirmation of update   
            ----------
        """
        try: 
            with open(file_loc, 'rb') as f:
                zipped_code = f.read()

            response = self.lambda_client.update_function_code(
                FunctionName=name,
                ZipFile=zipped_code
            )
            msg = (f'lambda funciton {name} updated')
            print(msg)
            return response
            
        except Exception as e:
            err = f'An error occurred while updating lambda {name}\n{e} '
            return err