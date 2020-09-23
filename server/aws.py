import os
import boto3
from botocore.exceptions import ClientError

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
            state = ec2_instances['Reservations'][instance_type]['Instances'][instance]['State']['Name']
            try:
                private_ip = ec2_instances['Reservations'][instance_type]['Instances'][instance]['PrivateIpAddress']
            except KeyError:
                private_ip = "None"
            try:
                public_ip = ec2_instances['Reservations'][instance_type]['Instances'][instance]['PublicIpAddress']
            except KeyError:
                public_ip = "None"
            try:
                tags = ec2_instances['Reservations'][instance_type]['Instances'][instance]['Tags']
                name = None
                for tag in tags:
                    if 'Name' in tag["Key"]:
                        name = tag["Value"]
            except KeyError:
                tags = "None"
                name = "None"
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


def get_untagged_instances(region):
    un_tagged_instances = []
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region)
    ec2_instances = ec2.describe_instances()
    for instance_type in range(len(ec2_instances['Reservations'])):
        for instance in range(len(ec2_instances['Reservations'][instance_type]['Instances'])):
            instance_id = ec2_instances['Reservations'][instance_type]['Instances'][instance]['InstanceId']
            tags = ec2_instances['Reservations'][instance_type]['Instances'][instance]['Tags']
            if not any(d.get('instance_id', None) == instance_id for d in tags):
                un_tagged_instances.append(instance_id)
    return un_tagged_instances


def attach_tag_to_instances(ins_list):
    ec2 = boto3.resource('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    for ins in ins_list:
        ec2.create_tags(Resources=[ins], Tags=[{'Key': 'instance_id', 'Value': ins}])


def get_instances_monthly_cost(strt_date, end_date):
    ec2_ce = boto3.client('ce', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    response = ec2_ce.get_cost_and_usage_with_resources(
        TimePeriod={
            'Start': strt_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Filter={"And": [
            {'Dimensions': {
                'Key': 'RECORD_TYPE',
                'Values': ['Usage']}
             },
            {'Dimensions': {
                'Key': 'SERVICE',
                'Values': ['Amazon Elastic Compute Cloud - Compute']}
             }]},
        Metrics=['UnblendedCost'],
        GroupBy=[{
            'Type': 'DIMENSION',
            'Key': 'RESOURCE_ID'}])
    # parsing response
    monthly_cost_list = []
    for single_ins_cost in response['ResultsByTime'][0]['Groups']:
        ins_key = single_ins_cost['Keys'][0]
        ins_cost = single_ins_cost['Metrics']['UnblendedCost']['Amount']
        cost_dic = {
            "CE_INS_KEY": ins_key,
            "CE_INS_COST": round(float(ins_cost), 2)
        }
        monthly_cost_list.append(cost_dic)
    return monthly_cost_list


def get_instances_daily_cost(strt_date, end_date):
    ec2_ce = boto3.client('ce', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    response = ec2_ce.get_cost_and_usage_with_resources(
        TimePeriod={
            'Start': strt_date,
            'End': end_date
        },
        Granularity='DAILY',
        Filter={"And": [
            {'Dimensions': {
                'Key': 'RECORD_TYPE',
                'Values': ['Usage']}
             },
            {'Dimensions': {
                'Key': 'SERVICE',
                'Values': ['Amazon Elastic Compute Cloud - Compute']}
             }]},
        Metrics=['UnblendedCost'],
        GroupBy=[{
            'Type': 'DIMENSION',
            'Key': 'RESOURCE_ID'}])
    # parsing response
    daily_cost_list = []
    for single_ins_cost in response['ResultsByTime'][0]['Groups']:
        ins_key = single_ins_cost['Keys'][0]
        ins_cost = single_ins_cost['Metrics']['UnblendedCost']['Amount']
        cost_dic = {
            "CE_INS_KEY": ins_key,
            "CE_INS_COST": round(float(ins_cost), 2)
        }
        daily_cost_list.append(cost_dic)
    return daily_cost_list


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
