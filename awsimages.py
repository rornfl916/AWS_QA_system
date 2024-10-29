import boto3
import json
from datetime import datetime

### 포함되어야 하지 않는 문자열 리스트
parse = [
    "elasticbeanstalk",
    "deep learning",
    "sql",
    "eks",
    "k8s",
    "gpu",
    "arm",
    "ecs",
    "cluster",
    "macos",
    "gaming",
    "cloud9",
    "spanish",
    "gateway",
    "tpm",
    "arm",
    "chinese",
    "spanish",
    "hungarian",
    "nat",
    "nvidia",
    "ha",
    "byos",
    "backport",
    "sap",
    "hyper-v",
    "tensorflow",
    "datasync",
    "russian",
    "japanese",
    "italian",
    "czech",
    "german",
    "korean",
    "brazil",
    "turkish",
    "portugal",
    "dutch",
    "polish",
    "stig",
    "swedish",
    "french",
    "desktop",
    "graphic",
    "dcv",
    "dotnet",
    "pro",
    "unsupported",
    "enforcing",
    "minimal",
    "aarch64",
    "kurian",
    "ioanyt",
    "nginx",
    "zendphp",
    "cognosys",
    "based",
    "php",
    "isms",
    "container",
    "docker",
    "jdk",
    "java",
    "free",
    "bsd",
    "node",
    "zend",
    "made",
    "rust",
    "apps4rent",
    "locust",
    "rancher",
    "askforcloud",
]

# with open('C:/Users/JAESEONGSHIN/OneDrive - ZConverter Inc/자동화/cloud/AWS/aws_credentials.json', 'r') as credentials_file:
#     aws_credentials = json.load(credentials_file)

# ec2 = boto3.client(
#     'ec2',
#     aws_access_key_id=aws_credentials['access_key'],
#     aws_secret_access_key=aws_credentials['secret_key'],
#     region_name=aws_credentials['region']
# )

class image:
    def __init__(self, ec2, name):
        self.ec2 = ec2
        self.name = name
    

    ### boto describe_images(이미지 가져오기)
    def describe_images(self, ec2):
        response = ec2.describe_images(
            ExecutableUsers=[
                'all',
            ],
            # Owners=[
            #     'amazon',
            # ],
            Filters=[
                {
                    'Name': 'architecture',
                    'Values': [
                        'x86_64',
                    ],
                    # 'Name': 'owner-alias',
                    # 'Values': [
                    #     'amazon',
                    # ],
                    'Name': 'virtualization-type',
                    'Values': [
                        'hvm',
                    ],
                    'Name': 'root-device-type',
                    'Values': [
                        'ebs',
                    ],
                    'Name': 'state',
                    'Values': [
                        'available',
                    ],
                    'Name': 'image-type',
                    'Values': [
                        'machine',
                    ],
                    'Name': 'is-public',
                    'Values': [
                        'true'
                    ],
                    'Name': 'ena-support',
                    'Values': [
                        'true'
                    ],
                    # 'Name': 'creation-date',
                    # 'Values': [
                    #     '2024-*'
                    # ],
                },
            ],
            IncludeDeprecated=False,
        )

        return response

    def parsing(self, string, string_list):
        return any(substring in string for substring in string_list)

    # 이미지의 Name과 Description을 기준으로 위의 string_list에 포함되면 그냥 넘기고 아니라면 images 리스트에 append
    def list_image(self, ec2):
        images = []
        for i in self.describe_images(ec2)['Images']:
            try:
                if self.parsing(i['Name'].lower(), parse):
                    continue
                elif self.parsing(i['Description'].lower(), parse):
                    continue
            ### 이미지 정보 저장 용도의 list에 append로 필요한 정보들 dict 형태로 입력
                images.append(
                    {
                    'Description': i['Description'],
                    'Name': i['Name'],
                    'ImageId': i['ImageId'],
                    'CreationDate': i['CreationDate']
                    }
                )
            except:
                continue
        return images


    # CreationDate 기준으로 최신 이미지 받아와야 함.
    # 현재 이미지도 Ubuntu, SUSE, Amzn, Debian을 전부 가져오기 때문에 특정 기준으로 parsing을 해주어야 함


    def parse_with_image_name(self, os_name, image_list):
        parsed_image = []
        for i in image_list:
            if os_name.lower() in i['Name'].lower():
                parsed_image.append(i)
        time_data = [i['CreationDate'] for i in parsed_image]
        time_data = [datetime.fromisoformat(time[:-1]) for time in time_data]
        latest_time_index = time_data.index(max(time_data))
        return parsed_image[latest_time_index]
