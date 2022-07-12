from typing import Union

import boto3
from fastapi import APIRouter

from app.schemas.aws import Ec2Create, KeyPairCreate, SecurityGroupCreate, SecurityGroupConfigure

router = APIRouter()


@router.post("/create-ec2-instance")
def create_ec2_instance(body: Ec2Create) -> Union[Exception, dict]:
    """
    Create aws EC2 instance
    """
    try:
        ec2_resource = boto3.resource(
            "ec2",
            aws_access_key_id=body.access_key_id,
            aws_secret_access_key=body.secret_access_key,
            region_name=body.region,
        )
        ec2_instance = ec2_resource.create_instances(
            ImageId=body.image_id,
            MinCount=body.min_count,
            MaxCount=body.max_count,
            InstanceType=body.instance_type,
            KeyName=body.key_name,
            BlockDeviceMappings=[
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeSize": body.volume_size,
                    },
                },
            ],
            SecurityGroups=[body.security_group_name]
        )
    except Exception as exc:
        return exc
    return {"EC2_instance_id": ec2_instance[0].id}


@router.post("/create-key-pair")
def create_key_pair(body: KeyPairCreate) -> Union[Exception, dict]:
    """
    Create aws KeyPair
    """
    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=body.access_key_id,
            aws_secret_access_key=body.secret_access_key,
            region_name=body.region,
        )
        key_pair = ec2_client.create_key_pair(KeyName=body.key_name)
    except Exception as exc:
        return exc
    return {
        "KeyMaterial": key_pair.get("KeyMaterial"),
        "KeyName": key_pair.get("KeyName"),
        "KeyPairId": key_pair.get("KeyPairId"),
    }


@router.post("/create-security-group")
def create_security_group(body: SecurityGroupCreate) -> Union[Exception, dict]:
    """
    Create aws security group
    """
    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=body.access_key_id,
            aws_secret_access_key=body.secret_access_key,
            region_name=body.region,
        )
        vpc_id = body.vpc_id
        if not vpc_id:
            existing_security_groups = ec2_client.describe_security_groups()
            vpc_id = existing_security_groups["SecurityGroups"][0].get("VpcId")
        security_group = ec2_client.create_security_group(
            GroupName=body.group_name, Description=body.description, VpcId=vpc_id
        )
    except Exception as exc:
        return exc
    return {"GroupId": security_group.get("GroupId")}


@router.post("/configure-security-group/{group_id}")
def configure_security_group(group_id: str, body: SecurityGroupConfigure) -> Union[Exception, dict]:
    """
    Configure inbound/outbound rules in aws security group
    """
    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=body.access_key_id,
            aws_secret_access_key=body.secret_access_key,
            region_name=body.region,
        )
        ec2_client.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": body.from_port_inbound,
                    "ToPort": body.to_port_inbound,
                    "IpRanges": [{
                        "CidrIp": body.cidr_ip_inbound,
                        "Description": body.inbound_description,
                    }],
                },
            ]
        )
        ec2_client.authorize_security_group_egress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": body.from_port_outbound,
                    "ToPort": body.to_port_outbound,
                    "IpRanges": [{
                        "CidrIp": body.cidr_ip_outbound,
                        "Description": body.outbound_description,
                    }],
                },
            ]
        )
    except Exception as exc:
        return exc
    return {"SecurityGroups": ec2_client.describe_security_groups(GroupIds=[group_id]).get("SecurityGroups")}
