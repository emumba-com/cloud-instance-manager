import os
import boto3
from botocore.exceptions import ClientError
from pprint import pprint

# Loading secret keys set in .env
access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


# Get specific region instances
def get_instances_details(region_name):
    instance_detail = []
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region_name)
    ec2_instances = ec2.describe_instances()
    for instance_type in range(len(ec2_instances['Reservations'])):
        for instance in range(len(ec2_instances['Reservations'][instance_type]['Instances'])):
            instance_id = ec2_instances['Reservations'][instance_type]['Instances'][instance]['InstanceId']
            private_ip = ec2_instances['Reservations'][instance_type]['Instances'][instance]['PrivateIpAddress']
            state = ec2_instances['Reservations'][instance_type]['Instances'][instance]['State']['Name']
            try:
                public_ip = ec2_instances['Reservations'][instance_type]['Instances'][instance]['PublicIpAddress']
            except KeyError:
                public_ip = "None"
            tags = ec2_instances['Reservations'][instance_type]['Instances'][instance]['Tags']
            name = None
            for tag in tags:
                if 'Name' in tag["Key"]:
                    name = tag["Value"]
            key_name = ec2_instances['Reservations'][instance_type]['Instances'][instance]['KeyName']

            instance_dict = {
                "Id": instance_id,
                "Name": name,
                "State": state,
                "PublicIP": public_ip,
                "PrivateIP": private_ip,
                "KeyName": key_name,
                "RegionName": region_name
            }
            instance_detail.append(instance_dict)
    return instance_detail


def start_instance(instance_id, region_name):
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region_name)
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as boto3_exception:
        if 'DryRunOperation' not in str(boto3_exception):
            print(boto3_exception)
            return False
        # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        return response
    except ClientError as boto3_exception:
        print(boto3_exception)
        return False


def stop_instance(instance_id, region_name):
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region_name)
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as boto3_exception:
        if 'DryRunOperation' not in str(boto3_exception):
            print(boto3_exception)
            return False
    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        return response
    except ClientError as boto3_exception:
        print(boto3_exception)
        return False


def get_all_regions():
    ec2 = boto3.client(service_name='ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    all_regions = ec2.describe_regions()
    regions_list = []
    for region in all_regions['Regions']:
        regions_list.append(region['RegionName'])
    return regions_list
