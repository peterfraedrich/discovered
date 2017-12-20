#!/usr/bin/env python3

import redis
import time
import json
import psutil
import socket
import platform
import os
import datetime
import sys

class ServiceDiscovery:
    '''
    uses Redis for easy service discovery and lookup
    by service name
    '''

    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0, redis_auth=None, ttl=-1, service_group='default', auto=True):
        '''
        @param redis_host str
        @param redis_port int
        @param redis_db int
        @param redis_auth str
        @param ttl int
        @param service_group str
        @param auto bool
        sets up a new service discovery connection
        '''
        self.ttl = ttl
        self.auto = auto
        self.sg = 'discovered:{}'.format(service_group)
        self.r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_auth)
        self.r.set('{}:{}'.format(self.sg, 'sd_init'), time.time())
        return

    def register_service(self, service_name, endpoint, auth_type='', auth_credentials='', backend='', description=''):
        '''
        @param service_name str
        @param endpoint str
        @param auth_type str
        @param auth_credentials str
        @param backend str
        @param description str
        registeres a new service with SD
        '''
        info = {
            'endpoint' : endpoint,
            'auth_type' : auth_type,
            'auth_credentials' : auth_credentials,
            'backend' : backend,
            'description' : description
        }   
        self.r.hmset('{}:{}:{}'.format(self.sg, service_name, 'info'), info)
        return

    def register_node(self, service_name, node_name, ip=None, fqdn=None, os=None, platform_name=None, arch=None, cpu_count=None, memory=None, last_boot=None):
        '''
        @param service_name str
        @param node_name str
        @param node_details str
        @returns none
        Registers a node with a service; creates a service
        if its the first node.
        '''
        info = {
            'node_name' : node_name,
            'ip' : [ ip ],
            'fqdn' : fqdn,
            'os' : os,
            'platform' : platform_name,
            'arch' : arch,
            'cpu_count' : cpu_count,
            'memory' : memory,
            'last_boot' : last_boot,
            'py_version' : platform.python_version(),
            'py_name' : __name__,
            'py_args' : sys.argv
        }
        if self.auto:
            ip = []
            for name,iface in psutil.net_if_addrs().iteritems():
                for obj in iface:
                    if obj.family == 2:
                        ip.append(obj.address)
            info['ip'] = ip
            info['fqdn'] = socket.getfqdn()
            info['os'] = platform.system()
            if info['os'] == 'Linux':
                info['platform'] = '{} ({})'.format(platform.platform(), platform.linux_distribution()[0])
            else:
                info['platform'] = platform.platform()
            info['arch'] = platform.architecture()[0]
            info['cpu_count'] = psutil.cpu_count()
            info['memory'] = int(psutil.virtual_memory().total) / 1048576 
            info['last_boot'] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        self.r.hmset('{}:{}:{}:{}'.format(self.sg, service_name, 'nodes', node_name), info)
        if self.ttl != -1:
            self.r.expire('{}:{}:{}:{}'.format(self.sg, service_name, 'nodes', node_name), self.ttl)
        return

    def get_service(self, service_name):
        '''
        @param service_name str
        returns service info
        '''
        return self.r.hgetall('{}:{}:{}'.format(self.sg, service_name, 'info'))

    def get_nodes(self, service_name):
        '''
        @param service_name str
        returns nodes in a service
        '''
        nodes = []
        for node in self.r.scan_iter('{}:{}:{}:*'.format(self.sg, service_name, 'nodes')):
            nodes.append(self.r.hgetall(node))
        return nodes
