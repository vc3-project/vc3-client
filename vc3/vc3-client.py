#!/usr/bin/env python

import argparse

from vc3 import client

class VC3ClientCLI(object):
    '''
    vc3-client
     --version
     --debug
     --infoserver <host:port>
     --cert
     --key
     
        user-create
        user-update
        user-delete
        user-list    [user-name]
        
        project-create
        project-update
        project-delete 
        project-list    [project-name]
        
        resource-create
        resource-update
        resource-delete
        resource-list      [resource-label]
  
        allocation-create
        allocation-update
        allocation-delete
        allocation-list     [allocation-label]
        
        
        
    
    '''
    
    def __init__(self):
        self.parseopts()
        self.setuplogging()


    def parseopts(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', 
                            action="store", 
                            dest='configpath', 
                            default='~/etc/vc3-client.conf', 
                            help='configuration file path.')
        
        parser.add_argument('-d', '--debug', 
                            action="store_true", 
                            dest='debug', 
                            help='debug logging')        
        
        parser.add_argument('-i','--infoserver',
                            action='store',
                            dest='infoserver',
                            default='infoserver.domain.com',
                            help='explicitly define infoserver')
        
               
        
        # Init sub-command
        subparsers = parser.add_subparsers( dest="subcommand")
        
        parser_usercreate = subparsers.add_parser('user-create', 
                                                help='create new vc3 user')
        parser_usercreate.add_argument('username', 
                                     action="store")
        
        parser_usercreate.add_argument('--firstname', 
                                     action="store", 
                                     dest="firstname", 
                                     default='unknown')

        parser_usercreate.add_argument('--lastname', 
                                     action="store", 
                                     dest="lastname", 
                                     default='unknown')

        parser_usercreate.add_argument('--email', 
                                     action="store", 
                                     dest="email", 
                                     default='unknown')

        parser_usercreate.add_argument('--institution', 
                                     action="store", 
                                     dest="institution", 
                                     default='unknown')        

        self.results= parser.parse_args()
        #parser_init.add_argument(...)      
        print("VC3 Client!")
        print(self.results)

    def invoke(self):
        cp = ConfigParser()
        ns = self.results
        print("Config is %s" % ns.configpath)
        cp.read(os.path.expanduser(ns.configpath))
        
        capi = client.VC3ClientAPI(cp)
        
        
        if ns.subcommand == 'usercreate':
            capi.createUser( ns.name,
                             ns.firstname,
                             ns.lastname,
                             ns.email,
                             ns.institution)


    
        #self.log.debug("Running...")
        



if __name__ == '__main__':
    vc3cli = VC3ClientCLI()
    vc3cli.invoke()



parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')

# A create-cluster command
create_parser = subparsers.add_parser('cluster', help='Create a cluster')
create_parser.add_argument('-c', default=False, action='store', dest='cluster_specs', help='file with cluster specifications',)
create_parser.add_argument('-r', default=False, action='store', dest='resource_specs', help='file with resources specifications',)
create_parser.add_argument('-p', default=False, action='store', dest='policy', help='file with policies',)


# A destroy-cluster command
create_parser = subparsers.add_parser('request', help='Destroy a cluster')
create_parser.add_argument('-i', default=False, action='store', dest='cluster_id', help='id of the cluster to be destroyed',)

# A add-resource command
create_parser = subparsers.add_parser('resource', help='Add a new resource')
create_parser.add_argument('-r', default=False, action='store', dest='new_resource', help='new resource',)

# A add-user command
create_parser = subparsers.add_parser('user', help='Add a new user')
create_parser.add_argument('-u', default=False, action='store', dest='new_user', help='new user',)

# A add-vspec command
create_parser = subparsers.add_parser('cluster', help='Add a new ???')
create_parser.add_argument('-v', default=False, action='store', dest='new_cluster', help='new ???',)

# A add-account command
create_parser = subparsers.add_parser('allocation', help='Add a new account')
create_parser.add_argument('-a', default=False, action='store', dest='new_account', help='new account',)

opts = parser.parse_args()
print 
print opts.cluster_specs
print opts.resource_specs
print opts.policy
