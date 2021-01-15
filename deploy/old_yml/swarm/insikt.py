#!/usr/bin/python

"""
Insikt settings and running : insikt.py

"""

from __future__ import print_function
import os
import sys
import json as j
from collections import namedtuple
import base64
#import getpass
#import socket
#import traceback
import requests
import paramiko
#from paramiko.py3compat import input
#import interactive
#from postgres import select_from

JENKINS = "jenkins"
DEBIAN = "debian"
UBUNTU = "ubuntu"
S3PROFILE = "dimitrii"
PUB_KEY = '/home/' + UBUNTU + '/.ssh/authorized_keys'
STORM_DIR = '/opt/storm'
STORM_TAR = '/opt/storm/c.tar.gz'
STORM_TAR_NAME = '/home/' + UBUNTU + '/c.tar.gz'
STORM_VERSION = '1.0.6'
SUPERVISOR_TAR_NAME = '/home/' + UBUNTU + '/s.tar.gz'
SUPERVISOR = 'supervisor'
ZOO_CONF = '/etc/zookeeper/conf/zoo.cfg'
ZOO_CONF_NAME = '/home/' + UBUNTU + '/zoo.cfg'
POS_ZOO_CONF = '19'
POS_ZOO_CONF_GITHUB = '26'
ZOO_CONF_GITHUB = '/home/ubuntu/zookeeper/bin/../conf/zoo.cfg'
ZOO_PROCESS = 'org.apache.zookeeper.server.quorum'
STORM_CONF = '/opt/storm/current/conf/storm.yaml'
STORM_CONF_NAME = '/home/' + UBUNTU + '/storm.yaml'
STORM_PROCESS = 'org.apache.storm.daemon.nimbus'
POS_STORM = '25'
ZOOKEEPER = 'zookeeper zookeeper-bin zookeeperd libzookeeper-java'
ES_CONF_NAME = '/home/' + UBUNTU + '/elasticsearch.yml'
KIBANA_CONF_NAME = '/home/' + UBUNTU + '/kibana.yml'
ES_STATEFULSET_NAME = '/home/' + UBUNTU + '/es-statefulset.yaml'
ES_SVC_NAME = '/home/' + UBUNTU + '/es-svc.yaml'
AWS_CONF_NAME = '/home/' + UBUNTU + '/.aws/config'
AWS_CREDENTIALS_NAME = '/home/' + UBUNTU + '/.aws/credentials'

H1 = '34.240.211.245'
H1L = '172.31.20.58'
H2 = '34.246.99.181'
H2L = '172.31.8.61'
H3 = '18.202.76.77'
H3L = '172.31.27.112'
H4 = '18.202.142.8'
H4L = '172.31.43.114'
H5 = '34.244.227.59'
H5L = '172.31.23.102'
H6 = 'insikt6'
H7 = 'insikt7'
H8 = 'insikt8'
L1 = '192.168.0.165'
LOCALHOST = 'localhost'

HOSTNAME = H4


HOSTS = [H5]

try:
    os.environ["PASS"]
except KeyError:
    print("Please set the environment variable PASS")
    sys.exit(1)

Prc = namedtuple('prc', 'proc pos cont')



PUB_KEY = "/home/" + UBUNTU + "/.ssh/id_rsa.pub"

def my_key(key_file):
    """ Read my public key. """
    pub_key_file = open(key_file, 'r')
    pub_key = pub_key_file.read()
    pub_key_file.close()
    return pub_key.split(' ')[1]

#.split('==')[0]

PUB_KEY1 = my_key(PUB_KEY)

#print(PUB_KEY1)


def my_connect(pub_key):
    """ That is function not work, look to demo_simple.py """
    key = paramiko.RSAKey(data=base64.b64decode(pub_key))
    client = paramiko.SSHClient()
    client.get_host_keys().add('spp-main.insiktintelligence.com', 'ssh-rsa', key)
    client.connect('spp-main.insiktintelligence.com', 22, username='ubuntu', password='')
    stdout = client.exec_command('ls')[1]
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()



def run_commands(hostname, command_list):
    """Distance running list of command"""

    # setup logging
    paramiko.util.log_to_file("demo_simple.log")
    # Paramiko client configuration
    #UseGSSAPI = (
    #    paramiko.GSS_AUTH_AVAILABLE
    #)  # enable "gssapi-with-mic" authentication, if supported by your python installation
    #DoGSSAPIKeyExchange = (
    #    paramiko.GSS_AUTH_AVAILABLE
    #)  # enable "gssapi-kex" key exchange, if supported by your python installation
    # UseGSSAPI = False
    # DoGSSAPIKeyExchange = False

    # get hostname
    username = UBUNTU
    port = 22
    sout = ""
    password = os.environ["PASS"]


    #if not UseGSSAPI and not DoGSSAPIKeyExchange:
    #    password = PASS


    # now, connect and use paramiko Client to negotiate SSH2 across the connection
#    try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print("*** Connecting...")
        #if not UseGSSAPI and not DoGSSAPIKeyExchange:
    client.connect(hostname, port, username, password)
#        else:
#            try:
#                client.connect(
#                    hostname,
#                    port,
#                    username,
#                    gss_auth=UseGSSAPI,
#                    gss_kex=DoGSSAPIKeyExchange,
#                )
#            except Exception:
                # traceback.print_exc()
#                    client.connect(hostname, port, username, password)

        #chan = client.invoke_shell()
        #print(repr(client.get_transport()))
    print("*** Here we go!\n")
        #interactive.interactive_shell(chan)
        #chan.close()
        # that is place for command on Nimbus servers:
    stdout = client.exec_command(command_list)[1]
    for line in stdout:
        sout = sout + ' ' + line.strip('\n')
    client.close()
    return sout

#    except Exception as error:
#        print("*** Caught exception: %s: %s" % (error.__class__, error))
#        traceback.print_exc()
#        try:
#        client.close()
#        except:
#            pass


def check_file_location(host, path_name):
    """Put file to right folder"""
    sout = run_commands(host, "ls " + path_name)
    return sout


def check_file_content(host, path_name, some_filter):
    """ Put file to right folder """
    sout = run_commands(host, "cat " + path_name + '| grep ' + some_filter)
    return sout


def check_process(host, process, pos):
    """Look to list of running process"""
    sout = run_commands(host, "ps aux | grep " + process + " | grep  -v grep | awk \'{print $" + \
pos + "}\'")
    return sout

def kotlin_login(host):
    """login kotlin"""
    res = requests.post("http://" + host + ":8090/api/login", \
    data=j.dumps({'username': 'parronator', 'password': '123456Aa'}), \
    headers={'content-type': 'application/json', 'Accept': '*/*'})
    print(res.status_code, res.reason)
    print(res.text)
# For get thoken
    json_t = j.loads(res.text)
    print (json_t)
    print (json_t['login']['access_token'])
    token_access = json_t['login']['access_token']

    print(j.dumps(dict(res.headers)))
    print(res.url)
    print("========================================")
    return token_access


def main():
    """Do some things"""
    pass


if __name__ == "__main__":
    main()
