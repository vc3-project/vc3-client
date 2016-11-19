#!/usr/bin/env python 

from vc3client.lib.accounts import Accounts
from vc3client.lib.clusters import Clusters
from vc3client.lib.resources import  Resources
from vc3client.lib.specs import Specs
from vc3client.lib.users import Users

import argparse

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')

# A create-cluster command
create_parser = subparsers.add_parser('create-cluster', help='Create a cluster')
create_parser.add_argument('-c', default=False, action='store', dest='cluster_specs', help='file with cluster specifications',)
create_parser.add_argument('-r', default=False, action='store', dest='resource_specs', help='file with resources specifications',)
create_parser.add_argument('-p', default=False, action='store', dest='policy', help='file with policies',)


# A destroy-cluster command
create_parser = subparsers.add_parser('destroy-cluster', help='Destroy a cluster')
create_parser.add_argument('-i', default=False, action='store', dest='cluster_id', help='id of the cluster to be destroyed',)

# A add-resource command
create_parser = subparsers.add_parser('add-resource', help='Add a new resource')
create_parser.add_argument('-r', default=False, action='store', dest='new_resource', help='new resource',)

# A add-user command
create_parser = subparsers.add_parser('add-user', help='Add a new user')
create_parser.add_argument('-u', default=False, action='store', dest='new_user', help='new user',)

# A add-vspec command
create_parser = subparsers.add_parser('add-vspec', help='Add a new ???')
create_parser.add_argument('-v', default=False, action='store', dest='new_vspec', help='new ???',)

# A add-account command
create_parser = subparsers.add_parser('add-account', help='Add a new account')
create_parser.add_argument('-a', default=False, action='store', dest='new_account', help='new account',)

opts = parser.parse_args()
print 
print opts.cluster_specs
print opts.resource_specs
print opts.policy
