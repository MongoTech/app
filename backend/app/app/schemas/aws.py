from typing import Optional

from pydantic import BaseModel

from app import configs


class Ec2Auth(BaseModel):
    access_key_id: str
    secret_access_key: str
    region: Optional[str] = configs.AWS_REGION_NAME


class Ec2Create(Ec2Auth):
    image_id: Optional[str] = configs.EC2_IMAGE_ID
    min_count: Optional[int] = configs.EC2_MIN_COUNT
    max_count: Optional[int] = configs.EC2_MAX_COUNT
    instance_type: Optional[str] = configs.EC2_INSTANCE_TYPE
    key_name: str
    security_group_name: Optional[str]
    volume_size: Optional[int] = configs.EBS_VOLUME_SIZE


class KeyPairCreate(Ec2Auth):
    key_name: str


class SecurityGroupCreate(Ec2Auth):
    group_name: str
    description: str
    vpc_id: Optional[str]


class SecurityGroupConfigure(Ec2Auth):
    cidr_ip_inbound: Optional[str] = configs.EC2_CIDR_IP
    inbound_description: Optional[str]
    from_port_inbound: int
    to_port_inbound: int
    cidr_ip_outbound: Optional[str] = configs.EC2_CIDR_IP
    outbound_description: Optional[str]
    from_port_outbound: int
    to_port_outbound: int
