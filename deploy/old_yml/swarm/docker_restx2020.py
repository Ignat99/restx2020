#!/usr/bin/env python
# coding: utf-8

"""
    docker_alert.py file for
    running docker container
    with tests
"""

from __future__ import print_function
import os
import os.path
import json
import click
import docker

HERE = os.path.dirname(__file__)
#dockerfile = os.path.join(here, 'test')
DOCKERFILE = HERE
#docker_client = docker.from_env()
#docker_client = docker.Client(base_url='unix://var/run/docker.sock')
DOCKER_CLIENT = docker.APIClient(base_url='unix://var/run/docker.sock')
#generator = docker_client.images.build(path=dockerfile, tag='restx2020:latest', rm=True)
#generator = docker_client.build(path=dockerfile, tag='restx2020:v.0.9', rm=True)
GENERATOR = DOCKER_CLIENT.build(path=DOCKERFILE, tag='restx2020:latest', rm=True)

def circle():
    """Print output"""
    while True:
        try:
            output = GENERATOR.next()
            output = output.strip('\r\n')
            json_output = json.loads(output)
            if 'stream' in json_output:
                click.echo(json_output['stream'].strip('\n'))
        except StopIteration:
#            click.echo("Docker image build complete.")
            return "Docker image build complete."
        except ValueError:
#            click.echo("Error parsing output from docker image build: %s" % output)
            return "Error parsing output from docker image build: %s" % output
    return "Exit"

MESSAGE = circle()
#for chunk in generator:
#    if 'stream' in chunk:
#        for message in chunk['stream'].splitlines():
#            print(message)
#message = json.loads(generator)
print(MESSAGE)


#try:
#docker_client.images.remove('restx2020:latest')
#docker_client.remove_container('restx2020')
#except docker.errors.NotFound as ex:
#    print(ex)
#    raise

#docker_client.create_container('restx2020:v.0.9', '/bin/sleep 30', name='restx2020')
# command='./start.sh',





#docker_client.create_network('deploy_default', driver="bridge", internal=True)

#docker_client.create_container(image='restx2020:latest', \
#, links={
#    'deploy_database_1': 'database'
#}
#        links={'deploy_database_1': '172.20.0.3'}
#links={'deploy_database_1': '172.20.0.3'},



#ports=[(8086, 'tcp'), (8085, 'tcp')],

LINKS = [('deploy_database_1', 'database')]


#docker_client.containers.run(image='restx2020:latest', \
DOCKER_CLIENT.create_container(image='restx2020:latest', \
environment=["SQL_HOST=\"database\"", "DB_PASS=\"test\"", "DB_USER=\"test\"", "DB_PORT=3306", \
"DB_NAME=\"insikt\""], name='restx2020',  \
detach=True, stdin_open=True, tty=True, \
networking_config=DOCKER_CLIENT.create_networking_config({
    'deploy_default': DOCKER_CLIENT.create_endpoint_config(
        links=LINKS
    )
}), \
host_config=DOCKER_CLIENT.create_host_config(links=LINKS, \
port_bindings={
    '8032/tcp': ("", 8032),
    '8033/tcp': ("", 8033)
}, \
restart_policy={
    "Name": "no",
    "MaximumRetryCount": 0
}, dns=[], dns_search=[], dns_opt=[], blkio_weight_device=[], devices=[], \
network_mode='deploy_default'
                                            ) \
)
#hostname="lain.insiktintelligence.com")
#docker_client.port('deploy_database_1', 3306)
#docker_client.port('restx2020', 3306)
#docker_client.start('restx2020')
#docker_client.top('restx2020')
