# https://gist.github.com/svrist/73e2d6175104f7ab4d201280acba049c
import os
from os import listdir
from os.path import isfile, join
import boto3
import json

from clint.textui import prompt, puts, colored, validators

boto3.setup_default_session(profile_name='stephen')
ec2_client = boto3.client('ec2')
cf_client = boto3.client('cloudformation')

def status_checks():
    # aws ec2 describe-instance-status --instance-ids i-1234567890abcdef0
    pass

def list_all_ec2():
    response = ec2_client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            puts(colored.blue(f'ec2 instance / {instance["InstanceId"]} / {get_instance_name(instance)} / {instance["State"]["Name"]}'))

def get_instance_name(instance):
    for tag in instance["Tags"]:
        if tag['Key'] == 'Name':
            return tag['Value']

def choose_ec2(attr='InstanceId'):
    response = ec2_client.describe_instances()
    ec2_type_options = []
    for i, reservation in enumerate(response["Reservations"], start=1):
        for j, instance in enumerate(reservation["Instances"], start=1):
            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]
            # print(instance)
            instance_name = get_instance_name(instance)
            ec2_type_options.append({'selector': i, 'prompt': f'{instance_name} / {instance_id} / {instance["InstanceType"]} / {state}', 'return': instance})

    selected_instance = prompt.options("Which ec2 instance", ec2_type_options)
    puts(colored.blue(f'You selected {selected_instance["InstanceId"]}'))
    return selected_instance

def choose_stack():
    stacks = cf_client.list_stacks()['StackSummaries']
    options = []
    idx = 1
    for stack in stacks:
        if stack['StackStatus'] != 'DELETE_COMPLETE':
           options.append({'selector': idx, 'prompt': stack['StackName'], 'return': stack['StackName']})
           idx += 1
    selected_stack = prompt.options("Which stack", options)
    puts(colored.blue(f'You selected {selected_stack}'))
    return selected_stack

def choose_from_list(file_list, message):
    options = []
    for i, file_name in enumerate(file_list, start=1):
        options.append({'selector': i, 'prompt': f'{file_name}', 'return': file_name})

    key = prompt.options(message, options)
    puts(colored.blue(f'You selected {key}'))
    return key

def validate_stack_exists(stack_name):
    stacks = cf_client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

def create_stack(stack_name):
    ec2_type_options = [
        {'selector': '1', 'prompt': 't2.small', 'return': 't2.small'},
        {'selector': '2', 'prompt': 't2.xlarge', 'return': 't2.xlarge'},
        {'selector': '3', 'prompt': 'p2.xlarge', 'return': 'p2.xlarge'},
        {'selector': '4', 'prompt': 'p3.2xlarge', 'return': 'p3.2xlarge'}
    ]
    ec2_type = prompt.options("What type of ec2 instance", ec2_type_options)

    puts(colored.cyan(f'You chose {ec2_type}'))
    template = get_template()
    image_id = 'ami-2fa95952' # Ubuntu nvidia-docker

    print(template)
    print(stack_name)
    my_keys = list_keypairs()
    key = choose_from_list(my_keys, 'Which key?')

    response = cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=json.dumps(template),
        Parameters=[
            {
                'ParameterKey': 'MyIdentifier',
                'ParameterValue': stack_name
            },
            {
                'ParameterKey': 'MyImageId',
                'ParameterValue': image_id
            },
            {
                'ParameterKey': 'InstanceType',
                'ParameterValue': ec2_type
            },
            {
                'ParameterKey': 'KeyName',
                'ParameterValue': key,
                'UsePreviousValue': True
            }
        ]
    )

    puts(colored.green(f'Creating stack {stack_name} with a {ec2_type} instance'))

def update_stack(stack_name):
    ec2_type_options = [
        {'selector': '1', 'prompt': 't2.small', 'return': 't2.small'},
        {'selector': '2', 'prompt': 't2.medium', 'return': 't2.medium'},
        {'selector': '3', 'prompt': 't2.xlarge', 'return': 't2.xlarge'},
        {'selector': '4', 'prompt': 'p2.xlarge', 'return': 'p2.xlarge'}
    ]
    ec2_type = prompt.options("Which stack?", ec2_type_options)

    puts(colored.cyan(f'You chose {ec2_type}'))
    template = get_template()
    image_id = 'ami-2fa95952' # Ubuntu nvidia-docker

    response = cf_client.update_stack(
        StackName=stack_name,
        TemplateBody=json.dumps(template),
        Parameters=[
            {
                'ParameterKey': 'MyIdentifier',
                'ParameterValue': stack_name
            },
            {
                'ParameterKey': 'MyImageId',
                'ParameterValue': image_id
            },
            {
                'ParameterKey': 'InstanceType',
                'ParameterValue': ec2_type
            },
            {
                'ParameterKey': 'KeyName',
                'ParameterValue': 'sj-mac-2017'
            }
        ]
    )

    puts(colored.green(f'Creating stack {stack_name} with a {ec2_type} instance'))

