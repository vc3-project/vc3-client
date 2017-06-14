#!/bin/env python
__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

import argparse
import logging
import os

from ConfigParser import ConfigParser
from client import VC3ClientAPI

class VC3ClientCLI(object):
    '''
    
    '''
    def __init__(self):
        self.parseopts()
        self.setuplogging()

    def parseopts(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', 
                            action="store", 
                            dest='configpath', 
                            default='~/vc3-services/etc/vc3-client.conf', 
                            help='configuration file path.')
        
        parser.add_argument('-d', '--debug', 
                            action="store_true", 
                            dest='debug', 
                            help='debug logging')        

        parser.add_argument('-v', '--verbose', 
                            action="store_true", 
                            dest='verbose', 
                            help='verbose/info logging')            
        
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
        
        parser_userlist = subparsers.add_parser('user-list', 
                                                help='list vc3 user(s)')
        
        parser_userlist.add_argument('--username', 
                                     action="store")


        parser_projectcreate = subparsers.add_parser('project-create', 
                                                help='create new vc3 project')
        
        parser_projectcreate.add_argument('projectname', 
                                     action="store")

        parser_projectcreate.add_argument('--owner', 
                                     action="store", 
                                     dest="owner", 
                                     default='unknown')

        parser_projectcreate.add_argument('--members', 
                                     action="store", 
                                     dest="members", 
                                     default='unknown',
                                     help='comma-separated list of vc3users'
                                     )

        parser_projectadduser = subparsers.add_parser('project-adduser', 
                                                help='add user to vc3 project')
        
        parser_projectadduser.add_argument('project', 
                                     action="store")

        parser_projectadduser.add_argument('user', 
                                     action="store", 
                                     )
              
        
        parser_projectlist = subparsers.add_parser('project-list', 
                                                help='list all vc3 project(s)')

        parser_projectlist.add_argument('projectname', 
                                     action="store",
                                     help='list details of specified project')


        parser_resourcecreate = subparsers.add_parser('resource-create', 
                                                help='store new vc3 resource')
        
        parser_resourcecreate.add_argument('--name',
                                           dest = 'resourcename', 
                                           action="store")
        '''

                             accessmethod, 
                             accessflavor, 
                             gridresource, 
                             mfa=False, 
                             attributemap=None
        '''

        parser_resourcecreate.add_argument('--owner', 
                                     action="store", 
                                     dest="owner", 
                                    )

        parser_resourcecreate.add_argument('--type', 
                                     action="store", 
                                     dest="type", 
                                     )

        parser_resourcecreate.add_argument('--accessmethod', 
                                     action="store", 
                                     dest="accessmethod", 
                                     )

        parser_resourcecreate.add_argument('--accessflavor', 
                                     action="store", 
                                     dest="accessflavor", 
                                     )

        parser_resourcecreate.add_argument('--mfa', 
                                     action="store_true", 
                                     dest="mfa",
                                     default=False, 
                                     )        
        
                        
        parser_resourcelist = subparsers.add_parser('resource-list', 
                                                help='list vc3 resource(s)')

        parser_resourcelist.add_argument('--projectname', 
                                     action="store")


        parser_allocationcreate = subparsers.add_parser('allocation-create', 
                                                help='store new vc3 allocation')
        
        parser_allocationcreate.add_argument('allocationname', 
                                     action="store")

        parser_allocationcreate.add_argument('--owner', 
                                     action="store", 
                                     dest="owner", 
                                     default='unknown')

        parser_allocationcreate.add_argument('--members', 
                                     action="store", 
                                     dest="members", 
                                     default='unknown')
        
        parser_allocationlist = subparsers.add_parser('allocation-list', 
                                                help='list vc3 allocation(s)')

        parser_allocationlist.add_argument('--projectname', 
                                     action="store")






        self.results= parser.parse_args()



    def setuplogging(self):
        self.log = logging.getLogger()
        FORMAT='%(asctime)s (UTC) [ %(levelname)s ] %(name)s %(filename)s:%(lineno)d %(funcName)s(): %(message)s'
        formatter = logging.Formatter(FORMAT)
        #formatter.converter = time.gmtime  # to convert timestamps to UTC
        logStream = logging.StreamHandler()
        logStream.setFormatter(formatter)
        self.log.addHandler(logStream)
    
        self.log.setLevel(logging.WARN)
        if self.results.debug:
            self.log.setLevel(logging.DEBUG)
        if self.results.verbose:
            self.log.setLevel(logging.INFO)
        self.log.info('Logging initialized.')


    def run(self):
        cp = ConfigParser()
        ns = self.results
        self.log.info("Config is %s" % ns.configpath)
        cp.read(os.path.expanduser(ns.configpath))

        capi = VC3ClientAPI(cp)
        
        # User commands
        if ns.subcommand == 'user-create':
            u = capi.defineUser( ns.username,
                             ns.firstname,
                             ns.lastname,
                             ns.email,
                             ns.institution)
            self.log.debug("User is %s" % u)
            capi.storeUser(u)
            
        elif ns.subcommand == 'user-list' and ns.username is None:
            ulist = capi.listUsers()
            for u in ulist:
                print(u)
        
        elif ns.subcommand == 'user-list' and ns.username is not None:
            uo = capi.getUser(ns.username)
            print(uo)
        
        # Project commands
        elif ns.subcommand == 'project-create':
            p = capi.defineProject( ns.projectname,
                                    ns.owner,
                                    ns.members)
            self.log.debug("Project is %s" % p)
            capi.storeUser(p)    
            
        elif ns.subcommand == 'project-list' and ns.projectname is None:
            plist = capi.listProjects()
            for p in plist:
                print(p)
        
        elif ns.subcommand == 'project-list' and ns.projectname is not None:
            po = capi.getProject(ns.projectname)
            print(po)

        elif ns.subcommand == 'project-adduser':
            po = capi.getProject(ns.project)
            po.addUser(ns.user)
            capi.storeProject(po)
            
        # Resource commands
        elif ns.subcommand == 'resource-create':
            r = capi.defineProject( ns.resourcename,
                                    ns.owner,
                                    )
            self.log.debug("Project is %s" % p)
            capi.storeUser(p)    
            
        elif ns.subcommand == 'resource-list' and ns.resourcename is None:
            plist = capi.listProjects()
            for p in plist:
                print(p)
        
        elif ns.subcommand == 'resource-list' and ns.resourcename is not None:
            po = capi.getProject(ns.resourcename)
            print(po)
        
        
        # Allocation commands
        elif ns.subcommand == 'allocation-create':
            a = capi.defineAllocation( ns.allocationname,
                                       ns.owner,
                                       ns.resource,
                                       
                                       )
            self.log.debug("Allocation is %s" % a)
            capi.storeUser(p)    
            
        elif ns.subcommand == 'allocation-list' and ns.allocationname is None:
            plist = capi.listProjects()
            for p in plist:
                print(p)
        
        elif ns.subcommand == 'allocation-list' and ns.allocationname is not None:
            po = capi.getProject(ns.allocationname)
            print(po)
        
        
        else:
            self.log.warning('Unrecognized subcommand is %s' % ns.subcommand)
            

if __name__ == '__main__':
    vc3cli = VC3ClientCLI()
    vc3cli.run()    