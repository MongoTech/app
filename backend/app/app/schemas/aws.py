from typing import Optional

from pydantic import BaseModel

from app import configs


class Ec2Auth(BaseModel):
    access_key_id: str
    secret_access_key: str
    region: Optional[str] = configs.AWS_REGION_NAME


class Ec2Create(Ec2Auth):
    image_id: Optional[str] = configs.EC2_IMAGE_ID
    min_count: Optional[int] = 1
    max_count: Optional[int] = 1
    instance_type: Optional[str] = configs.EC2_INSTANCE_TYPE
    key_name: str


class KeyPairCreate(Ec2Auth):
    key_name: str


class SecurityGroupCreate(Ec2Auth):
    group_name: str
    description: str
    vpc_id: Optional[str]
