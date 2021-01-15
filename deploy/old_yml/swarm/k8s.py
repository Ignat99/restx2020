#!/usr/bin/python

"""
Instalation Kubernetes : k8s.py

https://medium.appbase.io/deploy-elasticsearch-with-kubernetes-on-aws-in-10-steps-7913b607abda
https://habr.com/es/company/southbrige/blog/416643/
"""

from __future__ import print_function
import os
from postgres import select_from
from insikt import run_commands, H5, \
S3PROFILE, UBUNTU, AWS_CONF_NAME, AWS_CREDENTIALS_NAME


def kops(host):
    """Install tools awscli, kops"""
    run_commands(host, 'pip install awscli --upgrade --user')
    run_commands(host, "wget -O kops https://github.com/kubernetes/kops/releases/download/$(curl \
-s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d \'\"\' \
-f 4)/kops-linux-amd64")
    run_commands(host, 'chmod +x ./kops')
    run_commands(host, 'sudo mv ./kops /usr/local/bin/')

def kubectl(host):
    """Install tools kubectl"""
#    run_commands(host, 'pip install awscli --upgrade --user')
    run_commands(host, "wget -O kubectl \
https://storage.googleapis.com/kubernetes-release/release/$(curl \
-s https://storage.googleapis.com/kubernetes-release/stable.txt)/bin/linux/amd64/kubectl")
    run_commands(host, 'chmod +x ./kubectl')
    run_commands(host, 'sudo mv ./kubectl /usr/local/bin/kubectl')

def aws_iam(host):
    """Build cluster within AWS, create a dedicated IAM user for kops.
    Require the following IAM permissions:
    AmazonEC2FullAccess
    AmazonRoute53FullAccess
    AmazonS3FullAccess
    IAMFullAccess
    AmazonVPCFullAccess

    """
    run_commands(host, '$(aws ecr get-login --no-include-email --region eu-west-1)')
    run_commands(host, 'aws iam create-group --group-name kops')
    run_commands(host, 'aws iam attach-group-policy \
--policy-arn arn:aws:iam:aws:policy/AmazonEC2FullAccess  --group-name kops')
    run_commands(host, 'aws iam attach-group-policy \
--policy-arn arn:aws:iam:aws:policy/AmazonRoute53FullAccess  --group-name kops')
    run_commands(host, 'aws iam attach-group-policy \
--policy-arn arn:aws:iam:aws:policy/AmazonS3FullAccess  --group-name kops')
    run_commands(host, 'aws iam attach-group-policy \
--policy-arn arn:aws:iam:aws:policy/IAMFullAccess  --group-name kops')
    run_commands(host, 'aws iam attach-group-policy \
--policy-arn arn:aws:iam:aws:policy/AmazonVPCFullAccess  --group-name kops')
    run_commands(host, 'aws iam create-user --user-name kops')
    run_commands(host, 'aws iam add-user-to-group --user-name kops --group-name kops')
    run_commands(host, 'aws iam create-access-key --user-name kops')
    sout = run_commands(host, 'aws iam list-users')
    if sout == kops:
        print("User kops created")
        run_commands(host, 'export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)')
        run_commands(host, \
'export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)')

def configuring_dns():
    """
    If we plan to use a sub-domain of our hosted domain: insiktintelligence.com,
    you will have to create a second public hosted zone.
    https://github.com/kubernetes/kops/blob/master/docs/aws.md#configure-dns
    """
    pass


def insiktcluster(host):
    """Creating Kubernetes cluster with 1 master and 3 nodes"""
# insiktcluster.insiktintelligence.com if setup DNS
    run_commands(host, 'export NAME=insiktcluster.k8s.local')
    run_commands(host, 'export KOPS_STATE_STORE=s3://insiktbucket')
    run_commands(host, 'aws ec2 describe-availability-zones --region eu-west-1')
#    run_commands(host, 'kops create cluster --zones eu-west-1c --node-count 3 \
#--dns private ${NAME}')
    sout = run_commands(host, "kops create cluster --zones eu-west-1c --node-count 3 ${NAME}")
    if sout == 'ready':
        print("Cluster is starting")

def check_cluster(host):
    """Cluster Validation"""
    sout = run_commands(host, 'kops validate cluster')
    if sout == 'ready':
        print("Cluster is ready")
    sout = run_commands(host, 'kops get nodes')
    if sout == 'Ready':
        print("Nodes is ready")
    sout = run_commands(host, 'kops get pods')
    if sout == 'Running':
        print("Pods is running")

def k8s_es(host):
    """Deploy Elasticsearch cluster on K8S"""
