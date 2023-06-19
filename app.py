import boto3
import os

# GLOBAL VARIABLES
os.environ["AWS_ACCESS_KEY_ID"] = "YOUR-AWS-ACCESS-KEY-ID"
os.environ["AWS_SECRET_ACCESS_KEY"] = "YOUR-AWS-SECRET-ACCESS-KEY"
os.environ["AWS_DEFAULT_REGION"] = "YOUR-REGION"

S3 = boto3.resource('s3')

def move_objects_list(bucket_name: str, bucket_prefix: str, partial_object_name: str) -> list:
    """
        Function to search for certain files in a folder.
        :param partial_object_name: str, required: Part of the files names to be search.
        :param bucket_name: str, required: The name of the bucket.
        :param bucket_prefix: str, required: The prefix inside the bucket to the folder.
        :return: list
    """
    object_list = list()
    bucket = S3.Bucket(bucket_name)
    partial_object_path = str(bucket_prefix+partial_object_name)

    for obj in bucket.objects.all():
        if bucket_prefix in obj.key:
            if partial_object_path in obj.key:
                object_list.append(obj.key)

    return object_list

def main(event, context):
    """
        Function to move files for folder in the same bucket.
        :param event: dict, required: dictionary that will give the execution params.
        :param context: object, not-required: In this case there is nothing inside the context
    """
    folder_list: list = list(event['folder_origin'])
    bucket_raw = S3.Bucket(event['bucket'])

    for folder in folder_list:
        bucket_prefix = str(event['prefix']+folder)
        copy_source = dict()
        move_list = move_objects_list(partial_object_name=event['partial_object_name'], 
                                      bucket_name=event['bucket'], 
                                      bucket_prefix=bucket_prefix)
        
        print(f"In {bucket_prefix} we have {len(move_list)} files to move!")
        for item in move_list:
            copy_source = {
            'Bucket': str(event['bucket']),
            'Key': str(item)
            }
            object_name = item.split('/')[-1]
            key = str(bucket_prefix+event['destination_folder']+ object_name)
            print(key)

            # MOVED
            S3.meta.client.copy(CopySource=copy_source, Bucket=event['bucket'], Key=key)
            
            # DELETE OBJ VERSION
            bucket_raw.object_versions.filter(Prefix=str(item)).delete()
        print(f"Folder {folder} finished")