def delete_stack(stack_name):
    response = cf_client.delete_stack(StackName=stack_name)
    # TODO: check response to make sure 
    puts(colored.blue(f'Deleting stack {stack_name}'))

def get_template():
    """ 
    Loads a cloudformation template from file
    """
    with open('./accio/templates/mystack2.json') as json_data:
        template_data = json.load(json_data)
    template_str = json.dumps(template_data)
    cf_client.validate_template(TemplateBody=template_str)
    #return json.dumps(template)
    return template_data

def ssh_login():
    """
    Prompts for ec2 instance, then ssh into it
    """
    my_keys_path = os.path.expanduser('~/.ssh/')
    onlyfiles = [f for f in listdir(my_keys_path) if isfile(join(my_keys_path, f))]
    my_pem = choose_from_list(onlyfiles, "Which pem to access your instance?")
    ec2_instance = choose_ec2()
    public_ip = ec2_instance["PublicIpAddress"]
    puts(colored.green('Logging into  ') + str(public_ip) + '...')
    os.system(f'ssh -v -p 22 -i ~/.ssh/{my_pem} ubuntu@{public_ip}; exec bash')

def ssh_launch():
    pass

def list_keypairs():
    response = ec2_client.describe_key_pairs()
    my_keypairs = [k['KeyName'] for k in response['KeyPairs']]
    print(my_keypairs)
    return my_keypairs

def stop_ec2():
    ec2_instance = choose_ec2()
    ec2_instance_id = ec2_instance["InstanceId"]

    ec2_client.stop_instances(InstanceIds=[ec2_instance_id])
    puts(colored.green('Stopping ') + str(ec2_instance_id) + '...')

def start_ec2():
    ec2_instance = choose_ec2()
    ec2_instance_id = ec2_instance["InstanceId"]

    ec2_client.start_instances(InstanceIds=[ec2_instance_id])
    puts(colored.green('Starting ') + str(ec2_instance_id) + '...')

def attach_volume():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    volumes = ec2.volumes.all()
    for vol in volumes:
        puts(colored.green('Volumes ') + str(vol))
    # ec2_client.attach_volume(volume_id, instance_id, 'dev/sda1')

def create_ecr_registry(registry_name='mystack/repo'):
    ecr_client = boto3.client('ecr')
    ecr_client.create_repository(repositoryName=registry_name)

def push_image():
    """
    WIP
    """
    ecr_repo = 'aws_account_id.dkr.ecr.region.amazonaws.com/my-web-app'
    os.system(f'docker push {ecr_repo}')

def upload_keys():
    """
    Uploads keys from local ~/.ssh/xyz to remote ec2
    """
    my_keys_path = os.path.expanduser('~/.ssh/')
    onlyfiles = [f for f in listdir(my_keys_path) if isfile(join(my_keys_path, f))]
    key_upload = choose_from_list(onlyfiles, "Which key do you want to upload?")
    ec2_instance = choose_ec2()
    my_pem = choose_from_list(onlyfiles, "Which pem to access your instance?")
    public_ip = ec2_instance["PublicIpAddress"]
    local_key = 'id_rsa_ec2'
    puts(colored.green(f'Uploading keys to {str(public_ip)} ...'))
    os.system(f'scp -i ~/.ssh/{my_pem} ~/.ssh/{key_upload} ubuntu@{public_ip}:~/.ssh/id_rsa')

def scp():
    """
    scp local file to remote ec2
    """
    ec2_instance = choose_ec2()
    my_keys_path = os.path.expanduser('~/.ssh/')
    onlyfiles = [f for f in listdir(my_keys_path) if isfile(join(my_keys_path, f))]
    my_pem = choose_from_list(onlyfiles, "Which pem to access your instance?")
    public_ip = ec2_instance["PublicIpAddress"]
    local_file = prompt.query("What file to upload (enter full path)?")
    if not os.path.exists(local_file):
        puts(colored.green(f'Local file {local_file} does not exists'))
        return
    remote_path = prompt.query("Enter path on remote to upload to?")
    puts(colored.green(f'Uploading local file ({local_file}) to {str(public_ip)} ...'))
    os.system(f'scp -i ~/.ssh/{my_pem} {local_file} ubuntu@{public_ip}:{remote_path}')

def tag_image():
    """
    WIP
    """
    image_hash = 'abc'
    ecr_repo = 'aws_account_id.dkr.ecr.region.amazonaws.com/my-web-app'
    os.system(f'docker tag {image_hash} {ecr_repo}')
