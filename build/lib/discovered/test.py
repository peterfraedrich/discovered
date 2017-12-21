#!/usr/bin/env

from __future__ import print_function
from pprint import pprint
import discovered


sd = discovered.ServiceDiscovery()

print('register service')
x = sd.register_service(service_name='redis', endpoint='localhost:6379', endpoint_type='keystore', backend='redis', description='redis keystore')
pprint(x)

print('register node')
y = sd.register_node(service_name='redis', node_name='r0')
pprint(y)

print('get service')
z = sd.get_service('redis')
pprint(z)

print('get nodes')
q = sd.get_nodes('redis')
pprint(q)

print('list services')
w = sd.list_services()
pprint(w)

print('list groups')
e = sd.list_service_groups()
pprint(e)

print('remove node')
r = sd.remove_node('redis', 'r0')
pprint(r)

print('remove svc')
t = sd.remove_service('redis')
pprint(t)

print('remove group')
u = sd.remove_service_group('default')
pprint(u)