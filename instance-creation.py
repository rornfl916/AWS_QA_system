import boto3
import json
import time
from awsimages import image

with open('aws_credentials.json', 'r') as credentials_file:
    aws_credentials = json.load(credentials_file)

# EC2 클라이언트 생성
ec2 = boto3.client(
    'ec2',
    aws_access_key_id=aws_credentials['access_key'],
    aws_secret_access_key=aws_credentials['secret_key'],
    region_name=aws_credentials['region']
)

img = image(ec2, 'noble')

def creation_instance(ec2):                         # 인스턴스 생성
    response = ec2.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvdb',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeType': 'gp3',
                    'VolumeSize': 30,
                },
            }
        ],
        # ImageId='ami-0abcdef1234567890',            # 사용할 AMI ID
        ImageId=img.parse_with_image_name('noble',img.list_image(ec2))['ImageId'],
        InstanceType='t3.medium',                    # 인스턴스 타입
        MinCount=1,
        MaxCount=1,
        KeyName='RIM_Oracle',                       # 키 페어 이름
        SecurityGroupIds=['sg-0479d510c1aff0954'],  # 보안 그룹 ID
        SubnetId='subnet-03d47f9a2b3c8f0fa',        # 서브넷 ID
    )
    return response

instance_id = creation_instance(ec2)['Instances'][0]['InstanceId']
print(f"인스턴스 생성 완료: {instance_id}")

def terminate_instance(instance_id):                    # 인스턴스 삭제
    response = ec2.terminate_instances(
        InstanceIds=[
            instance_id                                 # 이전에 생성한 인스턴스 ID
        ],
        # DryRun=True|False                             # 실제 동작 여부
    )
    return response

time.sleep(300)
print("인스턴스 삭제 완료: ", terminate_instance(instance_id))