#    os.system('scp ' + ES_STATEFULSET_NAME + ' ' + UBUNTU + '@' + host + ':/home/' + UBUNTU)
#    os.system('scp ' + ES_SVC_NAME + ' ' + UBUNTU + '@' + host + ':/home/' + UBUNTU)
    run_commands(host, 'cd /home/' + UBUNTU + '/ ; kubectl create -f es-statefulset.yaml')
    run_commands(host, 'cd /home/' + UBUNTU + '/ ; kubectl create -f es-svc.yaml')
    sout = run_commands(host, 'kubectl describe service elasticsearch')
    if sout == 'balancer':
        print("EnsuringLoadBalancer is starting")


def run_instances(host):
    """ Start new instance """
    run_commands(host, 'aws ec2 run-instances  --image-id ami-1624987f  --max-count 1 \
--min-count 1 --key-name insikt6 --instance-type m5.4xlage')
# Zone of HD must be the same with instance
    run_commands(host, 'aws ec2 create-volume  --availability-zone eu-west-1c --size 20')
    run_commands(host, 'aws ec2 attach-volume --instance-id i-2bc0925b --volume-id vol-08ab3079  \
--device /dev/xvdf')
    run_commands(host, 'mkfs.ext3 /dev/xvdf')
    run_commands(host, 'mkdir /mnt/ubuntu-image')
    run_commands(host, 'mount /dev/xvdf /mnt/ubuntu-image')

def aws_cli(host):
    """Configuring the AWS CLI"""
    print(run_commands(host, 'sudo apt -y install python-pip'))
    run_commands(host, 'sudo pip install awscli')

    run_commands(host, 'mkdir /home/' + UBUNTU + '/.aws')
    print(select_from('keys', 'access_token_key', '7'))
    print(select_from('keys', 'access_token_secret', '7'))
    os.system('scp ' + AWS_CONF_NAME + ' ' + UBUNTU + '@' + host + ':/home/' + UBUNTU + '/.aws')
    os.system('scp ' + AWS_CREDENTIALS_NAME + ' ' + UBUNTU + '@' + host + ':/home/' + \
UBUNTU + '/.aws')
    print(run_commands(host, 'aws s3 ls --profile ' + S3PROFILE))


def s3_bucket(host):
    """This bucket will become the source of truth for our cluster configuration"""
    run_commands(host, 'aws s3api create-bucket --bucket insiktbucket --region eu-west-1 \
--create-bucket-configuration LocationConstraint=eu-west-1 --profile ' + S3PROFILE)
    run_commands(host, 'aws s3api put-bucket-versioning --bucket insiktbucket \
--versioning-configuration Status=Enabled --profile ' + S3PROFILE)
    print(run_commands(host, 'aws s3 ls --profile ' + S3PROFILE))

def s3_backup(host):
    """Create backup of home dir and etc"""
#    run_commands(host, 'export KOPS_STATE_STORE=s3://insiktbucket')
    print(run_commands(host, 'aws s3 ls --profile ' + S3PROFILE))
    cur_dir = '/home'
    run_commands(host, 'aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + cur_dir + \
' --profile ' + S3PROFILE)
    cur_dir = '/etc'
    run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + cur_dir + \
' --profile ' + S3PROFILE)
    cur_dir = '/opt'
    run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + cur_dir + \
' --profile ' + S3PROFILE)
    cur_dir = '/var/lib'
    print(run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + \
cur_dir + ' --profile ' + S3PROFILE))
# /var/lib/[jenkins,postgres,zookeeper]
    cur_dir = '/root'
    print(run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + \
cur_dir + ' --profile ' + S3PROFILE))
    cur_dir = '/var/log'
    print(run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + \
cur_dir + ' --profile ' + S3PROFILE))
    cur_dir = '/usr'
    print(run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + \
cur_dir + ' --profile ' + S3PROFILE))
    cur_dir = '/tmp'
    print(run_commands(host, 'sudo aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + \
cur_dir + ' --profile ' + S3PROFILE))
#    cur_dir = '/home/ubuntu/NLP_Engine'
#    run_commands(host, 'aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + cur_dir + \
#' --profile ' + S3PROFILE)
#    cur_dir = '/home/ubuntu/nlp_engine'
#    run_commands(host, 'aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + cur_dir + \
#' --profile ' + S3PROFILE)
#    cur_dir = '/home/ubuntu/nltk_data'
#    run_commands(host, 'aws s3 sync ' + cur_dir + ' s3://insiktbucket/' + host + cur_dir + \
#' --profile ' + S3PROFILE)


def main():
    """Do some things"""
#    aws_cli(H1)
#    s3_bucket(H5)
#    s3_backup(H1)

#    aws_cli(H2)
#    s3_backup(H2)
#    aws_cli(H3)
#    s3_backup(H3)
#    aws_cli(H4)
#    s3_backup(H4)
    aws_cli(H5)
    s3_backup(H5)


if __name__ == "__main__":
    main()
