import boto3, os
from botocore.exceptions import ClientError

# Loading secret keys set in .env
access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

all_regions = []
regions_list = []

# Getting all regions at the start..
ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
all_regions = ec2.describe_regions()
for region in all_regions['Regions']:
    regions_list.append(region['RegionName'])

# Get specific region instances
def get_instances_details(region_name):
    instance_detail = []
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region_name)
    ec2_instances = ec2.describe_instances()
    print(ec2_instances)
    for i in range(len(ec2_instances['Reservations'])):
        for j in range(len(ec2_instances['Reservations'][i]['Instances'])):
            print("for i", i, " J is ", j)
            id = ec2_instances['Reservations'][i]['Instances'][j]['InstanceId']
            privateIp = ec2_instances['Reservations'][i]['Instances'][j]['PrivateIpAddress']
            state = ec2_instances['Reservations'][i]['Instances'][j]['State']['Name']
            if state == "running":
                publicIp = ec2_instances['Reservations'][i]['Instances'][j]['PublicIpAddress']
            else:
                publicIp = "None"
            name = ec2_instances['Reservations'][i]['Instances'][j]['Tags'][0]['Value']
            keyName = ec2_instances['Reservations'][i]['Instances'][j]['KeyName']

            instanceDict = {
                "Id": id,
                "Name": name,
                "State": state,
                "PublicIP": publicIp,
                "PrivateIP": privateIp,
                "KeyName": keyName,
                "RegionName": region_name
            }
            instance_detail.append(instanceDict)
    return instance_detail

# start instance in region
def start_instance(instance_id, region_name):
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region_name)
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
        # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# stop instance in region
def stop_instance(instance_id, region_name):
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                       region_name=region_name)
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


def get_all_regions():
    ec2 = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    all_regions = ec2.describe_regions()
    for region in all_regions['Regions']:
        all_regions.append[region['RegionName']]
        # print(region['RegionName'])
    return all_regions
