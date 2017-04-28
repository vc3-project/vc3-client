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

from entities import User, Project, Resource, Allocation, Request, Cluster, Application
from vc3 import infoclient

class VC3ClientAPI(object):
    def __init__(self, config):
        self.config = config
        self.ic = infoclient.InfoClient(self.config)
        self.log = logging.getLogger() 


    def defineUser(self,   
                   name,
                   first,
                   last,
                   email,
                   institution):           
        '''
       Defines a new User object for usage elsewhere in the API. 
              
       :param str name: The unique VC3 username of this user
       :param str first: User's first name
       :param str last: User's last name
       :param str email: User's email address
       :param str institution: User's intitutional affiliation or employer
       :return: User  A valid User object
       
       :rtype: User        
        '''
        u = User( name, first, last, email, institution)
        self.log.debug("Creating user: %s " % u)
        return u
    
        
    def createUser(self, user, infoclient=None):
        '''
        Stores the provided user in the infoservice. 
        
        :param User u:  User to add. 
        :return: None
        '''
        if infoclient is None:
            infoclient = self.ic
        user.store(infoclient)
        
                
        
    def updateUser(self, u ):
        '''
        
        '''

    def listUsers(self):
        doc = self.ic.getdocument('users')
        

        print(out)

    def getUser(self, username):
        pass

    
    def createProject(self):
        pass
    
    def updateProject(self):
        pass
    
    def showProject(self):
        pass
    
        
    def createResource(self):
        pass
    
    def ListResources(self):
        pass
    
    def createAllocation(self):
        pass

    def listAllocations(self):
        pass
    
    def createCluster(self):
        pass
    
    def listClusters(self):
        pass
    
    
class EntityExistsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


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
                            default='~/etc/vc3client.conf', 
                            help='configuration file path.')
        
        parser.add_argument('-d', '--debug', 
                            action="store_true", 
                            dest='debug', 
                            help='debug logging')        
        
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
        self.log.info('Logging initialized.')


    def invoke(self):
        cp = ConfigParser()
        ns = self.results
        self.log.info("Config is %s" % ns.configpath)
        cp.read(os.path.expanduser(ns.configpath))

        capi = VC3ClientAPI(cp)
        
        if ns.subcommand == 'user-create':
            
            u = capi.defineUser( ns.username,
                             ns.firstname,
                             ns.lastname,
                             ns.email,
                             ns.institution)
            self.log.debug("User is %s" % u)
            capi.createUser(u)
            
        else:
            self.log.warning('Unrecognized subcommand is %s' % ns.subcommand)
            

if __name__ == '__main__':
    vc3cli = VC3ClientCLI()
    vc3cli.invoke()    




